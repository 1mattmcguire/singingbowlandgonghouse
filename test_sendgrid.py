#!/usr/bin/env python
# test_sendgrid.py

import smtplib
import socket
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ===== CONFIGURE THESE VALUES =====
SENDGRID_HOST = 'smtp.sendgrid.net'
SENDGRID_PORT = 587  # Try 465 if this fails
API_KEY = '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'  # Replace with your actual API key
FROM_EMAIL = 'healing@singingbowlandgonghouse.com'  # Must be verified in SendGrid
TO_EMAIL = 'zenishbakhati0@gmail.com'  # Where to send test email
# ==================================

def test_connection():
    """Test basic connection to SendGrid server"""
    print(f"Testing connection to {SENDGRID_HOST}:{SENDGRID_PORT}")
    
    try:
        server = smtplib.SMTP(SENDGRID_HOST, SENDGRID_PORT, timeout=10)
        server.ehlo()
        print("✓ Connected to SendGrid server")
        server.quit()
        return True
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        return False

def test_tls():
    """Test TLS encryption"""
    print("\nTesting TLS encryption...")
    
    try:
        server = smtplib.SMTP(SENDGRID_HOST, SENDGRID_PORT, timeout=10)
        server.ehlo()
        server.starttls()
        server.ehlo()
        print("✓ TLS started successfully")
        server.quit()
        return True
    except Exception as e:
        print(f"✗ TLS failed: {e}")
        return False

def test_authentication():
    """Test API key authentication"""
    print("\nTesting authentication...")
    
    try:
        server = smtplib.SMTP(SENDGRID_HOST, SENDGRID_PORT, timeout=10)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login('apikey', API_KEY)
        print("✓ Authentication successful")
        server.quit()
        return True
    except smtplib.SMTPAuthenticationError:
        print("✗ Authentication failed!")
        print("Please verify:")
        print("1. Username is 'apikey' (not your email)")
        print("2. API Key is correct and has 'Mail Send' permission")
        print("3. Sender email is verified in SendGrid")
        return False
    except Exception as e:
        print(f"✗ Authentication error: {e}")
        return False

def send_test_email():
    """Send a test email through SendGrid"""
    print("\nSending test email...")
    
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = FROM_EMAIL
        msg['To'] = TO_EMAIL
        msg['Subject'] = 'SendGrid Test Email from Django Server'
        
        body = f"""This is a test email sent via SendGrid SMTP.
        
        Configuration:
        - Host: {SENDGRID_HOST}
        - Port: {SENDGRID_PORT}
        - From: {FROM_EMAIL}
        
        If you receive this, SendGrid is working correctly!
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Connect and send
        server = smtplib.SMTP(SENDGRID_HOST, SENDGRID_PORT, timeout=10)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login('apikey', API_KEY)
        
        server.sendmail(FROM_EMAIL, TO_EMAIL, msg.as_string())
        print(f"✓ Test email sent successfully to {TO_EMAIL}")
        
        server.quit()
        return True
        
    except Exception as e:
        print(f"✗ Failed to send email: {e}")
        return False

def main():
    print("=" * 50)
    print("SENDGRID CONNECTION TEST")
    print("=" * 50)
    
    # Check configuration
    if API_KEY == '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':
        print("\n⚠️  WARNING: You need to configure the API_KEY variable!")
        print("Get your API key from: https://app.sendgrid.com/settings/api_keys")
        return
    
    # Run tests
    if not test_connection():
        print("\nTrying alternative port 465...")
        global SENDGRID_PORT
        SENDGRID_PORT = 465
        if not test_connection():
            return
    
    test_tls()
    test_authentication()
    
    # Ask before sending actual email
    print("\n" + "=" * 50)
    send_email = input("Do you want to send a test email? (y/n): ")
    
    if send_email.lower() == 'y':
        send_test_email()
    else:
        print("Test email not sent.")
    
    print("\n" + "=" * 50)
    print("Test completed!")

if __name__ == "__main__":
    main()
