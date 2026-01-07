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

# ======================================================
# ASYNC EMAIL HANDLER (SAFE FOR GUNICORN)
# ======================================================

def send_emails_async(booking):
    try:
        logger.info("📧 Email sending started")
        send_booking_emails(booking)
        logger.info("✅ Email sending finished")
    except Exception:
        logger.exception("❌ Email sending failed")


# ======================================================
# PAGE VIEWS
# ======================================================

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


# ======================================================
# CONTACT FORM
# ======================================================

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


# ======================================================
# BOOKING (HTML FORM)
# ======================================================

def booking(request):
    if request.method == "POST":
        form = BookingForm(request.POST)

        if form.is_valid():
            booking = form.save()

            Thread(
                target=send_booking_emails,
                args=(booking,),
                daemon=True
            ).start()

            messages.success(request, "Booking submitted successfully.")
            return redirect("main:success")

    else:
        form = BookingForm()



# ======================================================
# BOOKING API (AJAX / FETCH)
# ======================================================

@csrf_exempt
def api_booking(request):

    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        data = (
            json.loads(request.body)
            if request.content_type == "application/json"
            else request.POST.dict()
        )

        form = BookingForm(data)

        if not form.is_valid():
            logger.warning("❌ Booking validation failed")
            return JsonResponse({
                "status": "error",
                "errors": form.errors
            }, status=400)

        booking = form.save()
        logger.info(f"✅ Booking #{booking.id} saved")

        # 🔥 ASYNC EMAIL
        Thread(
            target=send_emails_async,
            args=(booking,),
            daemon=True
        ).start()

        return JsonResponse({
            "status": "success",
            "message": "Booking submitted successfully."
        })

    except Exception:
        logger.exception("❌ API booking error")
        return JsonResponse({
            "status": "error",
            "message": "Server error"
        }, status=500)


# ======================================================
# SIMPLE API HEALTH CHECK
# ======================================================

def api_inquiry(request):
    return JsonResponse({"status": "ok"})
