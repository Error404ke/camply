from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import UserRegisterForm

User = get_user_model()

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now login.')
            return redirect('accounts:login')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile_view(request, username=None):
    """View profile of a user"""
    if username:
        user = get_object_or_404(User, username=username)
    else:
        user = request.user
    
    context = {
        'profile_user': user,
        'is_own_profile': user == request.user,
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def profile_edit(request):
    """Edit profile page"""
    user = request.user
    if request.method == 'POST':
        # Update user fields
        user.full_name = request.POST.get('full_name', user.full_name)
        user.bio = request.POST.get('bio', user.bio)
        user.course = request.POST.get('course', user.course)
        user.year_of_study = request.POST.get('year_of_study', user.year_of_study)
        user.location = request.POST.get('location', user.location)
        user.user_type = request.POST.get('user_type', user.user_type)
        
        # Handle profile picture
        if request.FILES.get('profile_picture'):
            user.profile_picture = request.FILES['profile_picture']
        
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('accounts:profile')
    
    return render(request, 'accounts/profile_edit.html', {'user': user})

@login_required
def profile_settings(request):
    """Profile settings page"""
    return render(request, 'accounts/profile_settings.html')

@login_required
def profile_add_account(request):
    """Add account page"""
    return render(request, 'accounts/add_account.html')

@login_required
def logout_view(request):
    """Logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('accounts:login')
