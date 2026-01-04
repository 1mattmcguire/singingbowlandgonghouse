"""
Django management command to test email configuration.
Usage: python manage.py test_email
"""
import logging
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Test email configuration by sending test emails to client and admin'

    def add_arguments(self, parser):
        parser.add_argument(
            '--client-email',
            type=str,
            help='Client email address to send test email to',
            default=None,
        )
        parser.add_argument(
            '--admin-email',
            type=str,
            help='Admin email address to send test email to',
            default=None,
        )

    def handle(self, *args, **options):
        client_email = options.get('client_email') or 'test@example.com'
        admin_email = options.get('admin_email') or getattr(settings, 'ADMIN_EMAIL', 'singingbowlandgonghouse@gmail.com')
        
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('📧 Testing Email Configuration'))
        self.stdout.write(self.style.SUCCESS('='*60))
        
        # Display current configuration
        self.stdout.write(f'\n📋 Current Email Configuration:')
        self.stdout.write(f'   Email Backend: {settings.EMAIL_BACKEND}')
        self.stdout.write(f'   Email Host: {settings.EMAIL_HOST}')
        self.stdout.write(f'   Email Port: {settings.EMAIL_PORT}')
        self.stdout.write(f'   Use TLS: {settings.EMAIL_USE_TLS}')
        if settings.EMAIL_HOST_USER:
            self.stdout.write(self.style.SUCCESS(f'   ✅ Email User: {settings.EMAIL_HOST_USER}'))
        else:
            self.stdout.write(self.style.WARNING(f'   ⚠️  EMAIL_HOST_USER: Not set'))
        if settings.EMAIL_HOST_PASSWORD:
            self.stdout.write(self.style.SUCCESS(f'   ✅ Email Password: Set'))
        else:
            self.stdout.write(self.style.WARNING(f'   ⚠️  EMAIL_HOST_PASSWORD: Not set'))
        self.stdout.write(f'   From Email: {settings.DEFAULT_FROM_EMAIL}')
        booking_receiver = getattr(settings, 'BOOKING_RECEIVER_EMAIL', None)
        if booking_receiver:
            self.stdout.write(self.style.SUCCESS(f'   ✅ Booking Receiver Email: {booking_receiver}'))
        else:
            self.stdout.write(self.style.WARNING(f'   ⚠️  Booking Receiver Email: Not set (using admin email)'))
        self.stdout.write(f'   Admin Email: {admin_email}')
        
        # Test client email
        self.stdout.write(f'\n📤 Sending test email to client: {client_email}')
        try:
            send_mail(
                subject='Test Email - Singing Bowl & Gong House',
                message=f'''Hello!

This is a test email from Singing Bowl & Gong House booking system.

If you received this email, your email configuration is working correctly!

Email Backend: {settings.EMAIL_BACKEND}
From: {settings.DEFAULT_FROM_EMAIL}

Best regards,
Singing Bowl & Gong House Team''',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[client_email],
                fail_silently=False,
            )
            self.stdout.write(self.style.SUCCESS(f'   ✅ Client email sent successfully!'))
            logger.info(f"Test email sent successfully to client: {client_email}")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   ❌ Error sending client email: {e}'))
            logger.error(f"Error sending test email to client {client_email}: {e}", exc_info=True)
        
        # Test admin email
        self.stdout.write(f'\n📤 Sending test email to admin: {admin_email}')
        try:
            send_mail(
                subject='🔔 Test Email - New Booking Notification',
                message=f'''This is a test notification email.

Your email configuration is working correctly!

Email Backend: {settings.EMAIL_BACKEND}
From: {settings.DEFAULT_FROM_EMAIL}

This is how booking notifications will look when customers make bookings.

Best regards,
Singing Bowl & Gong House Booking System''',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[admin_email],
                fail_silently=False,
            )
            self.stdout.write(self.style.SUCCESS(f'   ✅ Admin email sent successfully!'))
            logger.info(f"Test email sent successfully to admin: {admin_email}")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   ❌ Error sending admin email: {e}'))
            logger.error(f"Error sending test email to admin {admin_email}: {e}", exc_info=True)
        
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('✅ Email test completed!'))
        self.stdout.write(self.style.SUCCESS('='*60 + '\n'))





