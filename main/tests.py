from unittest.mock import patch

from django.http import Http404
from django.test import RequestFactory, TestCase, override_settings
from django.urls import reverse

from main import views


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


class TestEmailViewTests(TestCase):
    """Regression tests for the debug-only email helper view."""

    @override_settings(DEBUG=False)
    @patch("main.views.send_mail")
    def test_test_email_returns_404_outside_debug(self, mock_send_mail):
        response = self.client.get("/test-email/")
        self.assertEqual(response.status_code, 404)
        mock_send_mail.assert_not_called()

    @override_settings(DEBUG=False)
    @patch("main.views.send_mail")
    def test_test_email_view_raises_404_outside_debug(self, mock_send_mail):
        request = RequestFactory().get("/test-email/")

        with self.assertRaises(Http404):
            views.test_email(request)

        mock_send_mail.assert_not_called()

    @override_settings(DEBUG=True)
    @patch("main.views.send_mail", side_effect=Exception("smtp credentials leaked"))
    def test_test_email_hides_exception_details(self, mock_send_mail):
        request = RequestFactory().get("/test-email/")

        response = views.test_email(request)
        response_text = response.content.decode()

        self.assertEqual(response.status_code, 500)
        self.assertTrue(response_text.endswith("Error sending test email"))
        self.assertNotIn("smtp credentials leaked", response_text)
        mock_send_mail.assert_called_once()
