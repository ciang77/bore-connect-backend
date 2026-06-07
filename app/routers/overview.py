import random
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.overview import Alarm, Device, DeviceRealtime, Subsystem, SubsystemRealtime, TrendData

router = APIRouter(prefix="/api/overview", tags=["Overview"])


def _pick_realtime(db: Session) -> DeviceRealtime | None:
    """按3秒窗口取模轮换，同窗口内 device-status 和 subsystems 拿到同一行"""
    count = db.query(DeviceRealtime).count()
    if count == 0:
        return None
    idx = (int(datetime.now().timestamp()) // 3) % count
    return (
        db.query(DeviceRealtime)
        .order_by(DeviceRealtime.id)
        .offset(idx)
        .first()
    )


@router.get("/device-status")
def get_device_status(db: Session = Depends(get_db)):
    device = db.query(Device).first()
    if not device:
        return {"code": 0, "data": None, "msg": "no device found"}

    realtime = _pick_realtime(db)

    # 温度、振动、伺服电流与24h趋势图完全一致：同一个5分钟桶聚合，取最新一个桶
    latest_bucket = (
        db.query(
            func.avg(TrendData.servo_current).label("servo_current"),
            func.avg(TrendData.vibration).label("vibration"),
            func.avg(TrendData.temperature).label("temperature"),
        )
        .filter(TrendData.record_time >= datetime.now() - timedelta(hours=24))
        .group_by(
            func.date_format(TrendData.record_time, "%Y%m%d%H"),
            func.floor(func.minute(TrendData.record_time) / 5),
        )
        .order_by(func.min(TrendData.record_time).desc())
        .first()
    )

    if latest_bucket and latest_bucket.temperature is not None:
        temperature = f"{latest_bucket.temperature:.0f}°C"
        vibration = f"{latest_bucket.vibration:.1f}mm/s"
        servo_current = f"{latest_bucket.servo_current:.1f}A"
    else:
        temperature = "0°C"
        vibration = "0mm/s"
        servo_current = "0A"

    return {
        "code": 0,
        "data": {
            "name": device.name,
            "model": device.model,
            "status": device.status,
            "runtime": f"{realtime.runtime:.1f}h" if realtime else "0h",
            "temperature": temperature,
            "vibration": vibration,
            "pressure": f"{realtime.pressure:.1f}MPa" if realtime else "0MPa",
            "spindleSpeed": f"{realtime.spindle_speed}RPM" if realtime else "0RPM",
            "servoCurrent": servo_current,
        },
    }


@router.get("/subsystems")
def get_subsystems(db: Session = Depends(get_db)):
    # 实时数据源：与 device-status 同源
    latest_bucket = (
        db.query(
            func.avg(TrendData.servo_current).label("servo_current"),
            func.avg(TrendData.vibration).label("vibration"),
            func.avg(TrendData.temperature).label("temperature"),
        )
        .filter(TrendData.record_time >= datetime.now() - timedelta(hours=24))
        .group_by(
            func.date_format(TrendData.record_time, "%Y%m%d%H"),
            func.floor(func.minute(TrendData.record_time) / 5),
        )
        .order_by(func.min(TrendData.record_time).desc())
        .first()
    )
    realtime = _pick_realtime(db)

    # 主轴实时值 — 直接从 trend_data / device_realtime 生成，不依赖 subsystem_realtime
    spindle_metrics = [
        {"label": "振动监测", "value": f"{latest_bucket.vibration:.1f}" if latest_bucket and latest_bucket.vibration is not None else "0", "unit": "mm/s"},
        {"label": "温度监测", "value": f"{latest_bucket.temperature:.0f}" if latest_bucket and latest_bucket.temperature is not None else "0", "unit": "°C"},
        {"label": "电流监测", "value": f"{latest_bucket.servo_current:.1f}" if latest_bucket and latest_bucket.servo_current is not None else "0", "unit": "A"},
        {"label": "转速监测", "value": str(realtime.spindle_speed) if realtime else "0", "unit": "RPM"},
    ]

    # 液压系统压力与 device-status 同源
    hydraulic_pressure = f"{realtime.pressure:.1f}" if realtime else "0"

    subs = db.query(Subsystem).all()
    result = []
    for sub in subs:
        if sub.name_en == "SPINDLE":
            metrics = spindle_metrics
        else:
            rows = (
                db.query(SubsystemRealtime)
                .filter(SubsystemRealtime.subsystem_id == sub.id)
                .all()
            )
            grouped: dict[str, list] = {}
            for r in rows:
                grouped.setdefault(r.label, []).append(r)
            picked = {label: random.choice(items) for label, items in grouped.items()}

            metrics = []
            for label, m in picked.items():
                if sub.name_en == "HYDRAULIC" and label == "系统压力":
                    value = hydraulic_pressure
                else:
                    value = str(m.value)
                metrics.append({"label": label, "value": value, "unit": m.unit})

            metrics.sort(key=lambda x: x["label"])

        result.append({
            "name": sub.name,
            "nameEn": sub.name_en,
            "status": sub.status,
            "healthScore": sub.health_score,
            "metrics": metrics,
        })

    return {"code": 0, "data": result}


_WEEKDAY_CN = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]


@router.get("/trend-data")
def get_trend_data(
    range: str = Query("24h", pattern="^(24h|7d)$"),
    db: Session = Depends(get_db),
):
    now = datetime.now()

    if range == "7d":
        since = now - timedelta(days=7)
        rows = (
            db.query(
                func.min(TrendData.record_time).label("ts"),
                func.avg(TrendData.servo_current).label("servo_current"),
                func.avg(TrendData.vibration).label("vibration"),
                func.avg(TrendData.temperature).label("temperature"),
            )
            .filter(TrendData.record_time >= since)
            .group_by(func.date_format(TrendData.record_time, "%Y%m%d%H"))
            .order_by("ts")
            .all()
        )
        labels = [
            _WEEKDAY_CN[r.ts.weekday()] if r.ts else ""
            for r in rows
        ]
    else:
        since = now - timedelta(hours=24)
        # 按5分钟降采样，避免数据点过多
        rows = (
            db.query(
                func.min(TrendData.record_time).label("ts"),
                func.avg(TrendData.servo_current).label("servo_current"),
                func.avg(TrendData.vibration).label("vibration"),
                func.avg(TrendData.temperature).label("temperature"),
            )
            .filter(TrendData.record_time >= since)
            .group_by(
                func.date_format(TrendData.record_time, "%Y%m%d%H"),
                func.floor(func.minute(TrendData.record_time) / 5),
            )
            .order_by("ts")
            .all()
        )
        labels = [r.ts.strftime("%H:%M") for r in rows]

    servo_current = [round(float(r.servo_current), 2) for r in rows]
    vibration = [round(float(r.vibration), 2) for r in rows]
    temperature = [round(float(r.temperature), 2) for r in rows]

    return {
        "code": 0,
        "data": {
            "labels": labels,
            "servoCurrent": servo_current,
            "vibration": vibration,
            "temperature": temperature,
        },
    }


@router.get("/alarms")
def get_alarms(db: Session = Depends(get_db)):
    """获取最近告警列表（最多 50 条，按时间倒序）"""
    rows = (
        db.query(Alarm)
        .order_by(Alarm.alarm_time.desc())
        .limit(50)
        .all()
    )
    data = [
        {
            "id": r.id,
            "time": r.alarm_time.strftime("%H:%M:%S"),
            "level": r.level,
            "subsystem": r.subsystem,
            "msg": r.msg,
        }
        for r in rows
    ]
    return {"code": 0, "data": data}
