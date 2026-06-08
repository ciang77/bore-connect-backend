import logging
import smtplib
import threading
import time
import hashlib
import json
import urllib.request
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from sqlalchemy import text

from app.config.settings import settings
from app.database.connection import SessionLocal, engine
from app.models.overview import Alarm

logger = logging.getLogger(__name__)

_DEDUP_INTERVAL = timedelta(minutes=5)  # 同一内容 5 分钟内只发一次
_DEFAULT_ALERT_ENABLED = False


# ═══════════════════════════════════════════════════════════════
#  DB settings 表：跨 worker 共享状态
#  字段: key (PK), value
#  用法:
#    alert_enabled     → "1" / "0"
#    last_check_time   → "2026-06-07 15:30:00"
#    dedup:{key}       → "2026-06-07 15:30:00"
# ═══════════════════════════════════════════════════════════════

def _ensure_settings_table():
    with engine.begin() as conn:
        conn.execute(text(
            "CREATE TABLE IF NOT EXISTS settings ("
            "  `key` VARCHAR(128) PRIMARY KEY,"
            "  `value` VARCHAR(255) NOT NULL"
            ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4"
        ))


def _db_get(key: str) -> str | None:
    """读取 settings 值"""
    _ensure_settings_table()
    db = SessionLocal()
    try:
        row = db.execute(
            text("SELECT `value` FROM settings WHERE `key` = :k"), {"k": key}
        ).fetchone()
        return row[0] if row else None
    finally:
        db.close()


def _db_set(key: str, value: str):
    """写入 settings 值"""
    _ensure_settings_table()
    db = SessionLocal()
    try:
        db.execute(
            text("INSERT INTO settings (`key`, `value`) VALUES (:k, :v) "
                 "ON DUPLICATE KEY UPDATE `value` = :v"),
            {"k": key, "v": value},
        )
        db.commit()
    finally:
        db.close()


def _db_delete(key: str):
    """删除 settings 值"""
    db = SessionLocal()
    try:
        db.execute(text("DELETE FROM settings WHERE `key` = :k"), {"k": key})
        db.commit()
    finally:
        db.close()


def _format_dt(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M:%S.%f")


def _parse_dt(value: str | None) -> datetime | None:
    if not value:
        return None
    for fmt in ("%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    return None


# ═══════════════════════════════════════════════════════════════
#  报警开关
# ═══════════════════════════════════════════════════════════════

def is_alert_enabled() -> bool:
    value = _db_get("alert_enabled")
    if value in {"0", "1"}:
        return value == "1"

    default_value = "1" if _DEFAULT_ALERT_ENABLED else "0"
    _db_set("alert_enabled", default_value)
    logger.info("实时报警开关未初始化，已设置默认值: %s", "开启" if _DEFAULT_ALERT_ENABLED else "关闭")
    return _DEFAULT_ALERT_ENABLED


def set_alert_enabled(enabled: bool):
    if enabled:
        # 重置时间基准，只推送开关之后的告警
        _db_set("last_check_time", _format_dt(datetime.now()))
    _db_set("alert_enabled", "1" if enabled else "0")
    logger.info("实时报警开关已%s", "开启" if enabled else "关闭")


# ═══════════════════════════════════════════════════════════════
#  邮件发送
# ═══════════════════════════════════════════════════════════════

def send_alert_email(subject: str, body: str) -> bool:
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
                此邮件由 Bore Connect 设备监控系统自动发送 · {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
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


# ═══════════════════════════════════════════════════════════════
#  企业微信群机器人推送
# ═══════════════════════════════════════════════════════════════

def send_wecom_markdown(content: str) -> bool:
    """通过企业微信群机器人发送 markdown 消息"""
    webhook_url = settings.WECOM_WEBHOOK_URL
    if not webhook_url:
        logger.warning("企业微信 Webhook 未配置，跳过推送")
        return False

    payload = {
        "msgtype": "markdown",
        "markdown": {
            "content": content
        }
    }

    try:
        req = urllib.request.Request(
            webhook_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            if result.get("errcode") == 0:
                logger.info("企业微信推送成功")
                return True
            else:
                logger.error("企业微信推送失败: %s", result)
                return False
    except Exception as e:
        logger.error("企业微信推送异常: %s", e)
        return False


# ═══════════════════════════════════════════════════════════════
#  去重（基于 DB，跨 worker 共享）
# ═══════════════════════════════════════════════════════════════

def _build_dedup_key(*parts: str) -> str:
    raw = "||".join(part.strip() for part in parts if part)
    digest = hashlib.sha1(raw.encode("utf-8")).hexdigest()
    return f"dedup:{digest}"


def _should_send(*parts: str) -> bool:
    """同一内容在 _DEDUP_INTERVAL 内只发送一次"""
    key = _build_dedup_key(*parts)
    now = datetime.now()
    last_str = _db_get(key)
    last = _parse_dt(last_str)
    if last and (now - last) < _DEDUP_INTERVAL:
        return False
    _db_set(key, _format_dt(now))
    return True


def _build_section_html(title: str, rows: list[tuple[str, str]], accent: str) -> str:
    if not rows:
        return ""

    items_html = "".join(
        f"""
        <tr>
            <td style="padding:8px 0; color: #888; width:110px; vertical-align: top;">{label}</td>
            <td style="padding:8px 0; color: #fff;">{value}</td>
        </tr>
        """
        for label, value in rows
    )
    return f"""
    <div style="margin-top: 18px; border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; overflow: hidden;">
        <div style="padding: 10px 14px; background: {accent}; color: #fff; font-weight: bold;">
            {title}
        </div>
        <div style="padding: 12px 16px;">
            <table style="width:100%; border-collapse: collapse; color: #e0e0e0;">
                {items_html}
            </table>
        </div>
    </div>
    """


# ═══════════════════════════════════════════════════════════════
#  核心扫描（MySQL 命名锁保证单 worker 执行）
# ═══════════════════════════════════════════════════════════════

def check_and_alert():
    """扫描数据库中的重大故障，新发现的发送邮件告警"""

    if not is_alert_enabled():
        return

    db = SessionLocal()
    try:
        # ── 尝试获取分布式锁，避免多 worker 重复执行 ──
        locked = db.execute(text("SELECT GET_LOCK('alert_check', 0)")).scalar()
        if not locked:
            return  # 别的 worker 正在执行，本轮跳过

        # ── 读取上次检查时间 ──
        last_str = _db_get("last_check_time")
        last_check = _parse_dt(last_str) or datetime.now()
        now = datetime.now()
        error_sections: list[str] = []

        # ── 1. 新的 error 级报警 ──
        new_errors = (
            db.query(Alarm)
            .filter(Alarm.level == "error", Alarm.alarm_time > last_check)
            .all()
        )
        for alarm in new_errors:
            if not _should_send("alarm", alarm.level, alarm.subsystem, alarm.msg):
                continue
            error_sections.append(_build_section_html(
                f"严重报警 · {alarm.subsystem}",
                [
                    ("故障时间", alarm.alarm_time.strftime('%Y-%m-%d %H:%M:%S')),
                    ("故障级别", "严重 error"),
                    ("所属子系统", alarm.subsystem),
                    ("故障描述", alarm.msg),
                ],
                "linear-gradient(90deg, #ff4757, #ff6b81)",
            ))

        if error_sections:
            summary = f"严重报警 {len(error_sections)} 项"
            body = f"""
            <div style="color: #e0e0e0;">
                <p style="margin: 0 0 12px; color: #fff; font-size: 15px; font-weight: bold;">
                    本轮扫描检测到新的 error 级别报警，请及时处理。
                </p>
                <p style="margin: 0 0 16px; color: #ffb3c1;">
                    汇总：{summary}
                </p>
                {''.join(error_sections)}
                <p style="margin-top: 18px; color: #ff6b81; font-weight: bold;">
                    ⚡ 此邮件为本轮汇总告警邮件，同内容 5 分钟内不会重复发送。
                </p>
            </div>
            """
            send_alert_email("[Bore Connect] Error 级别告警汇总", body)

            # ── 企业微信推送（markdown 格式） ──
            wecom_lines = [
                f"## ⚠️ Bore Connect 严重告警\n",
                f"> 本轮扫描检测到 **{summary}**，请及时处理\n",
            ]
            for alarm in new_errors:
                wecom_lines.append(
                    f"- **{alarm.subsystem}** | {alarm.msg}\n"
                    f"  故障时间: {alarm.alarm_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
                )
            wecom_lines.append(f"\n> 同内容 5 分钟内不会重复发送")
            send_wecom_markdown("".join(wecom_lines))

        # ── 更新检查时间 ──
        _db_set("last_check_time", _format_dt(now))

    finally:
        db.execute(text("DO RELEASE_LOCK('alert_check')"))
        db.close()


# ═══════════════════════════════════════════════════════════════
#  后台线程
# ═══════════════════════════════════════════════════════════════

def _alert_loop(interval: int = 30):
    logger.info("告警监控线程已启动，扫描间隔 %d 秒", interval)
    while True:
        time.sleep(interval)
        try:
            check_and_alert()
        except Exception as e:
            logger.error("告警检查异常: %s", e)


def start_alert_monitor(interval: int = 30):
    # 每次后端启动时刷新 last_check_time，避免发送重启前的历史告警
    _db_set("last_check_time", _format_dt(datetime.now()))
    logger.info("告警时间基准已重置为当前时间")
    t = threading.Thread(target=_alert_loop, args=(interval,), daemon=True)
    t.start()
