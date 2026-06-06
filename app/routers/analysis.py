import random
from collections import defaultdict

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
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
