import logging
from django.conf import settings
from .sendgrid_service import send_email

logger = logging.getLogger(__name__)


def send_booking_emails(booking):
    logger.error("📧 Sending booking emails using SendGrid API")

    # USER EMAIL
    user_body = (
        f"Hello {booking.name},\n\n"
        "Thank you for booking with Singing Bowl & Gong House.\n\n"
        f"Service: {booking.service}\n"
        f"Date: {booking.booking_date}\n\n"
        "We will contact you shortly.\n\n"
        "Warm regards,\n"
        "Singing Bowl & Gong House"
    )

    user_sent = send_email(
        to_email=booking.email,
        subject="Your Booking Confirmation",
        content=user_body,
    )

    # ADMIN EMAIL
    admin_body = (
        "New booking received:\n\n"
        f"Name: {booking.name}\n"
        f"Email: {booking.email}\n"
        f"Phone: {booking.phone}\n"
        f"Service: {booking.service}\n"
        f"Date: {booking.booking_date}\n"
    )

    admin_sent = send_email(
        to_email=settings.ADMIN_EMAIL,
        subject="New Booking Received",
        content=admin_body,
    )

    logger.error(
        f"📬 SendGrid results → user={user_sent}, admin={admin_sent}"
    )

    return user_sent, admin_sent
