from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Ensure users with role=admin have is_staff=True'

    def add_arguments(self, parser):
        parser.add_argument('--apply', action='store_true', help='Apply changes (set is_staff=True)')

    def handle(self, *args, **options):
        User = get_user_model()
        admins = User.objects.filter(role='admin')
        if not admins.exists():
            self.stdout.write(self.style.NOTICE('No users with role=admin found.'))
            return

        self.stdout.write(self.style.MIGRATE_HEADING('Found users with role=admin:'))
        for u in admins:
            self.stdout.write(f' - {u.username}: is_staff={u.is_staff}, is_superuser={u.is_superuser}')

        if options.get('apply'):
            to_update = admins.filter(is_staff=False)
            count = to_update.update(is_staff=True)
            self.stdout.write(self.style.SUCCESS(f'Updated {count} users (is_staff=True)'))
        else:
            self.stdout.write('Run with --apply to set is_staff=True for users with role=admin')
