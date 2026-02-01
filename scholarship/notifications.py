import logging
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

logger = logging.getLogger(__name__)

def _send_email(subject, template_name, context, to_email):
    """Internal helper to render and send email"""
    try:
        html_content = render_to_string(template_name, context)
        text_content = strip_tags(html_content)
        
        from_email = settings.DEFAULT_FROM_EMAIL
        
        email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=False)
        logger.info(f"Email '{subject}' sent to {to_email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email '{subject}' to {to_email}: {str(e)}")
        return False

def send_verification_approved_email(student):
    """Send email when admin verifies student data"""
    subject = 'Data Terverifikasi - Beasiswa TahfizhQu'
    context = {
        'student_name': student.nama,
        'dashboard_url': settings.LOGIN_URL,
    }
    return _send_email(subject, 'scholarship/emails/verification_approved.html', context, student.email)

def send_group_assignment_email(group, student):
    """Send email when student is assigned to a group"""
    subject = f'Grup Ujian Ditentukan: {group.nama_group} - Beasiswa TahfizhQu'
    context = {
        'student_name': student.nama,
        'group_name': group.nama_group,
        'examiner_name': group.examiner.nama,
        'whatsapp_link': group.whatsapp_link,
        'gmeet_link': group.gmeet_link,
    }
    return _send_email(subject, 'scholarship/emails/group_assignment.html', context, student.email)

def send_evaluation_complete_email(evaluation):
    """Send email when examiner completes evaluation"""
    subject = 'Evaluasi Ujian Selesai - Beasiswa TahfizhQu'
    context = {
        'student_name': evaluation.student.nama,
    }
    return _send_email(subject, 'scholarship/emails/evaluation_complete.html', context, evaluation.student.email)

def send_final_result_email(evaluation):
    """Send email when results are announced"""
    subject = 'Pengumuman Hasil Beasiswa TahfizhQu'
    context = {
        'student_name': evaluation.student.nama,
        'wsm_score': evaluation.wsm_score,
        'is_published': evaluation.is_published,
    }
    return _send_email(subject, 'scholarship/emails/final_result.html', context, evaluation.student.email)
