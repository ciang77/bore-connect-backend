from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Index,
)
from sqlalchemy.orm import relationship

from app.database.connection import Base


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=False, comment="设备名称")
    model = Column(String(32), nullable=False, comment="设备型号")
    status = Column(
        Enum("online", "warning", "stopped"),
        nullable=False,
        default="online",
        comment="设备状态",
    )
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class DeviceRealtime(Base):
    __tablename__ = "device_realtime"

    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)
    runtime = Column(Float, default=0, comment="运行时长(h)")
    pressure = Column(Float, default=0, comment="系统压力(MPa)")
    spindle_speed = Column(Integer, default=0, comment="主轴转速(RPM)")
    recorded_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    device = relationship("Device")


class Subsystem(Base):
    __tablename__ = "subsystems"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32), nullable=False, comment="子系统名称")
    name_en = Column(String(32), nullable=False, comment="英文标识")
    status = Column(
        Enum("normal", "warning", "fault"),
        nullable=False,
        default="normal",
        comment="运行状态",
    )
    health_score = Column(Integer, default=100, comment="健康评分(0-100)")
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class SubsystemRealtime(Base):
    __tablename__ = "subsystem_realtime"

    id = Column(Integer, primary_key=True, autoincrement=True)
    subsystem_id = Column(Integer, ForeignKey("subsystems.id"), nullable=False)
    label = Column(String(32), nullable=False, comment="指标名称")
    value = Column(Float, default=0, comment="数值")
    unit = Column(String(16), default="", comment="单位")
    recorded_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    subsystem = relationship("Subsystem")


class Motor(Base):
    __tablename__ = "motors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    motor_code = Column(String(16), unique=True, nullable=False, comment="电机编号")
    name = Column(String(32), nullable=False, comment="电机名称")
    type = Column(
        Enum("main", "X", "Y", "Z", "W", "C"),
        nullable=False,
        comment="电机类型",
    )
    health = Column(Integer, default=100, comment="健康度(0-100)")
    status = Column(
        Enum("running", "idle", "warning", "error"),
        nullable=False,
        default="running",
        comment="运行状态",
    )
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class Alarm(Base):
    __tablename__ = "alarms"

    id = Column(Integer, primary_key=True, autoincrement=True)
    alarm_time = Column(DateTime, default=datetime.now, comment="报警时间")
    level = Column(
        Enum("info", "warning", "error"),
        nullable=False,
        comment="报警级别",
    )
    subsystem = Column(String(32), nullable=False, comment="所属子系统")
    msg = Column(String(256), nullable=False, comment="报警消息")
    created_at = Column(DateTime, default=datetime.now)

    __table_args__ = (
        Index("idx_alarm_time", "alarm_time"),
        Index("idx_level", "level"),
    )


class AlarmTypeStat(Base):
    __tablename__ = "alarm_type_stats"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32), nullable=False, comment="报警类型名称")
    value = Column(Integer, default=0, comment="数量")
    alarm_level = Column(
        Enum("high", "medium", "low"),
        nullable=False,
        comment="优先级",
    )
    stat_date = Column(Date, nullable=False, comment="统计日期")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class RuntimeStat(Base):
    __tablename__ = "runtime_stats"

    id = Column(Integer, primary_key=True, autoincrement=True)
    period_type = Column(
        Enum("daily", "monthly", "yearly"),
        nullable=False,
        comment="统计周期",
    )
    period_date = Column(Date, nullable=False, comment="统计日期")
    runtime = Column(Float, default=0, comment="运行时长(h)")
    anomaly_count = Column(Integer, default=0, comment="异常次数")
    anomaly_duration = Column(Float, default=0, comment="异常时长(h)")
    normal_rate = Column(Float, default=100, comment="正常运行率(%)")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class TrendData(Base):
    __tablename__ = "trend_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    record_time = Column(DateTime, nullable=False, comment="记录时间")
    servo_current = Column(Float, default=0, comment="伺服电流(A)")
    vibration = Column(Float, default=0, comment="振动(mm/s)")
    temperature = Column(Float, default=0, comment="温度(°C)")

    __table_args__ = (Index("idx_record_time", "record_time"),)


class MotorCurrent(Base):
    __tablename__ = "motor_currents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    motor_id = Column(String(8), nullable=False, comment="电机编号")
    current = Column(Float, default=0, comment="电流值(A)")
    min_current = Column(Float, default=3, comment="最小电流(A)")
    max_current = Column(Float, default=15, comment="最大电流(A)")


class SubsystemStatus(Base):
    __tablename__ = "subsystem_status"

    id = Column(Integer, primary_key=True, autoincrement=True)
    subsystem_name = Column(String(32), nullable=False, comment="所属子系统")
    label = Column(String(32), nullable=False, comment="状态名称")
    value = Column(Integer, default=1, comment="0=异常(红) 1=正常(绿)")
