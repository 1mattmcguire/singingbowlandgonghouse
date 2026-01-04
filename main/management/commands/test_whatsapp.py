"""
Django management command to test WhatsApp configuration.
Usage: python manage.py test_whatsapp
"""
import logging
from django.core.management.base import BaseCommand
from django.conf import settings

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Test WhatsApp configuration by sending a test message'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('📱 Testing WhatsApp Configuration'))
        self.stdout.write(self.style.SUCCESS('='*60))
        
        # Display current configuration
        self.stdout.write(f'\n📋 Current WhatsApp Configuration:')
        
        whatsapp_enabled = getattr(settings, 'TWILIO_WHATSAPP_ENABLED', False)
        if whatsapp_enabled:
            self.stdout.write(self.style.SUCCESS(f'   ✅ WhatsApp: Enabled'))
        else:
            self.stdout.write(self.style.WARNING(f'   ⚠️  WhatsApp: Disabled (set TWILIO_WHATSAPP_ENABLED=true)'))
            self.stdout.write(self.style.ERROR('\n❌ WhatsApp notifications are disabled.'))
            self.stdout.write(self.style.ERROR('   Set TWILIO_WHATSAPP_ENABLED=true in your .env file to enable.'))
            return
        
        account_sid = getattr(settings, 'TWILIO_ACCOUNT_SID', '')
        auth_token = getattr(settings, 'TWILIO_AUTH_TOKEN', '')
        from_number = getattr(settings, 'TWILIO_WHATSAPP_FROM', '')
        to_number = getattr(settings, 'WHATSAPP_ADMIN_NUMBER', '')
        
        if account_sid:
            self.stdout.write(self.style.SUCCESS(f'   ✅ Twilio Account SID: Set'))
        else:
            self.stdout.write(self.style.ERROR(f'   ❌ TWILIO_ACCOUNT_SID: Not set'))
        
        if auth_token:
            self.stdout.write(self.style.SUCCESS(f'   ✅ Twilio Auth Token: Set'))
        else:
            self.stdout.write(self.style.ERROR(f'   ❌ TWILIO_AUTH_TOKEN: Not set'))
        
        if from_number:
            self.stdout.write(self.style.SUCCESS(f'   ✅ WhatsApp From: {from_number}'))
        else:
            self.stdout.write(self.style.ERROR(f'   ❌ TWILIO_WHATSAPP_FROM: Not set'))
        
        if to_number:
            self.stdout.write(self.style.SUCCESS(f'   ✅ Admin WhatsApp: {to_number}'))
        else:
            self.stdout.write(self.style.ERROR(f'   ❌ WHATSAPP_ADMIN_NUMBER: Not set'))
        
        # Check if all required credentials are present
        if not all([account_sid, auth_token, from_number, to_number]):
            self.stdout.write(self.style.ERROR('\n❌ Missing required Twilio credentials.'))
            self.stdout.write(self.style.ERROR('   Please set all required environment variables.'))
            return
        
        # Test WhatsApp message
        self.stdout.write(f'\n📤 Sending test WhatsApp message to: {to_number}')
        try:
            from twilio.rest import Client
            
            client = Client(account_sid, auth_token)
            message_body = """🔔 *Test WhatsApp Message*

This is a test message from Singing Bowl & Gong House booking system.

If you received this message, your WhatsApp configuration is working correctly!

Your WhatsApp notifications are properly configured and ready to receive booking alerts."""
            
            message = client.messages.create(
                from_=from_number,
                body=message_body,
                to=to_number
            )
            
            self.stdout.write(self.style.SUCCESS(f'   ✅ WhatsApp message sent successfully!'))
            self.stdout.write(self.style.SUCCESS(f'   Message SID: {message.sid}'))
            logger.info(f"Test WhatsApp message sent successfully. SID: {message.sid}")
            
        except ImportError:
            self.stdout.write(self.style.ERROR(f'   ❌ Twilio library not installed'))
            self.stdout.write(self.style.ERROR(f'   Install with: pip install twilio'))
            logger.error("Twilio library not installed")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   ❌ Error sending WhatsApp message: {e}'))
            logger.error(f"Error sending test WhatsApp message: {e}", exc_info=True)
        
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('✅ WhatsApp test completed!'))
        self.stdout.write(self.style.SUCCESS('='*60 + '\n'))

