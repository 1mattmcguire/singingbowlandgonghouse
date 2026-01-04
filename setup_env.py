"""
Setup script to create .env file for Gmail SMTP and WhatsApp configuration.
Run this script to set up your environment variables.
"""
import os
from pathlib import Path

def create_env_file():
    """Create .env file with Gmail SMTP and WhatsApp configuration"""
    base_dir = Path(__file__).parent
    env_file = base_dir / '.env'
    
    print("="*60)
    print("Email & WhatsApp Configuration Setup")
    print("="*60)
    print()
    
    # Check if .env already exists
    if env_file.exists():
        response = input(".env file already exists. Overwrite? (y/n): ").strip().lower()
        if response != 'y':
            print("Setup cancelled.")
            return
    
    # Gmail SMTP Configuration
    print("="*60)
    print("Gmail SMTP Configuration")
    print("="*60)
    print("\nEnter your Gmail credentials:")
    print("(You need to create a Gmail App Password: https://support.google.com/accounts/answer/185833)")
    email_user = input("EMAIL_HOST_USER (Gmail address): ").strip()
    email_password = input("EMAIL_HOST_PASSWORD (Gmail App Password): ").strip()
    
    default_from = input(f"DEFAULT_FROM_EMAIL [{email_user}]: ").strip()
    if not default_from:
        default_from = email_user
    
    # Get booking receiver email
    print("\nEnter the email address where booking notifications should be sent:")
    booking_receiver = input("BOOKING_RECEIVER_EMAIL: ").strip()
    
    # Get admin email
    admin_email = input(f"ADMIN_EMAIL [{booking_receiver}]: ").strip()
    if not admin_email:
        admin_email = booking_receiver
    
    # WhatsApp Configuration
    print("\n" + "="*60)
    print("WhatsApp Configuration (Optional)")
    print("="*60)
    print("\nTo enable WhatsApp notifications, you need a Twilio account.")
    print("Sign up at: https://www.twilio.com/try-twilio")
    print("\nLeave blank to skip WhatsApp setup (you can add it later).")
    
    enable_whatsapp = input("\nEnable WhatsApp notifications? (y/n): ").strip().lower() == 'y'
    
    twilio_sid = ""
    twilio_token = ""
    twilio_from = ""
    whatsapp_admin = ""
    
    if enable_whatsapp:
        twilio_sid = input("TWILIO_ACCOUNT_SID: ").strip()
        twilio_token = input("TWILIO_AUTH_TOKEN: ").strip()
        twilio_from = input("TWILIO_WHATSAPP_FROM (format: whatsapp:+14155238886): ").strip()
        whatsapp_admin = input("WHATSAPP_ADMIN_NUMBER (format: whatsapp:+1234567890): ").strip()
    
    # Create .env content
    env_content = f"""# Django Settings
SECRET_KEY={os.getenv('SECRET_KEY', 'django-insecure-development-only-change-me')}
DEBUG=1
ALLOWED_HOSTS=127.0.0.1,localhost

# Gmail SMTP Configuration
EMAIL_HOST_USER={email_user}
EMAIL_HOST_PASSWORD={email_password}
DEFAULT_FROM_EMAIL={default_from}
BOOKING_RECEIVER_EMAIL={booking_receiver}
ADMIN_EMAIL={admin_email}

# WhatsApp Configuration (Twilio)
TWILIO_WHATSAPP_ENABLED={'true' if enable_whatsapp and all([twilio_sid, twilio_token, twilio_from, whatsapp_admin]) else 'false'}
TWILIO_ACCOUNT_SID={twilio_sid}
TWILIO_AUTH_TOKEN={twilio_token}
TWILIO_WHATSAPP_FROM={twilio_from}
WHATSAPP_ADMIN_NUMBER={whatsapp_admin}

# Timezone
TIME_ZONE=Asia/Kathmandu
"""
    
    # Write .env file
    try:
        with open(env_file, 'w') as f:
            f.write(env_content)
        print()
        print("✅ .env file created successfully!")
        print()
        print("Next steps:")
        print("1. Test email configuration: python manage.py test_email")
        if enable_whatsapp and all([twilio_sid, twilio_token, twilio_from, whatsapp_admin]):
            print("2. Test WhatsApp configuration: python manage.py test_whatsapp")
        print("3. Make a test booking to verify notifications are sent")
        print()
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")

if __name__ == "__main__":
    create_env_file()





