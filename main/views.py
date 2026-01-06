from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import json
import logging
from threading import Thread

from .forms import InquiryForm, BookingForm
from .models import Inquiry, Booking
from .email_service import send_booking_emails

logger = logging.getLogger(__name__)


# =========================
# ASYNC EMAIL HANDLER
# =========================

def send_emails_async(booking):
    try:
        send_booking_emails(booking)
    except Exception as e:
        logger.error(f"Async email failed for booking {booking.id}: {e}")


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
            form.save()
            messages.success(request, "Your inquiry has been sent successfully.")
            return redirect("main:success")
    else:
        form = InquiryForm()

    return render(request, "main/contact.html", {"form": form})


# =========================
# BOOKING (FORM)
# =========================

def booking(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save()

            # 🔥 NON-BLOCKING EMAIL
            Thread(
                target=send_emails_async,
                args=(booking,),
                daemon=True
            ).start()

            messages.success(
                request,
                "Your booking has been submitted. You will receive a confirmation email shortly."
            )

            return redirect("main:success")
    else:
        form = BookingForm()

    return render(request, "main/booking.html", {"form": form})


# =========================
# API BOOKING (AJAX)
# =========================

@csrf_exempt
def api_booking(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body) if request.content_type == "application/json" else request.POST.dict()

        form_data = {
            "name": data.get("full_name") or data.get("name"),
            "email": data.get("email"),
            "phone": data.get("phone"),
            "service": data.get("service_type") or data.get("service"),
            "booking_date": data.get("preferred_date") or data.get("booking_date"),
            "age": data.get("age"),
            "session_type": data.get("session_type"),
            "course_selection": data.get("course_selection"),
            "medical_condition": data.get("medical_condition"),
            "message": data.get("message", ""),
        }

        form_data = {k: v for k, v in form_data.items() if v not in [None, ""]}

        form = BookingForm(form_data)

        if not form.is_valid():
            return JsonResponse({
                "status": "error",
                "errors": form.errors,
                "message": "Validation failed"
            }, status=400)

        booking = form.save()

        # 🔥 NON-BLOCKING EMAIL
        Thread(
            target=send_emails_async,
            args=(booking,),
            daemon=True
        ).start()

        return JsonResponse({
            "status": "success",
            "message": "Booking submitted successfully.",
            "booking_id": booking.id
        })

    except Exception as e:
        logger.exception("Booking API error")
        return JsonResponse({
            "status": "error",
            "message": "Server error"
        }, status=500)


def api_inquiry(request):
    return JsonResponse({"status": "ok"})
