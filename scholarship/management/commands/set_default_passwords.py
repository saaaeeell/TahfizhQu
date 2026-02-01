from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Set default password "password123" for all users (Student, Examiner, Admin, Superuser)'

    def handle(self, *args, **options):
        default_password = 'password123'
        
        # Get all users
        users = User.objects.all()
        
        if not users.exists():
            self.stdout.write(self.style.WARNING('No users found in the database'))
            return
        
        updated_count = 0
        
        for user in users:
            user.set_password(default_password)
            user.save()
            updated_count += 1
            self.stdout.write(
                self.style.SUCCESS(
                    f'✓ Updated {user.username} (role: {user.role})'
                )
            )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n✓ Successfully updated password for {updated_count} users to "{default_password}"'
            )
        )
