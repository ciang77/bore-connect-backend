import os
import json
from pathlib import Path

import jieba
import requests
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

load_dotenv()

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
    with open(_kb_path, encoding="utf-8") as f:
        data = json.load(f)
    for category, statuses in data.items():
        for status, faults in statuses.items():
            for item in faults:
                fault = item["fault"].strip().rstrip("，,")
                cause = item["cause"].strip()
                text = fault.lower()
                tokens = {t for t in jieba.lcut(text) if len(t.strip()) > 1}
                _kb_entries.append({
                    "category": category,
                    "status": status,
                    "fault": fault,
                    "cause": cause,
                    "tokens": tokens,
                })

_load_kb()

MATCH_THRESHOLD = 0.25

def match_kb(question: str) -> dict | None:
    query_text = question.lower()
    query_tokens = {t for t in jieba.lcut(query_text) if len(t.strip()) > 1}
    if not query_tokens:
        return None

    best = None
    best_score = 0.0
    for entry in _kb_entries:
        overlap = len(query_tokens & entry["tokens"])
        score = overlap / len(query_tokens)
        if score > best_score:
            best_score = score
            best = entry

    if best and best_score >= MATCH_THRESHOLD:
        return {"entry": best, "score": best_score}
    return None


# ── model configs ──

MODEL_CONFIGS = {
    "qwen": {
        "api_key": os.getenv("QWEN_API_KEY"),
        "api_url": os.getenv(
            "QWEN_API_URL",
            "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
        ),
        "model": os.getenv("QWEN_MODEL", "qwen3.6-35b-a3b"),
    },
    "deepseek": {
        "api_key": os.getenv("DEEPSEEK_API_KEY"),
        "api_url": os.getenv(
            "DEEPSEEK_API_URL",
            "https://api.deepseek.com/v1/chat/completions",
        ),
        "model": os.getenv("DEEPSEEK_MODEL", "deepseek-v4-flash"),
    },
}

DEFAULT_MODEL = "qwen"

_session = requests.Session()
_session.trust_env = False

class QARequest(BaseModel):
    question: str
    model: str = DEFAULT_MODEL
    max_tokens: int = 2048
    temperature: float = 0.2

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.get("/ping")
def ping():
    return {"ok": True, "models": list(MODEL_CONFIGS.keys()), "default": DEFAULT_MODEL}

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

@router.post("/qa/stream")
def qa_stream(req: QARequest):
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="question is required")

    # ── 优先匹配知识库 ──
    kb_match = match_kb(req.question)
    if kb_match:
        e = kb_match["entry"]
        lines = [
            f"【{e['category']} · {e['status']}】",
            f"故障：{e['fault']}",
            f"原因：{e['cause']}",
        ]

        def kb_stream():
            for line in lines:
                yield json.dumps({"delta": line + "\n"}, ensure_ascii=False) + "\n"
            yield json.dumps({"done": True}, ensure_ascii=False) + "\n"

        return StreamingResponse(kb_stream(), media_type="application/x-ndjson")

    # ── 知识库未命中，走大模型 ──
    config = MODEL_CONFIGS.get(req.model)
    if not config:
        raise HTTPException(status_code=400, detail=f"unknown model: {req.model}")

    if not config["api_key"]:
        raise HTTPException(status_code=500, detail=f"API key not configured for {req.model}")

    headers = {
        "Authorization": f"Bearer {config['api_key']}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": config["model"],
        "messages": [{"role": "user", "content": req.question}],
        "max_tokens": req.max_tokens,
        "temperature": req.temperature,
        "stream": True,
    }

    try:
        resp = _session.post(
            config["api_url"],
            headers=headers,
            json=payload,
            timeout=(5, 30),
            stream=True,
            proxies={"http": None, "https": None},
            verify=True
        )
        resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=str(e))

    def event_stream():
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

    return StreamingResponse(
        event_stream(),
        media_type="application/x-ndjson",
    )



