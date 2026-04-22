import os
import smtplib
from email.message import EmailMessage


EMAIL_ADDRESS=os.environ.get("EMAIL_ADDRESS")
EMAIL_PASSWORD=os.environ.get("EMAIL_PASSWORD")
EMAIL_HOST=os.environ.get("EMAIL_HOST") or "smtp.gmail.com"
EMAIL_PORT=os.environ.get("EMAIL_PORT")  or 465


def send_mail(
    subject: str = "No subject provided !",
    content: str = "No message provided !",
    to_email: str = EMAIL_ADDRESS,
    from_email: str = EMAIL_ADDRESS
):
    print("SEND_MAIL TOOL EXECUTED")
    print(f"Recipient: {to_email}")

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email
    msg.set_content(content)

    try:
        with smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT) as smtp:

            print("Attempting SMTP login...")

            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

            print("SMTP LOGIN SUCCESS")

            smtp.send_message(msg)

            print("EMAIL SENT SUCCESS")

    except Exception as e:
        print("SMTP ERROR:", e)
        raise
    