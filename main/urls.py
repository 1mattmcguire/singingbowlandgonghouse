from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path
from main.views import test_email 
app_name = 'main'



urlpatterns = [
    path('admin/', admin.site.urls),
    path('test-email/', test_email),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('products/', views.products, name='products'),
    path('booking/', views.booking, name='booking'),
    path('success/', views.success, name='success'),
    path('smiles/', views.smiles, name='smiles'),
    
    # API endpoints
    path('api/bookings/public/', views.api_booking, name='api_booking'),
]



