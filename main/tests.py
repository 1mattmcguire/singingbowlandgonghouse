from pathlib import Path

from django.conf import settings
from django.test import SimpleTestCase, TestCase, override_settings
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


class ProductionAvailabilityTests(SimpleTestCase):
    """Regression tests for production-only routing and proxy behavior."""

    @override_settings(
        ALLOWED_HOSTS=["testserver"],
        SECURE_SSL_REDIRECT=True,
        SECURE_PROXY_SSL_HEADER=("HTTP_X_FORWARDED_PROTO", "https"),
    )
    def test_forwarded_https_request_is_not_redirected_again(self):
        """Trusted proxy HTTPS traffic must reach the view instead of looping."""
        response = self.client.get(
            reverse("main:home"),
            HTTP_X_FORWARDED_PROTO="https",
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/home.html")

    @override_settings(
        ALLOWED_HOSTS=["testserver"],
        DEBUG=False,
        SECURE_SSL_REDIRECT=False,
    )
    def test_media_files_remain_reachable_when_debug_disabled(self):
        """Catalog images under MEDIA_ROOT must still be downloadable in production."""
        probe = Path(settings.MEDIA_ROOT) / "test-media-probe.txt"
        probe.parent.mkdir(parents=True, exist_ok=True)
        probe.write_text("media-ok", encoding="utf-8")
        try:
            response = self.client.get(f"{settings.MEDIA_URL}test-media-probe.txt")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content, b"media-ok")
        finally:
            probe.unlink(missing_ok=True)
