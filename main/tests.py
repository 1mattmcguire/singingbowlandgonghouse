from django.test import TestCase
from django.urls import reverse

from .models import Booking


class BookingViewTests(TestCase):
    def test_booking_get_renders_form(self):
        response = self.client.get(reverse("main:booking"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/booking.html")
        self.assertIn("form", response.context)

    def test_booking_invalid_post_renders_errors_without_saving(self):
        response = self.client.post(reverse("main:booking"), data={})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/booking.html")
        self.assertIn("form", response.context)
        self.assertTrue(response.context["form"].errors)
        self.assertEqual(Booking.objects.count(), 0)
