import os
import logging
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

logger = logging.getLogger(__name__)


def send_email(to_email, subject, content):
    """
    Send email using SendGrid API (NOT SMTP)
    """
    try:
        message = Mail(
            from_email=os.getenv("DEFAULT_FROM_EMAIL"),
            to_emails=to_email,
            subject=subject,
            plain_text_content=content,
        )

        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        response = sg.send(message)

        logger.error(
            f"✅ SendGrid API email sent to {to_email} | status={response.status_code}"
        )
        return True

    except Exception:
        logger.exception("❌ SendGrid API email failed")
        return False
