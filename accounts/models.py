from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    USER_TYPES = [
        ('student', 'Student'),
        ('landlord', 'Landlord'),
        ('admin', 'Admin'),
        ('superuser', 'Superuser'),
    ]
    
    PRIVACY_CHOICES = [
        ('public', 'Everyone'),
        ('friends', 'Friends Only'),
        ('private', 'Only Me'),
    ]
    
    # Basic Info
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='student')
    full_name = models.CharField(max_length=200, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    
    # Student Fields
    course = models.CharField(max_length=100, blank=True)
    year_of_study = models.IntegerField(null=True, blank=True)
    student_id = models.CharField(max_length=50, blank=True, null=True)
    
    # Landlord Fields
    company_name = models.CharField(max_length=200, blank=True, null=True)
    company_registration = models.CharField(max_length=100, blank=True, null=True)
    id_number = models.CharField(max_length=20, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    property_count = models.IntegerField(default=0)
    rating = models.FloatField(default=0.0)
    
    # Admin Fields
    department = models.CharField(max_length=100, blank=True, null=True)
    staff_id = models.CharField(max_length=50, blank=True, null=True)
    
    # Location
    location = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    county = models.CharField(max_length=100, blank=True, null=True)
    
    # Privacy Settings
    email_privacy = models.CharField(max_length=10, choices=PRIVACY_CHOICES, default='private')
    location_privacy = models.CharField(max_length=10, choices=PRIVACY_CHOICES, default='friends')
    year_privacy = models.CharField(max_length=10, choices=PRIVACY_CHOICES, default='friends')
    phone_privacy = models.CharField(max_length=10, choices=PRIVACY_CHOICES, default='private')
    
    # Theme Preference
    theme = models.CharField(max_length=10, default='light', choices=[('light', 'Light'), ('dark', 'Dark')])
    
    # Notification Preferences
    email_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)
    
    # Verification
    is_verified = models.BooleanField(default=False)
    verification_documents = models.FileField(upload_to='verifications/', null=True, blank=True)
    
    # Status
    is_online = models.BooleanField(default=False)
    last_active = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_user_type_display()}"

    def get_user_type_display(self):
        return dict(self.USER_TYPES).get(self.user_type, 'Student')
    
    def is_student(self):
        return self.user_type == 'student'
    
    def is_landlord(self):
        return self.user_type == 'landlord'
    
    def is_admin(self):
        return self.user_type == 'admin' or self.user.is_superuser
    
    def is_superuser(self):
        return self.user.is_superuser
    
    def get_dashboard_url(self):
        if self.is_superuser():
            return '/accounts/dashboard/superuser/'
        elif self.is_admin():
            return '/accounts/dashboard/admin/'
        elif self.is_landlord():
            return '/accounts/dashboard/landlord/'
        else:
            return '/accounts/dashboard/student/'
    
    def get_full_name(self):
        return self.full_name or self.user.username
