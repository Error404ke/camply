from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Profile

class Command(BaseCommand):
    help = 'Create profiles for users who don\'t have one'

    def handle(self, *args, **options):
        users = User.objects.all()
        created_count = 0
        
        for user in users:
            try:
                profile = Profile.objects.get(user=user)
                self.stdout.write(f'✓ Profile exists for {user.username}')
            except Profile.DoesNotExist:
                Profile.objects.create(user=user, user_type='student')
                created_count += 1
                self.stdout.write(f'✓ Created profile for {user.username}')
        
        self.stdout.write(self.style.SUCCESS(f'\n✅ Created {created_count} profiles for users who were missing them.'))
