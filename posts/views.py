from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from datetime import timedelta
from .models import Post, Comment, Reel, Story

@login_required
def create_post(request):
    """Create a new post or reel"""
    if request.method == 'POST':
        content = request.POST.get('content')
        post_type = request.POST.get('post_type', 'post')
        image = request.FILES.get('image')
        video = request.FILES.get('video')
        
        if not content and not image and not video:
            messages.error(request, 'Please add content or media to your post.')
            return redirect('posts:create_post')
        
        post = Post.objects.create(
            user=request.user,
            content=content or '',
            post_type=post_type,
            image=image,
            video=video
        )
        
        messages.success(request, 'Your post has been published!')
        return redirect('home')
    
    return render(request, 'posts/create_post.html')

@login_required
def create_reel(request):
    """Create a new reel"""
    if request.method == 'POST':
        caption = request.POST.get('caption', '')
        video = request.FILES.get('video')
        
        if not video:
            messages.error(request, 'Please upload a video for your reel.')
            return redirect('posts:create_reel')
        
        reel = Reel.objects.create(
            user=request.user,
            caption=caption,
            video=video
        )
        
        messages.success(request, 'Your reel has been published!')
        return redirect('home')
    
    return render(request, 'posts/create_reel.html')

@login_required
def create_story(request):
    """Create a new story with background, filters, and effects"""
    if request.method == 'POST':
        content = request.POST.get('content', '')
        media = request.FILES.get('media')
        background_image = request.FILES.get('background_image')
        
        background_type = request.POST.get('background_type', 'solid')
        background_color = request.POST.get('background_color', '#1a237e')
        gradient_start = request.POST.get('gradient_start')
        gradient_end = request.POST.get('gradient_end')
        
        filter_type = request.POST.get('filter_type', 'normal')
        brightness = float(request.POST.get('brightness', 1.0))
        contrast = float(request.POST.get('contrast', 1.0))
        saturation = float(request.POST.get('saturation', 1.0))
        blur = float(request.POST.get('blur', 0.0))
        
        text_color = request.POST.get('text_color', '#ffffff')
        text_size = request.POST.get('text_size', 'large')
        text_style = request.POST.get('text_style', 'normal')
        text_background = request.POST.get('text_background') == 'on'
        text_bg_color = request.POST.get('text_bg_color', 'rgba(0,0,0,0.5)')
        
        expires_at = timezone.now() + timedelta(hours=24)
        
        image = None
        video = None
        if media:
            if media.content_type and media.content_type.startswith('image/'):
                image = media
            elif media.content_type and media.content_type.startswith('video/'):
                video = media
        
        story = Story.objects.create(
            user=request.user,
            image=image,
            video=video,
            content=content,
            expires_at=expires_at,
            background_type=background_type,
            background_color=background_color if background_type == 'solid' else None,
            gradient_start=gradient_start if background_type == 'gradient' else None,
            gradient_end=gradient_end if background_type == 'gradient' else None,
            background_image=background_image if background_type == 'image' else None,
            filter_type=filter_type,
            brightness=brightness,
            contrast=contrast,
            saturation=saturation,
            blur=blur,
            text_color=text_color,
            text_size=text_size,
            text_style=text_style,
            text_background=text_background,
            text_bg_color=text_bg_color,
        )
        
        messages.success(request, 'Your story has been posted!')
        return redirect('home')
    
    return render(request, 'posts/create_story.html')

@login_required
def like_post(request, post_id):
    """Like or unlike a post"""
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    
    if user in post.likes.all():
        post.likes.remove(user)
        liked = False
    else:
        post.likes.add(user)
        liked = True
    
    return JsonResponse({
        'liked': liked,
        'likes_count': post.get_likes_count()
    })

@login_required
def like_reel(request, reel_id):
    """Like or unlike a reel"""
    reel = get_object_or_404(Reel, id=reel_id)
    user = request.user
    
    if user in reel.likes.all():
        reel.likes.remove(user)
        liked = False
    else:
        reel.likes.add(user)
        liked = True
    
    return JsonResponse({
        'liked': liked,
        'likes_count': reel.get_likes_count()
    })

@login_required
@require_POST
def add_comment(request, post_id):
    """Add a comment to a post"""
    post = get_object_or_404(Post, id=post_id)
    content = request.POST.get('content')
    
    if content:
        comment = Comment.objects.create(
            post=post,
            user=request.user,
            content=content
        )
        return JsonResponse({
            'success': True,
            'username': request.user.username,
            'content': content,
            'created_at': comment.created_at.strftime('%b %d, %Y %H:%M')
        })
    
    return JsonResponse({'success': False, 'error': 'Comment cannot be empty'})

@login_required
def view_story(request, story_id):
    """View a story (add to views)"""
    story = get_object_or_404(Story, id=story_id, is_active=True)
    
    if story.is_expired():
        return JsonResponse({'error': 'Story has expired'}, status=400)
    
    if request.user not in story.views.all():
        story.views.add(request.user)
    
    return JsonResponse({
        'success': True,
        'views': story.get_views_count(),
        'username': story.user.username,
        'content': story.content,
        'image_url': story.image.url if story.image else None,
        'video_url': story.video.url if story.video else None,
        'filter_style': story.get_filter_style(),
        'background': {
            'type': story.background_type,
            'color': story.background_color,
            'gradient_start': story.gradient_start,
            'gradient_end': story.gradient_end,
            'image_url': story.background_image.url if story.background_image else None,
        },
        'text_style': {
            'color': story.text_color,
            'size': story.text_size,
            'style': story.text_style,
            'background': story.text_background,
            'bg_color': story.text_bg_color,
        }
    })

@login_required
def delete_story(request, story_id):
    """Delete a story"""
    story = get_object_or_404(Story, id=story_id, user=request.user)
    story.is_active = False
    story.save()
    return JsonResponse({'success': True})

@login_required
def get_user_stories(request, user_id):
    """Get all stories for a specific user"""
    from django.contrib.auth.models import User
    user = get_object_or_404(User, id=user_id)
    
    stories = Story.objects.filter(
        user=user,
        is_active=True,
        expires_at__gt=timezone.now()
    ).order_by('created_at')
    
    story_data = []
    for story in stories:
        story_data.append({
            'id': story.id,
            'username': story.user.username,
            'content': story.content,
            'image_url': story.image.url if story.image else None,
            'video_url': story.video.url if story.video else None,
            'views': story.get_views_count(),
            'background': {
                'type': story.background_type,
                'color': story.background_color,
                'gradient_start': story.gradient_start,
                'gradient_end': story.gradient_end,
                'image_url': story.background_image.url if story.background_image else None,
            },
            'filter_style': story.get_filter_style(),
            'text_style': {
                'color': story.text_color,
                'size': story.text_size,
                'style': story.text_style,
                'background': story.text_background,
                'bg_color': story.text_bg_color,
            }
        })
    
    return JsonResponse({
        'success': True,
        'stories': story_data,
        'user': {
            'id': user.id,
            'username': user.username,
            'profile_picture': user.profile.profile_picture.url if hasattr(user, 'profile') and user.profile.profile_picture else None,
        }
    })

def get_stories(request):
    """Get all active stories for the current user (public endpoint)"""
    stories = Story.objects.filter(
        is_active=True,
        expires_at__gt=timezone.now()
    ).order_by('-created_at')
    
    story_data = []
    for story in stories:
        story_data.append({
            'id': story.id,
            'username': story.user.username,
            'content': story.content,
            'image_url': story.image.url if story.image else None,
            'video_url': story.video.url if story.video else None,
            'created_at': story.created_at.strftime('%I:%M %p'),
            'views': story.get_views_count(),
        })
    
    return JsonResponse({'stories': story_data})
