from unittest.mock import patch

from django.test import TestCase, override_settings
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


class TestEmailViewTests(TestCase):
    """Regression tests for the diagnostic test-email endpoint."""

    @override_settings(DEBUG=False)
    @patch("main.views.send_mail")
    def test_test_email_is_hidden_outside_debug(self, mock_send_mail):
        """Production should not expose the diagnostic mail trigger."""
        response = self.client.get("/test-email/")

        self.assertEqual(response.status_code, 404)
        mock_send_mail.assert_not_called()

    @override_settings(DEBUG=True, DEFAULT_FROM_EMAIL="sender@example.com")
    @patch("main.views.send_mail", side_effect=RuntimeError("smtp credentials failed"))
    def test_test_email_hides_mailer_errors(self, mock_send_mail):
        """Debug failures should be logged server-side, not reflected to the client."""
        response = self.client.get("/test-email/")

        self.assertEqual(response.status_code, 500)
        self.assertContains(response, "Unable to send test email.", status_code=500)
        self.assertNotContains(response, "smtp credentials failed", status_code=500)
        mock_send_mail.assert_called_once_with(
            "Test Email",
            "SendGrid is working",
            "sender@example.com",
            ["healing@singingbowlandgonghouse.com"],
            fail_silently=False,
        )
