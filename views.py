from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings

def test_email(request):
    try:
        send_mail(
            "Test Email",
            "SendGrid is working 🚀",
            settings.DEFAULT_FROM_EMAIL,
            ["healing@singingbowlandgonghouse.com"],
            fail_silently=False,
        )
        return HttpResponse("✅ Email sent successfully")
    except Exception as e:
        return HttpResponse(f"❌ Error: {str(e)}")