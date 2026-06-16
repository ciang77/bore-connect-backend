import asyncio
import hashlib
import json
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy import func, text
from sqlalchemy.orm import Session

from app.database.machine_connection import MachineSessionLocal, get_machine_db

router = APIRouter(prefix="/api/test", tags=["Test"])

TAG_NAMES = ["axis_x_actPosition", "axis_x_setPosition", "axis_x_speed"]


def _get_latest_source_time(db: Session) -> str | None:
    """获取 history_data 中真正最新的 source_time（不经过聚合）"""
    row = db.execute(
        text("SELECT MAX(source_time) FROM history_data "
             "WHERE tag_code IN ('axis_x_actPosition', 'axis_x_setPosition', 'axis_x_speed')")
    ).scalar()
    return row.isoformat() if row else None


def _get_latest_values(db: Session) -> dict:
    """从 realtime_data 获取三个 tag 的最新值（覆盖表，始终 3 行）"""
    result = db.execute(
        text("SELECT tag_code, value_num, update_time FROM realtime_data "
             "WHERE tag_code IN ('axis_x_actPosition', 'axis_x_setPosition', 'axis_x_speed') "
             "ORDER BY tag_code")
    ).fetchall()
    vals = {}
    for r in result:
        vals[r[0]] = {"value": round(float(r[1]), 4), "time": r[2].isoformat()}
    return vals


def _query_pivoted(db: Session, since: datetime, group_by_hour_only: bool):
    """从 history_data 查询并转换为按 tag_code 分列的时序数据。

    表结构为 EAV（tag_code / value_num / source_time），
    这里将三个 tag 各自 pivot 为一列。
    """
    tags_str = ",".join(f"'{t}'" for t in TAG_NAMES)

    if group_by_hour_only:
        # 7d — 按小时聚合
        sql = text(f"""
            SELECT
                DATE_FORMAT(MIN(source_time), '%m/%d %H:00') AS ts_label,
                MIN(source_time) AS ts,
                AVG(CASE WHEN tag_code = 'axis_x_actPosition' THEN value_num END) AS act,
                AVG(CASE WHEN tag_code = 'axis_x_setPosition' THEN value_num END) AS set_,
                AVG(CASE WHEN tag_code = 'axis_x_speed' THEN value_num END) AS speed
            FROM history_data
            WHERE tag_code IN ({tags_str}) AND source_time >= :since
            GROUP BY DATE_FORMAT(source_time, '%Y%m%d%H')
            ORDER BY ts
        """)
    else:
        # 24h — 按 5 分钟聚合
        sql = text(f"""
            SELECT
                DATE_FORMAT(MIN(source_time), '%H:%i') AS ts_label,
                MIN(source_time) AS ts,
                AVG(CASE WHEN tag_code = 'axis_x_actPosition' THEN value_num END) AS act,
                AVG(CASE WHEN tag_code = 'axis_x_setPosition' THEN value_num END) AS set_,
                AVG(CASE WHEN tag_code = 'axis_x_speed' THEN value_num END) AS speed
            FROM history_data
            WHERE tag_code IN ({tags_str}) AND source_time >= :since
            GROUP BY DATE_FORMAT(source_time, '%Y%m%d%H'), FLOOR(MINUTE(source_time) / 5)
            ORDER BY ts
        """)

    result = db.execute(sql, {"since": since})
    rows = result.fetchall()

    labels = [r.ts_label for r in rows]
    act_position = [round(float(r.act), 3) if r.act is not None else 0 for r in rows]
    set_position = [round(float(r.set_), 3) if r.set_ is not None else 0 for r in rows]
    speed = [round(float(r.speed), 3) if r.speed is not None else 0 for r in rows]

    return labels, act_position, set_position, speed


@router.get("/realtime-data")
def get_realtime_data(
    range: str = Query("24h", pattern="^(24h|7d)$"),
    db: Session = Depends(get_machine_db),
):
    now = datetime.now()
    since = now - timedelta(days=7) if range == "7d" else now - timedelta(hours=24)
    group_by_hour = range == "7d"

    labels, act_position, set_position, speed = _query_pivoted(db, since, group_by_hour)
    latest_time = _get_latest_source_time(db)
    latest_values = _get_latest_values(db)

    return {
        "code": 0,
        "data": {
            "labels": labels,
            "actPosition": act_position,
            "setPosition": set_position,
            "speed": speed,
            "latestTime": latest_time,
            "latestValues": latest_values,
        },
    }


def _fingerprint(data: dict) -> str:
    return hashlib.md5(json.dumps(data, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


@router.get("/realtime-data/stream")
async def realtime_data_stream(
    range: str = Query("24h", pattern="^(24h|7d)$"),
):
    """SSE: 测试界面 realtime_data 实时推送"""

    async def event_generator():
        seen = None
        while True:
            db = MachineSessionLocal()
            try:
                now = datetime.now()
                since = now - timedelta(days=7) if range == "7d" else now - timedelta(hours=24)
                group_by_hour = range == "7d"

                labels, act_position, set_position, speed = _query_pivoted(db, since, group_by_hour)
                latest_time = _get_latest_source_time(db)
                latest_values = _get_latest_values(db)

                data = {
                    "labels": labels,
                    "actPosition": act_position,
                    "setPosition": set_position,
                    "speed": speed,
                    "latestTime": latest_time,
                    "latestValues": latest_values,
                }
                fp = _fingerprint(data)
                if fp != seen:
                    yield f"data: {json.dumps(data, ensure_ascii=False)}\n\n"
                    seen = fp
            finally:
                db.close()
            await asyncio.sleep(2)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
