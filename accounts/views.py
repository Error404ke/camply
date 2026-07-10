from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .models import Profile
from .forms import StudentRegistrationForm, LandlordRegistrationForm

# ===== DECORATORS =====

def role_required(allowed_roles):
    """Decorator to check user role"""
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('accounts:login')
            try:
                profile = Profile.objects.get(user=request.user)
                if request.user.is_superuser:
                    return view_func(request, *args, **kwargs)
                if profile.user_type not in allowed_roles:
                    messages.error(request, 'You do not have permission to access this page.')
                    return redirect('home')
            except Profile.DoesNotExist:
                profile = Profile.objects.create(user=request.user, user_type='student')
                if 'student' not in allowed_roles:
                    messages.error(request, 'You do not have permission to access this page.')
                    return redirect('home')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

# ===== AUTH VIEWS =====

@csrf_protect
def login_view(request):
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
            return redirect(profile.get_dashboard_url())
        except Profile.DoesNotExist:
            profile = Profile.objects.create(user=request.user, user_type='student')
            return redirect('accounts:student_dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            try:
                profile = Profile.objects.get(user=user)
                return redirect(profile.get_dashboard_url())
            except Profile.DoesNotExist:
                profile = Profile.objects.create(user=user, user_type='student')
                return redirect('accounts:student_dashboard')
        messages.error(request, 'Invalid username or password')
    
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('accounts:login')

@csrf_protect
def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    user_type = request.GET.get('type', 'student')
    
    # Only allow student and landlord registration through public forms
    if user_type == 'admin':
        messages.error(request, 'Admin accounts can only be created by superusers.')
        return redirect('accounts:register')
    
    if user_type == 'landlord':
        form_class = LandlordRegistrationForm
        template = 'accounts/register_landlord.html'
    else:
        form_class = StudentRegistrationForm
        template = 'accounts/register_student.html'
    
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            
            # Create user
            user = User.objects.create_user(username=username, email=email, password=password)
            
            # Create profile with role-specific data
            profile = Profile.objects.create(user=user, user_type=user_type)
            
            # Common fields
            profile.full_name = form.cleaned_data.get('full_name', '')
            profile.phone_number = form.cleaned_data.get('phone_number', '')
            
            # Role-specific fields
            if user_type == 'student':
                profile.student_id = form.cleaned_data.get('student_id', '')
                profile.course = form.cleaned_data.get('course', '')
                profile.year_of_study = form.cleaned_data.get('year_of_study')
                
            elif user_type == 'landlord':
                profile.company_name = form.cleaned_data.get('company_name', '')
                profile.company_registration = form.cleaned_data.get('company_registration', '')
                profile.id_number = form.cleaned_data.get('id_number', '')
                profile.address = form.cleaned_data.get('address', '')
                profile.is_approved = False
                messages.info(request, 'Your landlord account is pending approval by an admin.')
            
            profile.save()
            
            # Log the user in
            login(request, user)
            messages.success(request, f'Welcome to Camly! You are registered as {profile.get_user_type_display()}.')
            
            return redirect(profile.get_dashboard_url())
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = form_class()
    
    context = {
        'form': form,
        'user_type': user_type,
        'title': f'Register as {user_type.title()}',
    }
    return render(request, template, context)

# ===== PROFILE VIEWS =====

@login_required
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    try:
        profile = user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=user, user_type='student')
    
    viewer = request.user
    
    can_view_email = profile.email_privacy == 'public' or viewer == user
    can_view_location = profile.location_privacy == 'public' or viewer == user
    can_view_year = profile.year_privacy == 'public' or viewer == user
    can_view_phone = profile.phone_privacy == 'public' or viewer == user
    
    context = {
        'profile_user': user,
        'can_view_email': can_view_email,
        'can_view_location': can_view_location,
        'can_view_year': can_view_year,
        'can_view_phone': can_view_phone,
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def edit_profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user, user_type='student')
    
    if request.method == 'POST':
        profile.bio = request.POST.get('bio', '')
        profile.location = request.POST.get('location', '')
        profile.theme = request.POST.get('theme', 'light')
        
        profile.email_privacy = request.POST.get('email_privacy', 'private')
        profile.location_privacy = request.POST.get('location_privacy', 'friends')
        profile.year_privacy = request.POST.get('year_privacy', 'friends')
        profile.phone_privacy = request.POST.get('phone_privacy', 'private')
        
        if request.FILES.get('profile_picture'):
            profile.profile_picture = request.FILES.get('profile_picture')
        
        if profile.user_type == 'student':
            profile.course = request.POST.get('course', '')
            profile.year_of_study = request.POST.get('year_of_study') or None
            profile.student_id = request.POST.get('student_id', '')
        elif profile.user_type == 'landlord':
            profile.company_name = request.POST.get('company_name', '')
            profile.company_registration = request.POST.get('company_registration', '')
            profile.id_number = request.POST.get('id_number', '')
            profile.phone_number = request.POST.get('phone_number', '')
            profile.address = request.POST.get('address', '')
        
        profile.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('accounts:profile', username=request.user.username)
    
    return render(request, 'accounts/edit_profile.html', {'profile': profile})

# ===== DASHBOARD VIEWS =====

@login_required
@role_required(['student'])
def student_dashboard(request):
    return render(request, 'dashboards/student.html')

@login_required
@role_required(['landlord'])
def landlord_dashboard(request):
    try:
        profile = request.user.profile
        if not profile.is_approved and not request.user.is_superuser:
            messages.warning(request, 'Your landlord account is pending approval.')
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user, user_type='student')
    return render(request, 'dashboards/landlord.html')

@login_required
@role_required(['admin', 'superuser'])
def admin_dashboard(request):
    return render(request, 'dashboards/admin.html')

@login_required
@role_required(['superuser'])
def superuser_dashboard(request):
    return render(request, 'dashboards/superuser.html')

@login_required
@role_required(['admin', 'superuser'])
def manage_users(request):
    users = User.objects.all()
    return render(request, 'admin_panel/manage_users.html', {'users': users})

@login_required
@role_required(['admin', 'superuser'])
def manage_landlords(request):
    landlords = Profile.objects.filter(user_type='landlord')
    return render(request, 'admin_panel/manage_landlords.html', {'landlords': landlords})

@login_required
@role_required(['admin', 'superuser'])
def approve_landlord(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    if profile.user_type == 'landlord':
        profile.is_approved = True
        profile.save()
        messages.success(request, f'Landlord {profile.user.username} approved successfully!')
    return redirect('accounts:manage_landlords')
