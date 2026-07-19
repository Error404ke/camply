from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Story
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def story_list(request):
    users_with_stories = User.objects.filter(
        story_stories__is_active=True,  
        story_stories__expires_at__gt=timezone.now()
    ).distinct().exclude(id=request.user.id)
    
    story_rings = []
    for user in users_with_stories:
        first_story = Story.objects.filter(
            user=user,
            is_active=True,
            expires_at__gt=timezone.now()
        ).first()
        
        story_count = Story.objects.filter(
            user=user,
            is_active=True,
            expires_at__gt=timezone.now()
        ).count()
        
        story_rings.append({
            'user': user,
            'thumbnail': first_story.image.url if first_story and first_story.image else None,
            'first_story_id': first_story.id if first_story else None,
            'story_count': story_count,
        })
    
    return render(request, 'stories/story_list.html', {'story_rings': story_rings})

@login_required
def story_view(request, story_id):
    story = get_object_or_404(Story, id=story_id, is_active=True)
    user_stories = Story.objects.filter(
        user=story.user,
        is_active=True,
        expires_at__gt=timezone.now()
    )
    return render(request, 'stories/story_detail.html', {
        'current_story': story,
        'stories': user_stories,
    })

@login_required
def create_story(request):
    if request.method == 'POST' and request.FILES.get('image'):
        Story.objects.create(
            user=request.user,
            image=request.FILES['image'],
            caption=request.POST.get('caption', ''),
        )
        messages.success(request, 'Story created!')
        return redirect('stories:story_list')
    return render(request, 'stories/create_story.html')
