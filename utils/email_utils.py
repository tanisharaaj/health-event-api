import sendgrid
from sendgrid.helpers.mail import Mail
import os

from dotenv import load_dotenv
load_dotenv()


def send_email(to_email, subject, content):
    sg = sendgrid.SendGridAPIClient(api_key=os.getenv("SENDGRID_API_KEY"))
    message = Mail(
        from_email="tanisha.anand.raaj@gmail.com",
        to_emails=to_email,
        subject=subject,
        html_content=content
    )
    try:
        response = sg.send(message)
        return response.status_code == 202
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False
