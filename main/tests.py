import tempfile

from django.core.management import call_command
from django.test import TestCase, override_settings
from django.urls import reverse

from .management.commands.load_instruments import INSTRUMENTS_DATA
from .models import Instrument


EXPECTED_INSTRUMENT_COUNT = sum(
    len(entry["instruments"]) for entry in INSTRUMENTS_DATA
)


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


class LoadInstrumentsCommandTests(TestCase):
    """Regression tests for the catalog import management command."""

    def test_skip_images_imports_full_catalog_with_placeholder_image(self):
        """--skip-images must still create instruments instead of skipping all of them."""
        with tempfile.TemporaryDirectory() as media_root, override_settings(
            MEDIA_ROOT=media_root
        ):
            call_command("load_instruments", skip_images=True, verbosity=0)

            instrument_images = list(
                Instrument.objects.order_by("id").values_list("image", flat=True)
            )

        self.assertEqual(len(instrument_images), EXPECTED_INSTRUMENT_COUNT)
        self.assertEqual(
            set(instrument_images),
            {"instruments/placeholder-mainimage.jpg"},
        )

    def test_clear_and_skip_images_rebuilds_catalog_instead_of_wiping_it(self):
        """The documented skip-images path must not erase the catalog when used with --clear."""
        with tempfile.TemporaryDirectory() as media_root, override_settings(
            MEDIA_ROOT=media_root
        ):
            call_command("load_instruments", verbosity=0)
            self.assertEqual(Instrument.objects.count(), EXPECTED_INSTRUMENT_COUNT)

            call_command("load_instruments", clear=True, skip_images=True, verbosity=0)

            self.assertEqual(Instrument.objects.count(), EXPECTED_INSTRUMENT_COUNT)
