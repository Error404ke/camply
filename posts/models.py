from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Story(models.Model):
    """Stories (24-hour disappearing content)"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stories')
    image = models.ImageField(upload_to='stories/images/', blank=True, null=True)
    video = models.FileField(upload_to='stories/videos/', blank=True, null=True)
    content = models.TextField(max_length=200, blank=True)
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
