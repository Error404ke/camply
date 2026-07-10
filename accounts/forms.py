from django import forms
from django.contrib.auth.models import User
from .models import Profile

class StudentRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'glass-input', 'placeholder': 'Choose a username'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'glass-input', 'placeholder': 'Enter your email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'glass-input', 'placeholder': 'Create a password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'glass-input', 'placeholder': 'Confirm password'}))
    
    full_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'glass-input', 'placeholder': 'Enter your full name'}))
    student_id = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'glass-input', 'placeholder': 'Enter your student ID'}))
    course = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'glass-input', 'placeholder': 'Enter your course'}))
    year_of_study = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'class': 'glass-input', 'placeholder': 'Year of study (1-6)'}))
    phone_number = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'glass-input', 'placeholder': 'Phone number (optional)'}))
    
    class Meta:
        model = Profile
        fields = ['full_name', 'student_id', 'course', 'year_of_study', 'phone_number']
    
    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise forms.ValidationError('Passwords do not match')
        return password2

class LandlordRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'glass-input', 'placeholder': 'Choose a username'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'glass-input', 'placeholder': 'Enter your email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'glass-input', 'placeholder': 'Create a password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'glass-input', 'placeholder': 'Confirm password'}))
    
    full_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'glass-input', 'placeholder': 'Enter your full name'}))
    company_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'glass-input', 'placeholder': 'Company/Property name'}))
    company_registration = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'glass-input', 'placeholder': 'Business registration number'}))
    id_number = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'glass-input', 'placeholder': 'National ID/Passport number'}))
    phone_number = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'glass-input', 'placeholder': 'Phone number'}))
    address = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'glass-input', 'rows': 3, 'placeholder': 'Physical address'}))
    
    class Meta:
        model = Profile
        fields = ['full_name', 'company_name', 'company_registration', 'id_number', 'phone_number', 'address']
    
    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise forms.ValidationError('Passwords do not match')
        return password2

class AdminRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'glass-input', 'placeholder': 'Choose a username'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'glass-input', 'placeholder': 'Enter your email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'glass-input', 'placeholder': 'Create a password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'glass-input', 'placeholder': 'Confirm password'}))
    
    full_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'glass-input', 'placeholder': 'Enter your full name'}))
    staff_id = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'glass-input', 'placeholder': 'Staff ID'}))
    department = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'glass-input', 'placeholder': 'Department'}))
    phone_number = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'glass-input', 'placeholder': 'Phone number'}))
    
    class Meta:
        model = Profile
        fields = ['full_name', 'staff_id', 'department', 'phone_number']
    
    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise forms.ValidationError('Passwords do not match')
        return password2
