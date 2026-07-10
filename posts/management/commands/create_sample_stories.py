from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from posts.models import Story

class Command(BaseCommand):
    help = 'Create sample stories for testing'

    def handle(self, *args, **options):
        user = User.objects.first()
        if not user:
            self.stdout.write(self.style.ERROR('No users found. Create a superuser first.'))
            return
        
        # Delete existing stories
        Story.objects.all().delete()
        
        # Create sample stories with different backgrounds
        stories_data = [
            {
                'content': 'Welcome to Camly! 🎉',
                'background_type': 'solid',
                'background_color': '#1a237e',
                'filter_type': 'normal',
            },
            {
                'content': 'Check out our campus!',
                'background_type': 'gradient',
                'gradient_start': '#e74c3c',
                'gradient_end': '#f39c12',
                'filter_type': 'warm',
            },
            {
                'content': 'Study groups are now available!',
                'background_type': 'solid',
                'background_color': '#2ecc71',
                'filter_type': 'bright',
            },
            {
                'content': 'New courses added for 2025',
                'background_type': 'gradient',
                'gradient_start': '#9b59b6',
                'gradient_end': '#3498db',
                'filter_type': 'cool',
            },
        ]
        
        for story_data in stories_data:
            story = Story.objects.create(
                user=user,
                content=story_data['content'],
                background_type=story_data['background_type'],
                background_color=story_data.get('background_color'),
                gradient_start=story_data.get('gradient_start'),
                gradient_end=story_data.get('gradient_end'),
                filter_type=story_data.get('filter_type', 'normal'),
                expires_at=timezone.now() + timedelta(hours=24),
                is_active=True
            )
            self.stdout.write(self.style.SUCCESS(f'Created story: {story.content[:30]}...'))
        
        self.stdout.write(self.style.SUCCESS(f'\n✅ Created {len(stories_data)} sample stories!'))
