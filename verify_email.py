from django.conf import settings
from django.core import mail
from django.test import Client, override_settings
from django.contrib.auth import get_user_model
from scholarship.models import Student

# Override email backend to capture emails in mail.outbox
settings.EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

User = get_user_model()
try:
    user = User.objects.create_user(username='teststudent_email_2', email='test_email_2@example.com', password='password', role='student')
except:
    user = User.objects.get(username='teststudent_email_2')

client = Client()
client.login(username='teststudent_email_2', password='password')

response = client.post('/apply/', {
    'nama': 'Test Student',
    'tanggal_lahir': '2000-01-01',
    'kampus': 'UMJ',
    'asal_sekolah': 'SMA 1',
    'fakultas': 'Teknik',
    'jurusan': 'Informatika',
    'jumlah_hafalan': 5,
    'nim': '1122334455', 
    'ipk': 3.5, 
    'semester': 3
})

print(f"Response Status: {response.status_code}")
print(f"Emails sent: {len(mail.outbox)}")
if len(mail.outbox) > 0:
    print(f"Subject: {mail.outbox[0].subject}")
    print(f"Body: {mail.outbox[0].body}")
