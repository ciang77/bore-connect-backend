import json
import logging
from pathlib import Path

import jieba
import requests
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from app.config.settings import settings

logger = logging.getLogger(__name__)

# ── knowledge base ──
_kb_path = Path(__file__).parent.parent / "knowledge" / "faults.json"
_kb_entries: list[dict] = []

_jieba_loaded = False

def _load_kb():
    global _kb_entries, _jieba_loaded
    if not _jieba_loaded:
        jieba.initialize()
        for w in ["空开", "跳闸", "静压", "编码器", "变位机", "排屑器", "铣头",
                   "龙门架", "回零", "手轮", "扫码枪", "内冷", "外冷", "航车",
                   "限位", "光栅尺", "变频器", "离合器", "护罩", "冷却液"]:
            jieba.add_word(w)
        _jieba_loaded = True

    if _kb_entries:
        return

    if not _kb_path.exists():
        logger.warning("知识库文件不存在: %s", _kb_path)
        return

    try:
        with open(_kb_path, encoding="utf-8") as f:
            data = json.load(f)
        for category, statuses in data.items():
            for status, faults in statuses.items():
                for item in faults:
                    fault = item.get("fault", "").strip().rstrip("，,")
                    cause = item.get("cause", "").strip()
                    if not fault:
                        continue
                    text = fault.lower()
                    tokens = {t for t in jieba.lcut(text) if len(t.strip()) > 1}
                    _kb_entries.append({
                        "category": category,
                        "status": status,
                        "fault": fault,
                        "cause": cause,
                        "tokens": tokens,
                    })
        logger.info("知识库加载完成: %d 条记录", len(_kb_entries))
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        logger.error("知识库加载失败: %s", e)
        _kb_entries = []

_load_kb()

MATCH_THRESHOLD = 0.25
MATCH_TOP_K = 3

def match_kb(question: str, top_k: int = MATCH_TOP_K) -> list[dict]:
    query_text = question.lower()
    query_tokens = {t for t in jieba.lcut(query_text) if len(t.strip()) > 1}
    if not query_tokens:
        return []

    scored = []
    for entry in _kb_entries:
        overlap = len(query_tokens & entry["tokens"])
        score = overlap / len(query_tokens)
        if score >= MATCH_THRESHOLD:
            scored.append({"entry": entry, "score": score})

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k]


# ── model configs ──

MODEL_CONFIGS = {
    "qwen": {
        "api_key": settings.QWEN_API_KEY,
        "api_url": settings.QWEN_API_URL,
        "model": settings.QWEN_MODEL,
    },
    "deepseek": {
        "api_key": settings.DEEPSEEK_API_KEY,
        "api_url": settings.DEEPSEEK_API_URL,
        "model": settings.DEEPSEEK_MODEL,
    },
}

DEFAULT_MODEL = "qwen"

SYSTEM_PROMPT = (
    "你是龙门镗铣床设备的智能助手，可以回答设备操作、维护保养、故障诊断等各类问题。"
    "请用简洁专业的语言回答，不要使用星号、井号等 Markdown 符号。"
    "回答要有条理，分点说明。如果不确定，说明需要进一步排查的方向。"
)

_session = requests.Session()
_session.trust_env = False

class QARequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=2000)
    model: str = DEFAULT_MODEL
    max_tokens: int = Field(default=2048, ge=1, le=8192)
    temperature: float = Field(default=0.2, ge=0.0, le=2.0)

router = APIRouter(prefix="/api/chat", tags=["Chat"])

def _openai_compatible_stream_iter(resp: requests.Response):
    for raw_line in resp.iter_lines(decode_unicode=True):
        if not raw_line:
            continue
        line = raw_line.strip()
        if not line.startswith("data:"):
            continue
        data_str = line[5:].strip()
        if data_str == "[DONE]":
            break
        try:
            yield json.loads(data_str)
        except json.JSONDecodeError:
            continue


def _call_llm(config: dict, messages: list[dict], max_tokens: int, temperature: float):
    """调用大模型并返回 streaming Response，失败时抛出 RequestException。"""
    headers = {
        "Authorization": f"Bearer {config['api_key']}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": config["model"],
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "stream": True,
    }
    resp = _session.post(
        config["api_url"],
        headers=headers,
        json=payload,
        timeout=(5, 30),
        stream=True,
        proxies={"http": None, "https": None},
        verify=True,
    )
    resp.raise_for_status()
    return resp


def _stream_llm(resp: requests.Response):
    """将 LLM SSE 流转为 NDJSON 生成器。"""
    try:
        for data in _openai_compatible_stream_iter(resp):
            choice0 = (data.get("choices") or [{}])[0]
            delta = choice0.get("delta") or {}
            content = delta.get("content")
            if content:
                yield json.dumps({"delta": content}, ensure_ascii=False) + "\n"
        yield json.dumps({"done": True}, ensure_ascii=False) + "\n"
    finally:
        resp.close()


def _raw_kb_stream(entries: list[dict]):
    """降级方案：直接输出知识库原始数据。"""
    for e in entries:
        lines = [
            f"【{e['category']} · {e['status']}】",
            f"故障：{e['fault']}",
            f"原因：{e['cause']}",
        ]
        for line in lines:
            yield json.dumps({"delta": line + "\n"}, ensure_ascii=False) + "\n"
    yield json.dumps({"done": True}, ensure_ascii=False) + "\n"


@router.post("/completions")
def chat_completions(req: QARequest):
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="question is required")

    config = MODEL_CONFIGS.get(req.model)
    if not config:
        raise HTTPException(status_code=400, detail=f"unknown model: {req.model}")
    if not config["api_key"]:
        raise HTTPException(status_code=500, detail=f"API key not configured for {req.model}")

    # ── 匹配知识库 ──
    kb_matches = match_kb(req.question)

    if kb_matches:
        # 把检索结果作为上下文，交给大模型组织语言
        context_parts = []
        for m in kb_matches:
            e = m["entry"]
            context_parts.append(
                f"- 故障类型：{e['category']}，设备状态：{e['status']}\n"
                f"  故障描述：{e['fault']}\n"
                f"  原因分析：{e['cause']}"
            )
        kb_context = "以下是知识库中的相关记录：\n" + "\n".join(context_parts)

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"{kb_context}\n\n用户问题：{req.question}\n\n请根据以上知识库记录回答用户问题。"},
        ]

        try:
            resp = _call_llm(config, messages, req.max_tokens, req.temperature)
            return StreamingResponse(
                _stream_llm(resp),
                media_type="application/x-ndjson",
            )
        except requests.exceptions.RequestException:
            # 大模型不可用时降级为原始知识库数据
            entries = [m["entry"] for m in kb_matches]
            return StreamingResponse(
                _raw_kb_stream(entries),
                media_type="application/x-ndjson",
            )

    # ── 知识库未命中，走大模型 ──
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": req.question},
    ]

    try:
        resp = _call_llm(config, messages, req.max_tokens, req.temperature)
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=str(e))

    return StreamingResponse(
        _stream_llm(resp),
        media_type="application/x-ndjson",
    )
