from fastapi import APIRouter

router = APIRouter(
    prefix="/machine",
    tags=["Machine"]
)


@router.get("/status")
def get_machine_status():
    return {
        "machineName": "龙门镗铣床",
        "status": "running",
        "temperature": 42,
        "speed": 1200,
        "power": 78,
        "alarm": False
    }