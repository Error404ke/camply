from django.contrib import admin
from .models import Story

@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'expires_at', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['user__username', 'caption']
    readonly_fields = ['created_at']
