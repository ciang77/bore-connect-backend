"""
Machine 数据库数据模拟器 — 每 1 秒写入一组模拟数据：
- realtime_data: UPSERT 覆盖（保持每个 tag 只有最新一条）
- history_data: INSERT 追加（累积历史数据）

为 axis_x_actPosition / axis_x_setPosition / axis_x_speed 三个点位生成正弦波数据。
"""
import logging
import math
import random
import threading
from datetime import datetime

from sqlalchemy import text

from app.database.machine_connection import MachineSessionLocal

logger = logging.getLogger(__name__)

_machine_stop = threading.Event()
_machine_thread: threading.Thread | None = None

_angle = 0.0

UPSERT_SQL = text("""
    INSERT INTO realtime_data (device_id, tag_code, value_num, update_time)
    VALUES (:device_id, :tag_code, :value_num, :update_time)
    ON DUPLICATE KEY UPDATE value_num = VALUES(value_num), update_time = VALUES(update_time)
""")


def _insert_samples():
    """写入三个点位：realtime_data 覆盖 + history_data 追加"""
    global _angle
    db = MachineSessionLocal()
    try:
        now = datetime.now()
        _angle += 0.05
        base_pos = 10.0 + math.sin(_angle) * 2.0
        set_pos = 10.0 + math.sin(_angle - 0.1) * 1.8
        speed_val = math.cos(_angle) * 1.2 + random.uniform(-0.05, 0.05)

        tags = [
            ("axis_x_actPosition", round(base_pos, 4)),
            ("axis_x_setPosition", round(set_pos, 4)),
            ("axis_x_speed", round(speed_val, 4)),
        ]
        for code, val in tags:
            # 1. UPSERT 到 realtime_data（覆盖最新值）
            db.execute(UPSERT_SQL, {
                "device_id": "01",
                "tag_code": code,
                "value_num": val,
                "update_time": now,
            })
            # 2. INSERT 到 history_data（追加历史）
            db.execute(
                text("INSERT INTO history_data (device_id, tag_code, value_num, source_time) "
                     "VALUES (:device_id, :tag_code, :value_num, :source_time)"),
                {
                    "device_id": "01",
                    "tag_code": code,
                    "value_num": val,
                    "source_time": now,
                },
            )
        db.commit()
    except Exception as e:
        db.rollback()
        logger.warning(f"Machine 数据写入失败: {e}")
    finally:
        db.close()


def _run_loop(interval: float):
    logger.info(f"Machine 数据模拟器已启动，每 {interval}s 写入一组（realtime_data 覆盖 + history_data 追加）")
    _insert_samples()
    while not _machine_stop.wait(interval):
        _insert_samples()


def start_machine_simulator(interval: float = 1.0):
    global _machine_thread
    if _machine_thread and _machine_thread.is_alive():
        return
    _machine_stop.clear()
    _machine_thread = threading.Thread(target=_run_loop, args=(interval,), daemon=True)
    _machine_thread.start()
