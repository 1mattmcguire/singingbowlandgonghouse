"""
Clean, production-safe email service for booking confirmations.
Uses Django's built-in SMTP backend with environment variable configuration.
"""

from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def send_booking_confirmation_email(booking):
    """Send confirmation email to the user."""
    try:
        subject = "Booking Confirmation - Singing Bowl & Gong House"

        message = f"""Dear {booking.name},

Thank you for your booking with Singing Bowl & Gong House.

Booking Details:
- Service: {booking.get_service_display()}
- Date: {booking.booking_date}
- Session Type: {booking.session_type or 'N/A'}

We will contact you within 24 hours to confirm your booking.

Best regards,
Singing Bowl & Gong House
"""

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[booking.email],
            fail_silently=False,
        )

        logger.info(f"User confirmation email sent to {booking.email}")
        return True

    except Exception as e:
        logger.error(
            f"Failed to send user confirmation email "
            f"(booking #{booking.id}, {booking.email}): {str(e)}"
        )
        return False   # ❗ DO NOT raise


def send_booking_notification_email(booking):
    """Send admin notification email."""
    try:
        subject = f"New Booking Received - {booking.name}"

        message = f"""New booking received:

Name: {booking.name}
Email: {booking.email}
Phone: {booking.phone}
Service: {booking.get_service_display()}
Date: {booking.booking_date}
Age: {booking.age or 'N/A'}
Session Type: {booking.session_type or 'N/A'}
Course: {booking.course_selection or 'N/A'}
Medical Condition: {booking.medical_condition or 'None provided'}
Message: {booking.message or 'None'}

Created at: {booking.created_at}
"""

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
            fail_silently=False,
        )

        logger.info(f"Admin notification email sent to {settings.ADMIN_EMAIL}")
        return True

    except Exception as e:
        logger.error(
            f"Failed to send admin notification email "
            f"(booking #{booking.id}, admin={settings.ADMIN_EMAIL}): {str(e)}"
        )
        return False   # ❗ DO NOT raise


def send_booking_emails(booking):
    """
    Send both confirmation (user) and notification (admin) emails.

    Returns:
        (user_sent, admin_sent)
    """
    user_sent = send_booking_confirmation_email(booking)
    admin_sent = send_booking_notification_email(booking)

    logger.info(
        f"Booking #{booking.id} email summary → "
        f"user_sent={user_sent}, admin_sent={admin_sent}"
    )

    return user_sent, admin_sent

