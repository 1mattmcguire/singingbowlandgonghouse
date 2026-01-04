from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
import json
import os
import logging
from pathlib import Path

# Set up logger
logger = logging.getLogger(__name__)

from .models import Booking, Inquiry
from .forms import BookingForm, InquiryForm


def send_whatsapp_notification(booking):
    """
    Send WhatsApp notification to admin when a new booking is created.
    Uses Twilio WhatsApp API.
    Returns True if successful, False otherwise.
    """
    if not getattr(settings, 'TWILIO_WHATSAPP_ENABLED', False):
        logger.debug("WhatsApp notifications disabled")
        return False
    
    try:
        from twilio.rest import Client
        
        account_sid = settings.TWILIO_ACCOUNT_SID
        auth_token = settings.TWILIO_AUTH_TOKEN
        from_number = settings.TWILIO_WHATSAPP_FROM
        to_number = settings.WHATSAPP_ADMIN_NUMBER
        
        if not all([account_sid, auth_token, from_number, to_number]):
            logger.warning("Missing Twilio credentials for WhatsApp notification")
            return False
        
        # Format the message
        message_body = f"""🔔 *New Booking Received*

*Name:* {booking.name}
*Email:* {booking.email}
*Phone:* {booking.phone}
*Service:* {booking.get_service_display()}
*Booking Date:* {booking.booking_date.strftime("%B %d, %Y")}
*Session Type:* {booking.session_type or "N/A"}
*Course:* {booking.course_selection or "N/A"}
*Age:* {booking.age or "Not provided"}

*Medical Condition/Needs:*
{booking.medical_condition or "None specified"}

*Message:*
{booking.message or "None"}

*Submitted:* {booking.created_at.strftime("%Y-%m-%d %H:%M:%S")}"""
        
        # Send WhatsApp message via Twilio
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            from_=from_number,
            body=message_body,
            to=to_number
        )
        
        logger.info(f"WhatsApp notification sent successfully. SID: {message.sid}")
        return True
        
    except ImportError:
        logger.error("Twilio library not installed. Install with: pip install twilio")
        return False
    except Exception as e:
        logger.error(f"Error sending WhatsApp notification: {e}", exc_info=True)
        return False


def home(request):
    """Home page view"""
    return render(request, 'main/home.html')


def about(request):
    """About page view"""
    return render(request, 'main/about.html')


def services(request):
    """Services page view"""
    return render(request, 'main/services.html')


def courses(request):
    """Courses page view"""
    return render(request, 'main/courses.html')


def contact(request):
    """Contact page view with inquiry form"""
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save()
            
            # Send thank you email to user
            try:
                send_mail(
                    subject='Thank You for Contacting Singing Bowl & Gong House',
                    message=f'''Dear {inquiry.name},

Thank you for reaching out to Singing Bowl & Gong House. We have received your inquiry and will get back to you within 24 hours.

Your Inquiry Details:
- Subject: {inquiry.subject or 'General Inquiry'}
- Message: {inquiry.message[:200]}...

We look forward to connecting with you soon.

Best regards,
Singing Bowl & Gong House Team''',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[inquiry.email],
                    fail_silently=True,  # Don't block booking if email fails
                )
            except Exception as e:
                logger.error(f"❌ Error sending confirmation email to user {inquiry.email}: {e}", exc_info=True)
                # Don't raise - inquiry should succeed even if email fails
            else:
                logger.info(f"✅ User confirmation email sent successfully to: {inquiry.email}")
            
            # Send notification email to admin
            try:
                admin_email = getattr(settings, 'ADMIN_EMAIL', settings.DEFAULT_FROM_EMAIL)
                logger.info(f"📧 Sending inquiry notification email to: {admin_email}")
                send_mail(
                    subject=f'New Inquiry from {inquiry.name}',
                    message=f'''New inquiry received:

Name: {inquiry.name}
Email: {inquiry.email}
Phone: {inquiry.phone or 'Not provided'}
Subject: {inquiry.subject or 'No subject'}
Message: {inquiry.message}

Submitted at: {inquiry.created_at.strftime("%Y-%m-%d %H:%M:%S")}''',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[admin_email],
                    fail_silently=True,  # Don't block inquiry if email fails
                )
            except Exception as e:
                logger.error(f"❌ Error sending inquiry notification email to {admin_email}: {e}", exc_info=True)
                # Don't raise - inquiry should succeed even if email fails
            else:
                logger.info(f"✅ Inquiry notification email sent successfully to: {admin_email}")
            
            messages.success(request, 'Thank you! Your inquiry has been submitted successfully. We will contact you within 24 hours.')
            return redirect('success')
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = InquiryForm()
    
    return render(request, 'main/contact.html', {'form': form})


def booking(request):
    """Booking page view with booking form"""
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save()
            logger.info(f"✅ Booking saved: ID={booking.id}, Name={booking.name}, Email={booking.email}")
            
            # Send thank you email to user with complete booking details
            try:
                user_email_body = f'''Dear {booking.name},

Thank you for booking with Singing Bowl & Gong House!

We have received your booking request and will contact you within 24 hours to confirm your session and answer any questions you may have.

YOUR BOOKING DETAILS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Name: {booking.name}
Email: {booking.email}
Phone: {booking.phone}
Service: {booking.get_service_display()}
Booking Date: {booking.booking_date.strftime("%B %d, %Y")}
Session Type: {booking.session_type or "N/A"}
Course Selection: {booking.course_selection or "N/A"}
Age: {booking.age or "Not provided"}

Medical Condition/Specific Needs:
{booking.medical_condition or "None specified"}

Additional Message:
{booking.message or "None"}

Booking Reference: #{booking.id}
Submitted: {booking.created_at.strftime("%B %d, %Y at %I:%M %p")}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

We look forward to serving you and providing you with a transformative healing experience!

If you have any questions or need to modify your booking, please don't hesitate to contact us.

Best regards,
Singing Bowl & Gong House Team
Email: singingbowlandgonghouse@gmail.com
Phone: +977 984-3213802'''
                
                send_mail(
                    subject='Booking Confirmation - Singing Bowl & Gong House',
                    message=user_email_body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[booking.email],
                    fail_silently=True,  # Don't block booking if email fails
                )
            except Exception as e:
                print(f"❌ Error sending email to user: {e}")
                import traceback
                traceback.print_exc()
            else:
                print(f"✅ User confirmation email sent successfully to: {booking.email}")
            
            # Send notification email to admin
            try:
                admin_email = getattr(settings, 'ADMIN_EMAIL', settings.DEFAULT_FROM_EMAIL)
                print(f"\n📧 Sending admin notification email to: {admin_email}")
                admin_email_body = f'''🔔 NEW BOOKING RECEIVED

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CUSTOMER INFORMATION:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Name: {booking.name}
Email: {booking.email}
Phone: {booking.phone}
Age: {booking.age or "Not provided"}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BOOKING DETAILS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Service: {booking.get_service_display()}
Booking Date: {booking.booking_date.strftime("%B %d, %Y")}
Session Type: {booking.session_type or "N/A"}
Course Selection: {booking.course_selection or "N/A"}

Medical Condition/Specific Needs:
{booking.medical_condition or "None specified"}

Additional Message:
{booking.message or "None"}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Booking Reference: #{booking.id}
Submitted: {booking.created_at.strftime("%B %d, %Y at %I:%M %p")}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Please contact the customer within 24 hours to confirm the booking.'''
                
                send_mail(
                    subject=f'🔔 New Booking from {booking.name} - {booking.get_service_display()}',
                    message=admin_email_body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[booking_receiver],
                    fail_silently=True,  # Don't block booking if email fails
                )
                logger.info(f"✅ Booking notification email sent successfully to: {booking_receiver}")
                print(f"✅ Booking notification email sent successfully to: {booking_receiver}")
            except Exception as e:
                logger.error(f"❌ Error sending booking notification email to {booking_receiver}: {e}", exc_info=True)
                print(f"❌ Error sending booking notification email: {e}")
                import traceback
                traceback.print_exc()
                # Don't raise - booking should succeed even if email fails
            
            # Send WhatsApp notification
            try:
                whatsapp_sent = send_whatsapp_notification(booking)
                if whatsapp_sent:
                    logger.info("WhatsApp notification sent successfully")
                else:
                    logger.debug("WhatsApp notification not sent (disabled or failed)")
            except Exception as e:
                logger.error(f"Error sending WhatsApp notification: {e}", exc_info=True)
                # Don't raise - booking should succeed even if WhatsApp fails
            
            messages.success(request, 'Thank you! Your booking has been submitted successfully. We will contact you within 24 hours.')
            return redirect('success')
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = BookingForm()
    
    return render(request, 'main/booking.html', {'form': form})


def success(request):
    """Success page after form submission"""
    return render(request, 'main/success.html')


# API Views for AJAX form submissions
@csrf_exempt
@require_http_methods(["POST"])
def api_booking(request):
    """API endpoint for booking form submission"""
    try:
        data = json.loads(request.body)
        print(f"📥 Received booking request: {data}")
        
        # Helper function to clean data (convert empty strings to None for optional fields)
        def clean_value(value):
            if value == '' or value is None:
                return None
            return value
        
        # Map frontend data to model fields
        booking_data = {
            'name': (data.get('full_name') or data.get('name') or '').strip(),
            'email': (data.get('email') or '').strip(),
            'phone': (data.get('phone') or '').strip(),
            'service': data.get('service_type', 'personal'),
            'booking_date': data.get('enrollment_date') or data.get('preferred_date') or data.get('booking_date'),
            'message': clean_value(data.get('message', '')),
            'age': clean_value(data.get('age')),
            'session_type': clean_value(data.get('session_type')),
            'course_selection': clean_value(data.get('course_selection')),
            'medical_condition': clean_value(data.get('medical_condition')),
        }
        
        # Validate required fields are present
        if not booking_data['name']:
            return JsonResponse({
                'success': False,
                'error': 'Name is required.'
            }, status=400)
        if not booking_data['email']:
            return JsonResponse({
                'success': False,
                'error': 'Email is required.'
            }, status=400)
        if not booking_data['phone']:
            return JsonResponse({
                'success': False,
                'error': 'Phone number is required.'
            }, status=400)
        if not booking_data['booking_date']:
            return JsonResponse({
                'success': False,
                'error': 'Booking date is required.'
            }, status=400)
        
        form = BookingForm(booking_data)
        if form.is_valid():
            booking = form.save()
            logger.info(f"✅ Booking saved via API: ID={booking.id}, Name={booking.name}, Email={booking.email}")
            
            # Send thank you email to user with complete booking details
            try:
                user_email_body = f'''Dear {booking.name},

Thank you for booking with Singing Bowl & Gong House!

We have received your booking request and will contact you within 24 hours to confirm your session and answer any questions you may have.

YOUR BOOKING DETAILS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Name: {booking.name}
Email: {booking.email}
Phone: {booking.phone}
Service: {booking.get_service_display()}
Booking Date: {booking.booking_date.strftime("%B %d, %Y")}
Session Type: {booking.session_type or "N/A"}
Course Selection: {booking.course_selection or "N/A"}
Age: {booking.age or "Not provided"}

Medical Condition/Specific Needs:
{booking.medical_condition or "None specified"}

Additional Message:
{booking.message or "None"}

Booking Reference: #{booking.id}
Submitted: {booking.created_at.strftime("%B %d, %Y at %I:%M %p")}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

We look forward to serving you and providing you with a transformative healing experience!

If you have any questions or need to modify your booking, please don't hesitate to contact us.

Best regards,
Singing Bowl & Gong House Team
Email: singingbowlandgonghouse@gmail.com
Phone: +977 984-3213802'''
                
                send_mail(
                    subject='Booking Confirmation - Singing Bowl & Gong House',
                    message=user_email_body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[booking.email],
                    fail_silently=True,  # Don't block booking if email fails
                )
            except Exception as e:
                print(f"❌ Error sending email to user: {e}")
                import traceback
                traceback.print_exc()
            else:
                print(f"✅ User confirmation email sent successfully to: {booking.email}")
            
            # Send notification email to admin
            try:
                admin_email = getattr(settings, 'ADMIN_EMAIL', settings.DEFAULT_FROM_EMAIL)
                print(f"\n📧 Sending admin notification email to: {admin_email}")
                admin_email_body = f'''🔔 NEW BOOKING RECEIVED

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CUSTOMER INFORMATION:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Name: {booking.name}
Email: {booking.email}
Phone: {booking.phone}
Age: {booking.age or "Not provided"}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BOOKING DETAILS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Service: {booking.get_service_display()}
Booking Date: {booking.booking_date.strftime("%B %d, %Y")}
Session Type: {booking.session_type or "N/A"}
Course Selection: {booking.course_selection or "N/A"}

Medical Condition/Specific Needs:
{booking.medical_condition or "None specified"}

Additional Message:
{booking.message or "None"}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Booking Reference: #{booking.id}
Submitted: {booking.created_at.strftime("%B %d, %Y at %I:%M %p")}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Please contact the customer within 24 hours to confirm the booking.'''
                
                send_mail(
                    subject=f'🔔 New Booking from {booking.name} - {booking.get_service_display()}',
                    message=admin_email_body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[booking_receiver],
                    fail_silently=True,  # Don't block booking if email fails
                )
            except Exception as e:
                logger.error(f"❌ Error sending inquiry notification email to {admin_email}: {e}", exc_info=True)
                # Don't raise - inquiry should succeed even if email fails
            else:
                logger.info(f"✅ Inquiry notification email sent successfully to: {admin_email}")
            
            # Send WhatsApp notification
            try:
                whatsapp_sent = send_whatsapp_notification(booking)
                if whatsapp_sent:
                    logger.info("WhatsApp notification sent successfully")
                else:
                    logger.debug("WhatsApp notification not sent (disabled or failed)")
            except Exception as e:
                logger.error(f"Error sending WhatsApp notification: {e}", exc_info=True)
                # Don't raise - booking should succeed even if WhatsApp fails
            
            print(f"✅ Booking saved successfully: ID={booking.id}, Name={booking.name}, Email={booking.email}")
            return JsonResponse({
                'success': True,
                'message': 'Booking submitted successfully! We will contact you within 24 hours.'
            })
        else:
            # Format validation errors for better display
            error_messages = []
            for field, errors in form.errors.items():
                for error in errors:
                    field_label = form.fields[field].label if field in form.fields else field
                    error_messages.append(f"{field_label}: {error}")
            
            error_message = "; ".join(error_messages) if error_messages else "Please correct the errors in the form."
            
            # Log validation errors for debugging
            print(f"❌ Booking form validation failed:")
            print(f"   Data received: {booking_data}")
            print(f"   Validation errors: {form.errors}")
            print(f"   Error message: {error_message}")
            
            return JsonResponse({
                'success': False,
                'error': error_message,
                'errors': form.errors
            }, status=400)
    except json.JSONDecodeError as e:
        print(f"❌ JSON decode error: {e}")
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON data received. Please try again.'
        }, status=400)
    except Exception as e:
        print(f"❌ Unexpected error in api_booking: {e}")
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'success': False,
            'error': f'An error occurred while processing your booking: {str(e)}'
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def api_inquiry(request):
    """API endpoint for inquiry form submission"""
    try:
        data = json.loads(request.body)
        
        inquiry_data = {
            'name': data.get('full_name') or data.get('name'),
            'email': data.get('email'),
            'phone': data.get('phone', ''),
            'subject': data.get('subject', 'General Inquiry'),
            'message': data.get('message'),
        }
        
        form = InquiryForm(inquiry_data)
        if form.is_valid():
            inquiry = form.save()
            
            # Send emails (same as in contact view)
            try:
                send_mail(
                    subject='Thank You for Contacting Singing Bowl & Gong House',
                    message=f'''Dear {inquiry.name},

Thank you for reaching out to Singing Bowl & Gong House. We have received your inquiry and will get back to you within 24 hours.

Your Inquiry Details:
- Subject: {inquiry.subject or 'General Inquiry'}
- Message: {inquiry.message[:200]}...

We look forward to connecting with you soon.

Best regards,
Singing Bowl & Gong House Team''',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[inquiry.email],
                    fail_silently=True,  # Don't block booking if email fails
                )
            except Exception as e:
                logger.error(f"❌ Error sending confirmation email to user {inquiry.email}: {e}", exc_info=True)
                # Don't raise - inquiry should succeed even if email fails
            else:
                logger.info(f"✅ User confirmation email sent successfully to: {inquiry.email}")
            
            try:
                admin_email = getattr(settings, 'ADMIN_EMAIL', settings.DEFAULT_FROM_EMAIL)
                send_mail(
                    subject=f'New Inquiry from {inquiry.name}',
                    message=f'''New inquiry received:

Name: {inquiry.name}
Email: {inquiry.email}
Phone: {inquiry.phone or 'Not provided'}
Subject: {inquiry.subject or 'No subject'}
Message: {inquiry.message}

Submitted at: {inquiry.created_at.strftime("%Y-%m-%d %H:%M:%S")}''',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[booking_receiver],
                    fail_silently=True,  # Don't block booking if email fails
                )
            except Exception as e:
                logger.error(f"❌ Error sending inquiry notification email to {admin_email}: {e}", exc_info=True)
                # Don't raise - inquiry should succeed even if email fails
            else:
                logger.info(f"✅ Inquiry notification email sent successfully to: {admin_email}")
            
            return JsonResponse({
                'success': True,
                'message': 'Inquiry submitted successfully! We will contact you within 24 hours.'
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


def test_email(request):
    """Test email endpoint - for development/testing only"""
    try:
        recipient = getattr(settings, 'BOOKING_RECEIVER_EMAIL', None) or getattr(settings, 'ADMIN_EMAIL', settings.DEFAULT_FROM_EMAIL)
        send_mail(
            subject="📩 Test Email from Django",
            message=f"Email backend: {settings.EMAIL_BACKEND}\n\nIf you received this, your email configuration works!",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient],
            fail_silently=True,
        )
        logger.info(f"Test email sent to {recipient}")
        return HttpResponse("Email sent successfully! 🎉 Check your inbox.")
    except Exception as e:
        logger.error(f"Error sending test email: {e}", exc_info=True)
        return HttpResponse(f"Error: {e}")


def smiles(request):
    """
    Renders the 'Smiles We Created' page with automatically categorized images.
    Images are organized based on their filenames:
    - School Bags: contains 'bag', 'bags', 'school bag' in filename
    - Stationery: contains 'stationery', 'stationary' in filename
    - Uniforms: contains 'uniform', 'education support' in filename
    - Scholarships: contains 'scholarship', 'momentofjoeey' in filename
    - Gallery: all other education-related images
    """
    # Get the base directory
    BASE_DIR = Path(__file__).resolve().parent.parent
    images_dir = BASE_DIR / 'main' / 'static' / 'main' / 'images'
    
    # Categories for feature cards
    categories = {
        'school_bags': [],
        'stationery': [],
        'uniforms': [],
        'scholarships': [],
        'moments_of_joy': [],
        'gallery': []
    }
    
    # Keywords for categorization
    keywords = {
        'school_bags': ['bag', 'bags', 'school bag', 'schoolbag'],
        'stationery': ['stationery', 'stationary', 'stationeryitem', 'stationerycopy'],
        'uniforms': ['uniform', 'education support'],
        'scholarships': ['scholarship', 'momentofjoeey'],
        'moments_of_joy': ['momentofjoy', 'momentofjoyy', 'momentofjoyyy', 'momentofjoyyyy', 'momentofjoey', 'momentoffjoey', 'happy', 'smile', 'smiles'],
        'gallery': ['education', 'moment', 'student', 'impact', 'joy']
    }
    
    # Scan images directory
    if images_dir.exists():
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
        
        for file_path in images_dir.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in image_extensions:
                filename_lower = file_path.name.lower()
                
                # Skip non-education related images
                skip_keywords = ['logo', 'gong', 'bowl', 'handpan', 'chakra', 'tamtam', 'nipple', 
                                'scroll', 'training', 'therapy', 'healing', 'grouphealing', 
                                'personalhealing', 'aboutus', 'hero', 'mainimage', 'bgimg',
                                'map', 'whatsapp', 'wechat', 'google', 'jam', 'black', 'tiger',
                                'matt', 'plain', 'buddhacham', 'kopre', 'thado', 'ulta', 'stand',
                                'manipuree', 'happy faces', 'course', 'singing bowl']
                
                if any(skip in filename_lower for skip in skip_keywords):
                    continue
                
                # Categorize based on filename
                categorized = False
                
                # Check for school bags
                if any(keyword in filename_lower for keyword in keywords['school_bags']):
                    categories['school_bags'].append(file_path.name)
                    categorized = True
                
                # Check for stationery
                elif any(keyword in filename_lower for keyword in keywords['stationery']):
                    categories['stationery'].append(file_path.name)
                    categorized = True
                
                # Check for uniforms
                elif any(keyword in filename_lower for keyword in keywords['uniforms']):
                    categories['uniforms'].append(file_path.name)
                    categorized = True
                
                # Check for scholarships
                elif any(keyword in filename_lower for keyword in keywords['scholarships']):
                    categories['scholarships'].append(file_path.name)
                    categorized = True
                
                # Check for moments of joy (priority check before general gallery)
                elif any(keyword in filename_lower for keyword in keywords['moments_of_joy']):
                    categories['moments_of_joy'].append(file_path.name)
                    categorized = True
                
                # Add to gallery if it contains education-related keywords
                if any(keyword in filename_lower for keyword in keywords['gallery']):
                    if not categorized:  # Only add if not already categorized
                        categories['gallery'].append(file_path.name)
                    categorized = True
                
                # If not categorized but seems education-related, add to gallery
                if not categorized:
                    # Check if it's likely an education image (has common patterns)
                    if 'student' in filename_lower or 'receiving' in filename_lower:
                        categories['gallery'].append(file_path.name)
    
    # Sort each category
    for category in categories:
        categories[category].sort()
    
    context = {
        'school_bags_images': categories['school_bags'],
        'stationery_images': categories['stationery'],
        'uniforms_images': categories['uniforms'],
        'scholarships_images': categories['scholarships'],
        'moments_of_joy_images': categories['moments_of_joy'],
        'gallery_images': categories['gallery'],
    }
    
    return render(request, 'main/smiles.html', context)