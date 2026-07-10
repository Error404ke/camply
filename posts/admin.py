from django.contrib import admin
from django.utils.html import mark_safe
from .models import Post, Comment, Reel

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['user', 'content_preview', 'post_type', 'get_likes_count', 'created_at']
    list_filter = ['post_type', 'is_active']
    search_fields = ['user__username', 'content']
    readonly_fields = ['created_at', 'updated_at']
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'content_preview', 'created_at']
    search_fields = ['user__username', 'content']
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'

@admin.register(Reel)
class ReelAdmin(admin.ModelAdmin):
    list_display = ['user', 'caption_preview', 'views', 'get_likes_count', 'created_at']
    list_filter = ['is_active']
    search_fields = ['user__username', 'caption']
    readonly_fields = ['created_at', 'updated_at']
    
    def caption_preview(self, obj):
        return obj.caption[:50] + '...' if len(obj.caption) > 50 else obj.caption
    caption_preview.short_description = 'Caption'
