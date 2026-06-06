import random
from collections import defaultdict

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
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
