from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages

from .forms import InquiryForm, BookingForm
from .models import Inquiry, Booking


# =========================
# PAGE VIEWS
# =========================

def home(request):
    return render(request, "main/home.html")


def about(request):
    return render(request, "main/about.html")


def services(request):
    return render(request, "main/services.html")


def courses(request):
    return render(request, "main/courses.html")


def smiles(request):
    return render(request, "main/smiles.html")


def success(request):
    return render(request, "main/success.html")


# =========================
# CONTACT
# =========================

def contact(request):
    if request.method == "POST":
        form = InquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save()

            # User email
            send_mail(
                subject="Thank you for contacting Singing Bowl & Gong House",
                message=f"""
Dear {inquiry.name},

Thank you for contacting Singing Bowl & Gong House.
We will get back to you within 24 hours.

Best regards,
Singing Bowl & Gong House
""",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[inquiry.email],
                fail_silently=False,
            )

            # Admin email
            send_mail(
                subject=f"New Inquiry from {inquiry.name}",
                message=f"""
Name: {inquiry.name}
Email: {inquiry.email}
Message:
{inquiry.message}
""",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=False,
            )

            messages.success(request, "Your inquiry has been sent successfully.")
            return redirect("main:success")
    else:
        form = InquiryForm()

    return render(request, "main/contact.html", {"form": form})


# =========================
# BOOKING
# =========================

def booking(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save()

            # User email
            send_mail(
                subject="Booking Confirmation",
                message="Thank you for your booking with Singing Bowl & Gong House.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[booking.email],
                fail_silently=False,
            )

            # Admin email
            send_mail(
                subject="New Booking Received",
                message=f"New booking from {booking.name}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=False,
            )

            messages.success(request, "Your booking has been submitted.")
            return redirect("main:success")
    else:
        form = BookingForm()

    return render(request, "main/booking.html", {"form": form})


# =========================
# API ENDPOINTS
# =========================

def api_booking(request):
    return JsonResponse({"status": "ok"})


def api_inquiry(request):
    return JsonResponse({"status": "ok"})


def test_email(request):
    send_mail(
        "Test Email",
        "This is a test email.",
        settings.DEFAULT_FROM_EMAIL,
        [settings.ADMIN_EMAIL],
        fail_silently=False,
    )
    return JsonResponse({"status": "email sent"})
