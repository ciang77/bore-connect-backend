"""
趋势数据模拟器 — 每 30 秒写入一条模拟数据，保证 24h 和 7d 趋势图都有数据。
"""
import logging
import random
import threading
import time
from datetime import datetime

from app.database.connection import SessionLocal
from app.models.overview import TrendData

logger = logging.getLogger(__name__)

_stop_event = threading.Event()
_thread: threading.Thread | None = None


def _insert_sample():
    """写入一条模拟趋势数据"""
    db = SessionLocal()
    try:
        sample = TrendData(
            record_time=datetime.now(),
            servo_current=round(random.uniform(8.0, 16.0), 2),
            vibration=round(random.uniform(0.5, 5.0), 2),
            temperature=round(random.uniform(40.0, 65.0), 1),
        )
        db.add(sample)
        db.commit()
    except Exception as e:
        db.rollback()
        logger.warning(f"趋势数据写入失败: {e}")
    finally:
        db.close()


def _run_loop(interval: int):
    """后台循环"""
    logger.info(f"趋势数据模拟器已启动，每 {interval}s 写入一条")
    # 立即写入第一条，让图表立刻有数据
    _insert_sample()
    while not _stop_event.wait(interval):
        _insert_sample()


def start_trend_simulator(interval: int = 30):
    """启动趋势数据模拟器（后台线程）"""
    global _thread
    if _thread and _thread.is_alive():
        return
    _stop_event.clear()
    _thread = threading.Thread(target=_run_loop, args=(interval,), daemon=True)
    _thread.start()
