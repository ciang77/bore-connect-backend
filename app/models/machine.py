from sqlalchemy import Column, Integer, Float, DateTime, String

from app.database.machine_connection import MachineBase


class RealtimeData(MachineBase):
    """machine.realtime_data — 最新实时值（唯一约束: device_id + tag_code）"""

    __tablename__ = "realtime_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(String(64), default="")
    tag_code = Column(String(128), default="")
    value_num = Column(Float, default=0)
    update_time = Column(DateTime, nullable=False)


class HistoryData(MachineBase):
    """machine.history_data — 历史时序数据（无唯一约束，可累积）"""

    __tablename__ = "history_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(String(64), default="")
    tag_code = Column(String(128), default="")
    value_num = Column(Float, default=0)
    source_time = Column(DateTime, nullable=False)
