from django.test import TestCase, override_settings
from django.urls import reverse


@override_settings(ALLOWED_HOSTS=["testserver", "localhost", "127.0.0.1"])
class BookingPageTests(TestCase):
    def test_booking_page_get_renders_form(self):
        response = self.client.get(reverse("main:booking"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Book Your Session")
        self.assertIn("form", response.context)

    def test_booking_page_invalid_post_rerenders_bound_form(self):
        response = self.client.post(
            reverse("main:booking"),
            {
                "name": "",
                "email": "",
                "phone": "",
                "service": "",
                "booking_date": "",
                "session_type": "",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].is_bound)
        self.assertTrue(response.context["form"].errors)
