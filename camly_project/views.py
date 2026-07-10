from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import Profile
from posts.models import Post, Reel, Story
from django.utils import timezone
import os

def home(request):
    # If user is logged in, show feed
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = Profile.objects.create(user=request.user, user_type='student')
        
        # Get posts
        try:
            posts = Post.objects.filter(is_active=True).order_by('-created_at')
        except Exception as e:
            posts = []
            print(f"Error fetching posts: {e}")
        
        # Get reels - only those with video files
        try:
            reels = []
            all_reels = Reel.objects.filter(is_active=True).order_by('-created_at')[:10]
            for reel in all_reels:
                # Check if video file exists
                if reel.video and hasattr(reel.video, 'url') and reel.video.url:
                    reels.append(reel)
        except Exception as e:
            reels = []
            print(f"Error fetching reels: {e}")
        
        # Get active stories (not expired)
        try:
            stories = Story.objects.filter(
                is_active=True,
                expires_at__gt=timezone.now()
            ).order_by('-created_at')
        except Exception as e:
            stories = []
            print(f"Error fetching stories: {e}")
        
        context = {
            'user_profile': profile,
            'user_type': profile.user_type,
            'posts': posts,
            'reels': reels,
            'stories': stories,
        }
        return render(request, 'home.html', context)
    
    # Show public homepage for non-logged-in users
    return render(request, 'home.html')

def login_redirect(request):
    """Redirect to the actual login page"""
    return redirect('accounts:login')

def custom_404(request, exception):
    return render(request, '404.html', status=404)
