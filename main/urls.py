from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('courses/', views.courses, name='courses'),
    path('contact/', views.contact, name='contact'),
    path('booking/', views.booking, name='booking'),
    path('success/', views.success, name='success'),
    path('smiles/', views.smiles, name='smiles'),
    
    # API endpoints
    path('api/bookings/public/', views.api_booking, name='api_booking'),
    path('api/contact/', views.api_inquiry, name='api_inquiry'),
    path('test-email/', views.test_email, name='test_email'),
]



