from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                user = form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, f'Account created for {username}! You can now login.')
                return redirect('accounts:login')
            except Exception as e:
                messages.error(request, f'Error creating account: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

@login_required
def profile_edit(request):
    if request.method == 'POST':
        user = request.user
        user.email = request.POST.get('email')
        user.full_name = request.POST.get('full_name')
        user.course = request.POST.get('course')
        user.year_of_study = request.POST.get('year_of_study')
        user.location = request.POST.get('location')
        if request.FILES.get('profile_picture'):
            try:
                user.profile_picture = request.FILES['profile_picture']
            except Exception as e:
                messages.error(request, f'Error uploading profile picture: {str(e)}')
        user.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('accounts:profile')
    
    return render(request, 'accounts/profile_edit.html')
