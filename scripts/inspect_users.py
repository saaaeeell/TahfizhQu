import os, sys
from pathlib import Path
import django

# Ensure project root is on sys.path so Django can be imported reliably
proj_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(proj_root))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tahfizhqu.settings')
django.setup()

from scholarship.models import User, Student, Examiner

usernames = ['bintang37a', '22040700020', 'bintang25a']

for username in usernames:
    try:
        u = User.objects.get(username=username)
        print('---')
        print('Username:', u.username)
        print('ID:', u.id)
        print('Email:', u.email)
        print('Role:', u.role)
        print('is_active:', u.is_active)
        print('is_staff:', u.is_staff)
        print('is_superuser:', u.is_superuser)
        print('Password (hashed):', u.password)
        # related student or examiner
        students = u.applications.all()
        for s in students:
            print('  Student:', s.nama, 'is_verified=', s.is_verified)
        try:
            ex = u.examiner_profile
            print('  Examiner profile:', ex.nama)
        except Examiner.DoesNotExist:
            pass
    except User.DoesNotExist:
        print('---')
        print('User', username, 'does not exist')
