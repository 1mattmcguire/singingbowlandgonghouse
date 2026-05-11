from django.test import TestCase
from django.urls import reverse


class BookingViewTests(TestCase):
    """Regression tests for the public booking view."""

    def test_booking_get_returns_200(self):
        """GET /booking/ must render the form and not 500.

        Previously the view fell off the end of the function for GET requests
        and returned None, which Django converts into a 500 ValueError. The
        URL is also listed in sitemap.xml, so search engine crawlers were
        hitting the same crash.
        """
        response = self.client.get(reverse("main:booking"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/booking.html")
        self.assertIn("form", response.context)

    def test_booking_post_invalid_returns_200(self):
        """POST with an invalid (empty) payload must re-render the form, not 500."""
        response = self.client.post(reverse("main:booking"), data={})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/booking.html")
