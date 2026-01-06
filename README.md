# Singing Bowl & Gong House - Django Project

A full-featured Django web application for the Singing Bowl & Gong House, featuring booking and inquiry forms with email notifications.

## Project Structure

```
SingingBallAndGongHouse/
├── SingingBallAndGongHouse/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── main/
│   ├── templates/main/
│   │   ├── home.html
│   │   ├── about.html
│   │   ├── services.html
│   │   ├── courses.html
│   │   ├── contact.html
│   │   └── success.html
│   ├── static/main/
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
├── manage.py
├── requirements.txt
└── README.md
```

## Features

- **Home Page**: Beautiful landing page with hero section, founder's journey, and instrument showcase
- **About Page**: Information about the center and its mission
- **Services Page**: Details about sound healing services and training courses
- **Courses Page**: Information about available courses
- **Contact Page**: Contact form for inquiries
- **Booking System**: Full booking form with service selection, date picker, and medical information
- **Email Notifications**: Automatic thank-you emails to users and notification emails to admin
- **Django Admin**: Full admin interface for managing bookings and inquiries with filtering and search

## Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Run Migrations

Create the database tables:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 3: Create Superuser

Create an admin account to access the Django admin panel:

```bash
python manage.py createsuperuser
```

Follow the prompts to set:
- Username
- Email address
- Password

### Step 4: Collect Static Files

Collect all static files (CSS, JS, images) into the staticfiles directory:

```bash
python manage.py collectstatic --noinput
```

### Step 5: Run the Development Server

Start the Django development server:

```bash
python manage.py runserver
```

The application will be available at: `http://127.0.0.1:8000/`

## Access Points

- **Home**: http://127.0.0.1:8000/
- **About**: http://127.0.0.1:8000/about/
- **Services**: http://127.0.0.1:8000/services/
- **Courses**: http://127.0.0.1:8000/courses/
- **Contact**: http://127.0.0.1:8000/contact/
- **Booking**: http://127.0.0.1:8000/booking/ (or use "Book Now" button)
- **Success Page**: http://127.0.0.1:8000/success/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## Email Configuration

### Development

By default, if `EMAIL_HOST_PASSWORD` is **not** set, the app uses Django’s **console email backend** (emails print to the server console). This is ideal for local development.

### Production Setup (Recommended)

**Do not hardcode secrets in `settings.py`.** Configure these environment variables instead (see `.env.example`):

- `SECRET_KEY`
- `DEBUG` (set to `0` in production)
- `ALLOWED_HOSTS`
- `EMAIL_HOST_USER`
- `EMAIL_HOST_PASSWORD` (Gmail App Password)
- `DEFAULT_FROM_EMAIL`
- `ADMIN_EMAIL`

**Note**: For Gmail, you'll need to:
1. Enable 2-factor authentication
2. Generate an "App Password" (not your regular password)
3. Use the app password in `EMAIL_HOST_PASSWORD`

## Email Notifications

### User Confirmation Email

When a user submits a booking, they automatically receive a confirmation email with:
- Thank you message
- Complete booking details
- Booking reference number
- Contact information

### Admin Notification Email

You (admin) receive an email notification with:
- Customer information
- Complete booking details
- Medical conditions/needs
- Booking reference number
- Submission timestamp

## WhatsApp Notifications

### Current Setup

When a booking is received, a WhatsApp notification link is generated and printed to the console. You can:
1. Check the console/terminal where Django is running
2. Copy the WhatsApp link
3. Open it in your browser
4. WhatsApp will open with a pre-filled message
5. Click send to deliver the notification

### Automated WhatsApp (Optional)

For automated WhatsApp notifications (messages sent automatically), see `WHATSAPP_SETUP.md` for detailed instructions on setting up:
- Twilio WhatsApp API
- WhatsApp Business API
- Other automation options

**Your WhatsApp Number:** +977 984-3213802 (configured in settings.py)

## Models

### Booking Model

Fields:
- `name` (CharField): Full name of the customer
- `email` (EmailField): Customer email address
- `phone` (CharField): Phone number
- `service` (CharField): Service type (choices: personal, group, singing_bowl, gong, handpan)
- `booking_date` (DateField): Preferred booking date
- `message` (TextField): Additional message (optional)
- `age` (IntegerField): Customer age (optional)
- `session_type` (CharField): One to One or Group Session (optional)
- `course_selection` (CharField): Selected course if applicable (optional)
- `medical_condition` (TextField): Medical conditions or specific needs (optional)
- `created_at` (DateTimeField): Timestamp of submission

### Inquiry Model

Fields:
- `name` (CharField): Full name
- `email` (EmailField): Email address
- `phone` (CharField): Phone number (optional)
- `subject` (CharField): Inquiry subject (optional)
- `message` (TextField): Inquiry message
- `created_at` (DateTimeField): Timestamp of submission

## Django Admin Features

The admin panel provides:

- **List View**: See all bookings and inquiries in a table
- **Filtering**: Filter by service type, session type, booking date, creation date
- **Search**: Search by name, email, phone, message, course selection
- **Date Hierarchy**: Navigate by date
- **Edit/Delete**: Full CRUD operations on all records
- **Fieldsets**: Organized form fields for easy editing

## API Endpoints

The project includes API endpoints for AJAX form submissions:

- `POST /api/bookings/public/` - Submit booking form
- `POST /api/contact/` - Submit inquiry/contact form

Both endpoints return JSON responses:
- Success: `{"success": true, "message": "..."}`
- Error: `{"success": false, "errors": {...}}` or `{"success": false, "error": "..."}`

## Static Files

All static files are organized in `main/static/main/`:

- **CSS**: `main/static/main/css/` - All stylesheet files
- **JavaScript**: `main/static/main/js/` - All JavaScript files
- **Images**: `main/static/main/images/` - All image files

## Troubleshooting

### Static files not loading

1. Make sure you've run `python manage.py collectstatic`
2. Check that `DEBUG = True` in settings.py (for development)
3. Verify static files are in `main/static/main/` directories

### Email not sending

1. Check email backend configuration in settings.py
2. For production, verify SMTP credentials
3. Check console output for email errors (in development mode)

### Database errors

1. Make sure migrations are up to date: `python manage.py migrate`
2. Check that SQLite database file exists: `db.sqlite3`

### Admin access issues

1. Verify superuser was created: `python manage.py createsuperuser`
2. Check username and password are correct
3. Ensure you're accessing `/admin/` URL

## Development Notes

- The project uses SQLite database by default (development)
- For production, consider switching to PostgreSQL or MySQL
- Update `ALLOWED_HOSTS` in settings.py for production deployment
- Set `DEBUG = False` in production
- Use environment variables for sensitive settings (SECRET_KEY, database credentials, etc.)

## Support

For issues or questions, please contact: singingbowlandgonghouse@gmail.com

## License

Copyright © 2024 Singing Bowl & Gong House. All rights reserved.



