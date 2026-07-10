from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Post(models.Model):
    """Text, image, and video posts"""
    POST_TYPES = [
        ('post', 'Post'),
        ('reel', 'Reel'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(max_length=1000)
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    video = models.FileField(upload_to='posts/videos/', blank=True, null=True)
    post_type = models.CharField(max_length=10, choices=POST_TYPES, default='post')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Engagement
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    shares = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
    
    def __str__(self):
        return f"{self.user.username} - {self.content[:30]}"
    
    def get_likes_count(self):
        return self.likes.count()
    
    def get_comments_count(self):
        return self.comments.count()

class Comment(models.Model):
    """Comments on posts"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.content[:30]}"

class Reel(models.Model):
    """Video reels (short videos)"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reels')
    caption = models.TextField(max_length=500, blank=True)
    video = models.FileField(upload_to='reels/')
    is_active = models.BooleanField(default=True)
    likes = models.ManyToManyField(User, related_name='liked_reels', blank=True)
    views = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Reel'
        verbose_name_plural = 'Reels'
    
    def __str__(self):
        return f"{self.user.username} - Reel {self.id}"
    
    def get_likes_count(self):
        return self.likes.count()

class Story(models.Model):
    """Stories (24-hour disappearing content)"""
    BACKGROUND_TYPES = [
        ('solid', 'Solid Color'),
        ('gradient', 'Gradient'),
        ('image', 'Image Background'),
    ]
    
    FILTER_TYPES = [
        ('normal', 'Normal'),
        ('bright', 'Bright'),
        ('vintage', 'Vintage'),
        ('mono', 'Monochrome'),
        ('warm', 'Warm'),
        ('cool', 'Cool'),
        ('dramatic', 'Dramatic'),
    ]
    
    TEXT_SIZES = [
        ('small', 'Small'),
        ('medium', 'Medium'),
        ('large', 'Large'),
        ('xlarge', 'Extra Large'),
    ]
    
    TEXT_STYLES = [
        ('normal', 'Normal'),
        ('bold', 'Bold'),
        ('italic', 'Italic'),
        ('bold_italic', 'Bold Italic'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stories')
    image = models.ImageField(upload_to='stories/images/', blank=True, null=True)
    video = models.FileField(upload_to='stories/videos/', blank=True, null=True)
    content = models.TextField(max_length=200, blank=True)
    
    # Background settings - Allow null for fields that might not be used
    background_type = models.CharField(max_length=10, choices=BACKGROUND_TYPES, default='solid')
    background_color = models.CharField(max_length=20, blank=True, null=True, default='#1a237e')
    gradient_start = models.CharField(max_length=20, blank=True, null=True)
    gradient_end = models.CharField(max_length=20, blank=True, null=True)
    background_image = models.ImageField(upload_to='stories/backgrounds/', blank=True, null=True)
    
    # Filter & Effects
    filter_type = models.CharField(max_length=10, choices=FILTER_TYPES, default='normal')
    brightness = models.FloatField(default=1.0)
    contrast = models.FloatField(default=1.0)
    saturation = models.FloatField(default=1.0)
    blur = models.FloatField(default=0.0)
    
    # Text styling
    text_color = models.CharField(max_length=20, default='#ffffff')
    text_size = models.CharField(max_length=10, choices=TEXT_SIZES, default='large')
    text_style = models.CharField(max_length=20, choices=TEXT_STYLES, default='normal')
    
    # Text background
    text_background = models.BooleanField(default=False)
    text_bg_color = models.CharField(max_length=20, blank=True, null=True, default='rgba(0,0,0,0.5)')
    
    # Status
    is_active = models.BooleanField(default=True)
    views = models.ManyToManyField(User, related_name='viewed_stories', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Story'
        verbose_name_plural = 'Stories'
    
    def __str__(self):
        return f"{self.user.username} - Story ({self.created_at})"
    
    def is_expired(self):
        return timezone.now() > self.expires_at
    
    def get_views_count(self):
        return self.views.count()
    
    def get_filter_style(self):
        """Return CSS filter styles"""
        filters = []
        if self.filter_type == 'bright':
            filters.append('brightness(1.3) contrast(1.1)')
        elif self.filter_type == 'vintage':
            filters.append('brightness(0.9) contrast(1.2) sepia(0.3)')
        elif self.filter_type == 'mono':
            filters.append('grayscale(1) brightness(1.1) contrast(1.2)')
        elif self.filter_type == 'warm':
            filters.append('brightness(1.1) saturate(1.2) hue-rotate(-10deg)')
        elif self.filter_type == 'cool':
            filters.append('brightness(1.1) saturate(1.1) hue-rotate(20deg)')
        elif self.filter_type == 'dramatic':
            filters.append('contrast(1.4) brightness(0.9) saturate(1.3)')
        else:
            filters.append(f'brightness({self.brightness}) contrast({self.contrast}) saturate({self.saturation})')
        
        if self.blur > 0:
            filters.append(f'blur({self.blur}px)')
        
        return ' '.join(filters)
