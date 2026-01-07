from django.conf import settings
from .sendgrid_service import send_email


def val(x):
    return x if x else "Not provided"


def build_admin_email(booking):

    return f"""
    <h2>📥 New Booking Received</h2>

    <b>Name:</b> {val(booking.name)}<br>
    <b>Email:</b> {val(booking.email)}<br>
    <b>Phone:</b> {val(booking.phone)}<br>

    <hr>

    <b>Service:</b> {val(booking.service)}<br>
    <b>Session Type:</b> {val(booking.session_type)}<br>
    <b>Course Selected:</b> {val(booking.course_selection)}<br>
    <b>Preferred Date:</b> {val(booking.booking_date)}<br>
    <b>Age:</b> {val(booking.age)}<br>

    <hr>

    <b>Medical Condition:</b><br>
    {val(booking.medical_condition)}<br><br>

    <b>Message:</b><br>
    {val(booking.message)}

    <br><br>
    <small>Sent automatically from Singing Bowl & Gong House website</small>
    """


def build_user_email(booking):

    return f"""
    <h2>✅ Booking Confirmed</h2>

    Hi {booking.name},<br><br>

    Thank you for booking with Singing Bowl & Gong House.<br>
    Here are your booking details:

    <hr>

    <b>Service:</b> {val(booking.service)}<br>
    <b>Session Type:</b> {val(booking.session_type)}<br>
    <b>Course:</b> {val(booking.course_selection)}<br>
    <b>Date:</b> {val(booking.booking_date)}<br>

    <hr>

    We will contact you shortly.

    <br><br>
    Warm regards,<br>
    Singing Bowl & Gong House
    """


def send_booking_emails(booking):

    # Admin email
    admin_body = build_admin_email(booking)

    send_email(
        subject="📥 New Booking Received",
        html_content=admin_body,
        to_email=settings.ADMIN_EMAIL,
    )

    # User email
    user_body = build_user_email(booking)

    send_email(
        subject="Your Booking Confirmation",
        html_content=user_body,
        to_email=booking.email,
    )
