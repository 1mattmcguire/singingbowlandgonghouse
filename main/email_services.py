import logging
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)


def send_booking_emails(booking):
    """
    Sends booking confirmation email to user
    and notification email to admin.
    """

    user_sent = False
    admin_sent = False

    # -------------------
    # Email to USER
    # -------------------
    try:
        send_mail(
            subject="Your Booking Confirmation",
            message=(
                f"Hello {booking.name},\n\n"
                "Thank you for booking with Singing Bowl & Gong House.\n\n"
                f"Service: {booking.service}\n"
                f"Date: {booking.booking_date}\n\n"
                "We will contact you shortly.\n\n"
                "Warm regards,\n"
                "Singing Bowl & Gong House"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[booking.email],
            fail_silently=False,
        )
        user_sent = True
        logger.info(f"✅ Booking confirmation sent to user {booking.email}")
    except Exception as e:
        logger.exception("❌ Failed to send booking confirmation to user")

    # -------------------
    # Email to ADMIN
    # -------------------
    try:
        send_mail(
            subject="New Booking Received",
            message=(
                "New booking received:\n\n"
                f"Name: {booking.name}\n"
                f"Email: {booking.email}\n"
                f"Phone: {booking.phone}\n"
                f"Service: {booking.service}\n"
                f"Date: {booking.booking_date}\n"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
            fail_silently=False,
        )
        admin_sent = True
        logger.info("✅ Booking notification sent to admin")
    except Exception as e:
        logger.exception("❌ Failed to send booking notification to admin")

    return user_sent, admin_sent
