from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    USER_TYPES = [
        ('student', 'Student'),
        ('landlord', 'Landlord'),
    ]
    
    PRIVACY_CHOICES = [
        ('public', 'Everyone'),
        ('friends', 'Friends Only'),
        ('private', 'Only Me'),
    ]
    
    # Basic Info
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='student')
    full_name = models.CharField(max_length=200, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    
    # Student Fields
    course = models.CharField(max_length=100, blank=True)
    year_of_study = models.IntegerField(null=True, blank=True)
    student_id = models.CharField(max_length=50, blank=True, null=True)
    
    # Landlord Fields
    company_name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    location = models.CharField(max_length=200, blank=True)
    verified = models.BooleanField(default=False)
    
    # Privacy
    show_email = models.BooleanField(default=True)
    show_phone = models.BooleanField(default=False)
    visibility = models.CharField(max_length=10, choices=PRIVACY_CHOICES, default='public')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.username
    
    @property
    def is_student(self):
        return self.user_type == 'student'
    
    @property
    def is_landlord(self):
        return self.user_type == 'landlord'
    
    @property
    def is_admin_user(self):
        return self.is_superuser or self.is_staff

class Profile(models.Model):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, related_name='profile')
    
    def __str__(self):
        return f"{self.user.username}'s profile"
