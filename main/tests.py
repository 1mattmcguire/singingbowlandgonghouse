from django.test import SimpleTestCase, override_settings
from django.urls import reverse


@override_settings(ALLOWED_HOSTS=["testserver", "localhost", "127.0.0.1"])
class BookingViewTests(SimpleTestCase):
    def test_booking_page_renders_on_get(self):
        response = self.client.get(reverse("main:booking"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/booking.html")
        self.assertContains(response, "Book Your Session")
        self.assertIn("form", response.context)

    def test_booking_page_rerenders_invalid_post_instead_of_crashing(self):
        response = self.client.post(reverse("main:booking"), {})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/booking.html")
        self.assertIn("form", response.context)
        self.assertTrue(response.context["form"].errors)
