import logging
import smtplib
import threading
import time
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.config.settings import settings
from app.database.connection import SessionLocal
from app.models.overview import Alarm, Subsystem, Motor

logger = logging.getLogger(__name__)

# ── 全局状态 ──
alert_enabled = False          # 实时报警开关（前端按钮控制）
_last_check_time = datetime.now()

# 同类型去重缓存：{(level, subsystem) → 上次发送时间}
_dedup_cache: dict[tuple, datetime] = {}
_DEDUP_INTERVAL = timedelta(minutes=1)   # 同一类型 1 分钟内只发一次


def is_alert_enabled() -> bool:
    return alert_enabled


def set_alert_enabled(enabled: bool):
    global alert_enabled
    alert_enabled = enabled
    logger.info("实时报警开关已%s", "开启" if enabled else "关闭")


def send_alert_email(subject: str, body: str) -> bool:
    """发送告警邮件，返回是否成功"""
    if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
        logger.warning("SMTP 未配置，跳过邮件发送")
        return False

    try:
        msg = MIMEMultipart("alternative")
        msg["From"] = settings.SMTP_USER
        msg["To"] = settings.ALERT_EMAIL_TO
        msg["Subject"] = subject

        html_body = f"""
        <div style="font-family: 'Microsoft YaHei', Arial, sans-serif; max-width: 600px;
                    background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
                    border: 2px solid #ff4757; border-radius: 8px; overflow: hidden;">
            <div style="background: linear-gradient(90deg, #ff4757, #ff6b81); padding: 16px 20px;">
                <h2 style="color: #fff; margin: 0; font-size: 18px;">⚠ Bore Connect 重大故障告警</h2>
            </div>
            <div style="padding: 20px; color: #e0e0e0;">
                {body}
            </div>
            <div style="background: rgba(255,71,87,0.08); padding: 12px 20px;
                        border-top: 1px solid rgba(255,71,87,0.2); font-size: 12px; color: #888;">
                此邮件由 Bore Connect 设备监控系统自动发送 · {_now_str()}
            </div>
        </div>
        """

        msg.attach(MIMEText(html_body, "html", "utf-8"))

        server = smtplib.SMTP_SSL(settings.SMTP_SERVER, settings.SMTP_PORT, timeout=10)
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.sendmail(settings.SMTP_USER, settings.ALERT_EMAIL_TO.split(","), msg.as_string())
        server.quit()

        logger.info("告警邮件发送成功: %s", subject)
        return True
    except Exception as e:
        logger.error("邮件发送失败: %s", e)
        return False


def _now_str() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _should_send(level: str, subsystem: str) -> bool:
    """检查是否应该发送：同类型 1 分钟内只发一次"""
    key = (level, subsystem)
    now = datetime.now()
    last = _dedup_cache.get(key)
    if last and (now - last) < _DEDUP_INTERVAL:
        logger.debug("去重跳过: level=%s subsystem=%s (上次发送: %s)", level, subsystem, last.strftime("%H:%M:%S"))
        return False
    _dedup_cache[key] = now
    return True


def check_and_alert():
    """扫描数据库中的重大故障，新发现的发送邮件告警"""
    global _last_check_time

    if not alert_enabled:
        return   # 开关未开启，不发送

    db = SessionLocal()
    try:
        # ── 1. 新的 error 级报警 ──
        new_errors = (
            db.query(Alarm)
            .filter(
                Alarm.level == "error",
                Alarm.created_at >= _last_check_time,
            )
            .all()
        )
        for alarm in new_errors:
            if not _should_send(alarm.level, alarm.subsystem):
                continue
            body = f"""
            <table style="width:100%; border-collapse: collapse; color: #e0e0e0;">
                <tr><td style="padding:8px 0; color: #888; width:80px;">故障时间</td>
                    <td style="padding:8px 0; color: #fff;">{alarm.alarm_time.strftime('%Y-%m-%d %H:%M:%S')}</td></tr>
                <tr><td style="padding:8px 0; color: #888;">故障级别</td>
                    <td style="padding:8px 0; color: #ff4757; font-weight: bold;">严重 error</td></tr>
                <tr><td style="padding:8px 0; color: #888;">所属子系统</td>
                    <td style="padding:8px 0; color: #fff;">{alarm.subsystem}</td></tr>
                <tr><td style="padding:8px 0; color: #888;">故障描述</td>
                    <td style="padding:8px 0; color: #ff6b81;">{alarm.msg}</td></tr>
            </table>
            <p style="margin-top: 16px; color: #ff6b81; font-weight: bold;">
                ⚡ 请立即排查处理！
            </p>
            """
            send_alert_email(f"[Bore Connect] 重大故障 - {alarm.subsystem}", body)

        # ── 2. 子系统状态变为 fault ──
        fault_subs = (
            db.query(Subsystem)
            .filter(
                Subsystem.status == "fault",
                Subsystem.updated_at >= _last_check_time,
            )
            .all()
        )
        for sub in fault_subs:
            if not _should_send("fault", sub.name):
                continue
            body = f"""
            <table style="width:100%; border-collapse: collapse; color: #e0e0e0;">
                <tr><td style="padding:8px 0; color: #888; width:80px;">故障系统</td>
                    <td style="padding:8px 0; color: #ff4757; font-weight: bold;">{sub.name}</td></tr>
                <tr><td style="padding:8px 0; color: #888;">当前健康度</td>
                    <td style="padding:8px 0; color: #ff6b81;">{sub.health_score}%</td></tr>
            </table>
            <p style="margin-top: 16px; color: #ff6b81; font-weight: bold;">
                ⚡ 子系统已标记为故障状态，请立即排查！
            </p>
            """
            send_alert_email(f"[Bore Connect] 子系统故障 - {sub.name}", body)

        # ── 3. 电机状态异常 ──
        error_motors = (
            db.query(Motor)
            .filter(
                Motor.status == "error",
                Motor.updated_at >= _last_check_time,
            )
            .all()
        )
        for motor in error_motors:
            if not _should_send(motor.status, motor.name):
                continue
            body = f"""
            <table style="width:100%; border-collapse: collapse; color: #e0e0e0;">
                <tr><td style="padding:8px 0; color: #888; width:80px;">电机编号</td>
                    <td style="padding:8px 0; color: #fff;">{motor.motor_code}</td></tr>
                <tr><td style="padding:8px 0; color: #888;">电机名称</td>
                    <td style="padding:8px 0; color: #fff;">{motor.name}</td></tr>
                <tr><td style="padding:8px 0; color: #888;">当前状态</td>
                    <td style="padding:8px 0; color: #ff4757; font-weight: bold;">{motor.status}</td></tr>
                <tr><td style="padding:8px 0; color: #888;">健康度</td>
                    <td style="padding:8px 0; color: #ff6b81;">{motor.health}%</td></tr>
            </table>
            <p style="margin-top: 16px; color: #ff6b81; font-weight: bold;">
                ⚡ 电机异常，请检查！
            </p>
            """
            send_alert_email(f"[Bore Connect] 电机异常 - {motor.name}", body)

    finally:
        db.close()

    _last_check_time = datetime.now()


def _alert_loop(interval: int = 30):
    """后台线程：每隔 interval 秒扫描一次"""
    logger.info("告警监控线程已启动，扫描间隔 %d 秒", interval)
    while True:
        time.sleep(interval)
        try:
            check_and_alert()
        except Exception as e:
            logger.error("告警检查异常: %s", e)


def start_alert_monitor(interval: int = 30):
    """启动后台告警监控线程"""
    t = threading.Thread(target=_alert_loop, args=(interval,), daemon=True)
    t.start()
