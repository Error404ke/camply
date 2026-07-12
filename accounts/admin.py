from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'full_name', 'user_type', 'is_staff')
    list_filter = ('user_type', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'full_name')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('user_type', 'full_name', 'bio', 'profile_picture', 
                                       'course', 'year_of_study', 'student_id',
                                       'company_name', 'phone', 'location', 'verified',
                                       'show_email', 'show_phone', 'visibility')}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile)
