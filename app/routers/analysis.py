import asyncio
import hashlib
import json
import random
from collections import defaultdict

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal, get_db
from app.models.overview import MotorCurrent

router = APIRouter(prefix="/api/analysis", tags=["Analysis"])


@router.get("/motor-currents")
def get_motor_currents(db: Session = Depends(get_db)):
    rows = db.query(MotorCurrent).all()

    # 按 motor_id 分组，每组随机取一条
    grouped: dict[str, list[MotorCurrent]] = defaultdict(list)
    for r in rows:
        grouped[r.motor_id].append(r)

    data = []
    for motor_id in sorted(grouped.keys()):
        picked = random.choice(grouped[motor_id])
        data.append({
            "id": motor_id,
            "current": round(picked.current, 1),
            "minCurrent": picked.min_current,
            "maxCurrent": picked.max_current,
        })

    return {"code": 0, "data": data}


@router.get("/motor-currents/stream")
async def motor_currents_stream():
    """SSE: 电机电流实时推送"""

    async def event_generator():
        seen = None
        while True:
            db = SessionLocal()
            try:
                rows = db.query(MotorCurrent).all()

                grouped: dict[str, list[MotorCurrent]] = defaultdict(list)
                for r in rows:
                    grouped[r.motor_id].append(r)

                data = []
                for motor_id in sorted(grouped.keys()):
                    picked = random.choice(grouped[motor_id])
                    data.append({
                        "id": motor_id,
                        "current": round(picked.current, 1),
                        "minCurrent": picked.min_current,
                        "maxCurrent": picked.max_current,
                    })

                fp = hashlib.md5(json.dumps(data, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
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
