from django.test import TestCase
from django.urls import reverse


class BookingViewTests(TestCase):
    def test_booking_page_loads(self):
        response = self.client.get(reverse("main:booking"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/booking.html")
        self.assertIn("form", response.context)

    def test_booking_invalid_post_rerenders_form(self):
        response = self.client.post(reverse("main:booking"), {})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/booking.html")
        self.assertTrue(response.context["form"].errors)
