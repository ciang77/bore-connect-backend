"""实时报警开关 API"""
from fastapi import APIRouter

from app.services.alert import is_alert_enabled, set_alert_enabled

router = APIRouter(prefix="/api/alert", tags=["alert"])


@router.get("/status")
def get_alert_status():
    """获取实时报警开关状态"""
    return {"code": 200, "data": {"enabled": is_alert_enabled()}}


@router.post("/toggle")
def toggle_alert(data: dict):
    """切换实时报警开关  {enabled: true/false}"""
    enabled = bool(data.get("enabled", False))
    set_alert_enabled(enabled)
    return {"code": 200, "data": {"enabled": enabled}, "msg": "实时报警已开启" if enabled else "实时报警已关闭"}
