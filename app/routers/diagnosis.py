import asyncio
import hashlib
import json
import random
from collections import defaultdict

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal, get_db
from app.models.overview import SubsystemStatus

router = APIRouter(prefix="/api/diagnosis", tags=["Diagnosis"])


@router.get("/status")
def get_subsystem_status(db: Session = Depends(get_db)):
    rows = db.query(SubsystemStatus).all()

    # 按 (subsystem_name, label) 分组，每组随机取一条
    grouped: dict[tuple[str, str], list[SubsystemStatus]] = defaultdict(list)
    for r in rows:
        grouped[(r.subsystem_name, r.label)].append(r)

    # 按子系统聚合
    result: dict[str, list[dict]] = defaultdict(list)
    for (sub_name, label), items in grouped.items():
        picked = random.choice(items)
        result[sub_name].append({
            "label": label,
            "value": picked.value,
        })

    data = [
        {"name": name, "variables": sorted(vars, key=lambda x: x["label"])}
        for name, vars in result.items()
    ]

    return {"code": 0, "data": data}


@router.get("/status/stream")
async def diagnosis_status_stream():
    """SSE: 诊断状态实时推送"""

    async def event_generator():
        seen = None
        while True:
            db = SessionLocal()
            try:
                rows = db.query(SubsystemStatus).all()

                grouped: dict[tuple[str, str], list[SubsystemStatus]] = defaultdict(list)
                for r in rows:
                    grouped[(r.subsystem_name, r.label)].append(r)

                result: dict[str, list[dict]] = defaultdict(list)
                for (sub_name, label), items in grouped.items():
                    picked = random.choice(items)
                    result[sub_name].append({
                        "label": label,
                        "value": picked.value,
                    })

                data = [
                    {"name": name, "variables": sorted(vars, key=lambda x: x["label"])}
                    for name, vars in result.items()
                ]

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
