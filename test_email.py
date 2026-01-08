#!/usr/bin/env python
"""
Script untuk test email configuration
Run: python test_email.py
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tahfizhqu.settings')
django.setup()

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def test_verification_email():
    """Test sending verification email"""
    print("🧪 Testing Verification Email...")

    # Mock data
    context = {
        'username': 'TestUser',
        'activation_link': 'http://localhost:8000/activate/test123/token456/',
        'domain': 'localhost:8000',
    }

    # Render template
    html_content = render_to_string('scholarship/emails/verification_email.html', context)
    text_content = strip_tags(html_content)

    # Send email
    subject = 'TEST - Aktivasi Akun TahfizhQu'
    from_email = 'TahfizhQu <daisyorscry@gmail.com>'
    to_email = ['daisyorscry@gmail.com']  # Send to self for testing

    try:
        email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=False)
        print("✅ Verification email sent successfully!")
        print(f"📧 Sent to: {to_email[0]}")
        return True
    except Exception as e:
        print(f"❌ Failed to send email: {str(e)}")
        return False

def test_scholarship_confirmation_email():
    """Test sending scholarship confirmation email"""
    print("\n🧪 Testing Scholarship Confirmation Email...")

    # Mock data
    context = {
        'student_name': 'Muhammad Ali',
        'nim': '2021001',
        'fakultas': 'Teknik',
        'jurusan': 'Informatika',
        'semester': 5,
        'ipk': 3.75,
        'jumlah_hafalan': 10,
        'status': 'Proses',
    }

    # Render template
    html_content = render_to_string('scholarship/emails/scholarship_confirmation.html', context)
    text_content = strip_tags(html_content)

    # Send email
    subject = 'TEST - Konfirmasi Pendaftaran Beasiswa TahfizhQu'
    from_email = 'TahfizhQu <daisyorscry@gmail.com>'
    to_email = ['daisyorscry@gmail.com']  # Send to self for testing

    try:
        email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=False)
        print("✅ Scholarship confirmation email sent successfully!")
        print(f"📧 Sent to: {to_email[0]}")
        return True
    except Exception as e:
        print(f"❌ Failed to send email: {str(e)}")
        return False

def main():
    print("=" * 60)
    print("📬 TahfizhQu Email Configuration Test")
    print("=" * 60)

    # Test both email types
    result1 = test_verification_email()
    result2 = test_scholarship_confirmation_email()

    print("\n" + "=" * 60)
    if result1 and result2:
        print("✅ All email tests passed!")
        print("📥 Check your inbox: daisyorscry@gmail.com")
    else:
        print("❌ Some email tests failed. Check the errors above.")
    print("=" * 60)

if __name__ == '__main__':
    main()
