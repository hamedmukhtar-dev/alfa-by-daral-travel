import smtplib
from email.mime.text import MIMEText
from app.config import settings


def send_email(subject: str, body: str):
    if not all([
        settings.SMTP_HOST,
        settings.SMTP_USER,
        settings.SMTP_PASSWORD,
        settings.ALERT_EMAIL_TO,
    ]):
        # Pilot-safe: log only
        print("[EMAIL] Skipped (SMTP not configured)")
        return

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = settings.SMTP_USER
    msg["To"] = settings.ALERT_EMAIL_TO

    try:
        # ✅ Port 465 uses implicit SSL
        if settings.SMTP_PORT == 465:
            with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT, timeout=20) as server:
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.send_message(msg)
        else:
            # ✅ Port 587 uses STARTTLS
            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=20) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.send_message(msg)

        print("[EMAIL] Sent OK")

    except Exception as e:
        print(f"[EMAIL] Failed: {e}")
