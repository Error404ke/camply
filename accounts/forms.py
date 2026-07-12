from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.files.base import ContentFile
import base64
from .models import User

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    full_name = forms.CharField(max_length=200, required=True)
    profile_picture = forms.ImageField(required=False)
    user_type = forms.ChoiceField(
        choices=[
            ('student', 'Student'),
            ('landlord', 'Landlord'),
        ],
        required=True
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'full_name', 'user_type', 'profile_picture', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.full_name = self.cleaned_data['full_name']
        user.user_type = self.cleaned_data['user_type']
        
        if commit:
            user.save()
            # Handle profile picture separately after user is saved
            if self.cleaned_data.get('profile_picture'):
                try:
                    # Save the file directly
                    profile_pic = self.cleaned_data['profile_picture']
                    user.profile_picture.save(profile_pic.name, profile_pic, save=True)
                except Exception as e:
                    print(f"Error saving profile picture: {e}")
        return user
