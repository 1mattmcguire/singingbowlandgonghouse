from django.db import models
from django.core.validators import EmailValidator


class Booking(models.Model):
    SERVICE_TYPE_CHOICES = [
        ('personal', 'Personal Sound Healing'),
        ('group', 'Group Sound Healing'),
        ('singing_bowl', 'Singing Bowl Course'),
        ('gong', 'Gong Course'),
        ('handpan', 'Handpan Course'),
    ]
    
    SESSION_TYPE_CHOICES = [
        ('One to One', 'One to One'),
        ('Group Session', 'Group Session'),
    ]
    
    name = models.CharField(max_length=200)
    email = models.EmailField(validators=[EmailValidator()])
    phone = models.CharField(max_length=20)
    service = models.CharField(max_length=50, choices=SERVICE_TYPE_CHOICES)
    booking_date = models.DateField()
    message = models.TextField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    session_type = models.CharField(max_length=20, choices=SESSION_TYPE_CHOICES, blank=True, null=True)
    course_selection = models.CharField(max_length=100, blank=True, null=True)
    medical_condition = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
    
    def __str__(self):
        return f"{self.name} - {self.service} - {self.booking_date}"


class Inquiry(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(validators=[EmailValidator()])
    phone = models.CharField(max_length=20, blank=True, null=True)
    subject = models.CharField(max_length=200, blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Inquiry'
        verbose_name_plural = 'Inquiries'
    
    def __str__(self):
        return f"{self.name} - {self.subject or 'No Subject'} - {self.created_at.strftime('%Y-%m-%d')}"
