import os
from contextlib import asynccontextmanager
from datetime import datetime

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.chat import router as chat_router
from app.routers.overview import router as overview_router
from app.routers.analysis import router as analysis_router
from app.routers.diagnosis import router as diagnosis_router
from app.routers.alert import router as alert_router
from app.config.settings import settings
from app.services.alert import start_alert_monitor


@asynccontextmanager
async def lifespan(_app: FastAPI):
    start_alert_monitor(interval=30)
    yield


app = FastAPI(title="Bore Connect", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:8000", "http://127.0.0.1:8000", "http://127.0.0.1:9090", "http://localhost:9090"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)

app.include_router(chat_router)
app.include_router(overview_router)
app.include_router(analysis_router)
app.include_router(diagnosis_router)
app.include_router(alert_router)


@app.get("/api/health")
def health_check():
    return {"status": "ok"}


@app.get("/api/test-alert")
def test_alert():
    """手动触发测试告警邮件"""
    from app.services.alert import send_alert_email

    body = """
    <table style="width:100%; border-collapse: collapse; color: #e0e0e0;">
        <tr><td style="padding:8px 0; color: #888; width:80px;">测试时间</td>
            <td style="padding:8px 0; color: #fff;">""" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</td></tr>
        <tr><td style="padding:8px 0; color: #888;">测试说明</td>
            <td style="padding:8px 0; color: #00ff88;">这是一封测试邮件，验证告警系统正常工作</td></tr>
    </table>
    <p style="margin-top: 16px; color: #00ff88;">
        ✅ 如果您能收到此邮件，说明告警系统已配置成功。
    </p>
    """
    ok = send_alert_email("[Bore Connect] 告警测试邮件", body)
    return {"status": "ok" if ok else "fail", "msg": "邮件已发送" if ok else "发送失败，请查看日志"}


static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.isdir(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=settings.DEBUG, workers=4)
