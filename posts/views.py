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
    """Create a new story"""
    if request.method == 'POST':
        content = request.POST.get('content', '')
        image = request.FILES.get('image')
        video = request.FILES.get('video')
        
        if not image and not video and not content:
            messages.error(request, 'Please add content to your story.')
            return redirect('posts:create_story')
        
        # Story expires in 24 hours
        expires_at = timezone.now() + timedelta(hours=24)
        
        story = Story.objects.create(
            user=request.user,
            image=image,
            video=video,
            content=content,
            expires_at=expires_at
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
    if request.user not in story.views.all():
        story.views.add(request.user)
    return JsonResponse({'views': story.get_views_count()})

@login_required
def delete_story(request, story_id):
    """Delete a story"""
    story = get_object_or_404(Story, id=story_id, user=request.user)
    story.is_active = False
    story.save()
    return JsonResponse({'success': True})
