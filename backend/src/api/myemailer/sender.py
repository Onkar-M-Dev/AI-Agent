import os
import smtplib
from email.message import EmailMessage
import logging

logger = logging.getLogger(__name__)

EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
EMAIL_HOST = os.environ.get("EMAIL_HOST") or "smtp.gmail.com"
EMAIL_PORT = os.environ.get("EMAIL_PORT") or 465


def send_mail(
    subject: str = "No subject provided!",
    content: str = "No message provided!",
    to_email: str = None,   # ✅ FIXED
    from_email: str = EMAIL_ADDRESS
):
    if not to_email:
        raise ValueError("Recipient email is required")

    logger.info("Send mail tool executed")
    logger.info(f"Recipient: {to_email}")

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email
    msg.set_content(content)

    try:
        with smtplib.SMTP_SSL(EMAIL_HOST, int(EMAIL_PORT)) as smtp:
            logger.info("Attempting SMTP login...")

            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

            logger.info("SMTP login successful")

            smtp.send_message(msg)

            logger.info("Email sent successfully")

    except Exception as e:
        logger.error(f"SMTP ERROR: {e}")
        raise