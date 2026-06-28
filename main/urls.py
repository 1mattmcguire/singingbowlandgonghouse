from django.urls import path
from . import views
from django.contrib import admin
app_name = 'main'



urlpatterns = [
    path('admin/', admin.site.urls),
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



