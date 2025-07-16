from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from temporalio import activity
import os

from dotenv import load_dotenv
load_dotenv()


@activity.defn
async def send_email(data: dict) -> str:
    try:
        payload = data.get("payload", {})
        to = payload.get("to")
        subject = payload.get("subject", "No subject")
        content = payload.get("content", "")

        if not to:
            raise ValueError("Missing 'to' address in payload")

        message = Mail(
            from_email="tanisha.anand.raaj@gmail.com",
            to_emails=to,
            subject=subject,
            plain_text_content=content,
        )

        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        response = sg.send(message)

        print(f"✅ Email sent: {response.status_code}")
        return "Email sent successfully ✅"

    except Exception as e:
        print("❌ Error in send_email activity:", str(e))
        raise
