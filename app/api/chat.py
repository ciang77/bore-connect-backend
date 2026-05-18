import os
import requests
import json
from dotenv import load_dotenv
from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
API_KEY = os.getenv("QWEN_API_KEY")

API_URL = os.getenv(
    "QWEN_API_URL",
    "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
)
MODEL_NAME = os.getenv("QWEN_MODEL", "qwen3.6-35b-a3b")

_session = requests.Session()
_session.trust_env = False

class QARequest(BaseModel):
    question: str
    max_tokens: int = 500
    temperature: float = 0.2

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.get("/ping")
def ping():
    return {"ok": True, "model": MODEL_NAME}

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

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": req.question}],
        "max_tokens": req.max_tokens,
        "temperature": req.temperature,
        "stream": True,
    }

    try:
        resp = _session.post(
            API_URL,
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
                    yield f"data: {json.dumps({'delta': content}, ensure_ascii=False)}\n\n"
            yield f"data: {json.dumps({'done': True}, ensure_ascii=False)}\n\n"
        finally:
            resp.close()

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@router.get("/sse")
def sse(question: str, max_tokens: int = 500, temperature: float = 0.2):
    req = QARequest(question=question, max_tokens=max_tokens, temperature=temperature)
    return qa_stream(req)


@router.get("/ui", response_class=HTMLResponse)
def ui():
    html = """
<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Qwen SSE 测试</title>
    <style>
      body { font-family: system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, "PingFang SC", "Microsoft YaHei", sans-serif; margin: 24px; }
      .row { display: flex; gap: 8px; }
      input { flex: 1; padding: 10px 12px; font-size: 14px; }
      button { padding: 10px 14px; font-size: 14px; cursor: pointer; }
      #out { white-space: pre-wrap; border: 1px solid #ddd; padding: 12px; margin-top: 12px; min-height: 180px; }
      .muted { color: #666; font-size: 12px; margin-top: 10px; }
    </style>
  </head>
  <body>
    <h3>Qwen SSE 流式输出测试</h3>
    <div class="row">
      <input id="q" placeholder="输入问题，例如：用三句话解释什么是 SSE" />
      <button id="btn">发送</button>
      <button id="stop">停止</button>
    </div>
    <div id="out"></div>
    <div class="muted" id="status"></div>
    <script>
      const q = document.getElementById("q");
      const out = document.getElementById("out");
      const status = document.getElementById("status");
      const btn = document.getElementById("btn");
      const stop = document.getElementById("stop");
      let es = null;

      function closeES() {
        if (es) {
          es.close();
          es = null;
        }
      }

      function setStatus(s) {
        status.textContent = s;
      }

      btn.addEventListener("click", () => {
        const text = (q.value || "").trim();
        if (!text) return;
        closeES();
        out.textContent = "";
        setStatus("连接中...");
        const url = "/chat/sse?question=" + encodeURIComponent(text) + "&temperature=0.2&max_tokens=500";
        es = new EventSource(url);
        es.onopen = () => setStatus("已连接，等待流式输出...");
        es.onmessage = (ev) => {
          try {
            const data = JSON.parse(ev.data);
            if (data.done) {
              setStatus("已完成");
              closeES();
              return;
            }
            if (data.delta) out.textContent += data.delta;
          } catch (e) {
            out.textContent += ev.data;
          }
        };
        es.onerror = () => {
          setStatus("连接异常或中断");
          closeES();
        };
      });

      stop.addEventListener("click", () => {
        setStatus("已停止");
        closeES();
      });
    </script>
  </body>
</html>
"""
    return HTMLResponse(content=html)


app = FastAPI(title="Qwen 企业问答服务")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173"],  # 你的前端地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)
