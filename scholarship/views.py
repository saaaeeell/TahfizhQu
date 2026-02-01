from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.html import strip_tags
from django.conf import settings
from pathlib import Path
from .models import User, Student, Examiner, Group, Evaluation
from django.db.models import Count
from .forms import EvaluationForm, AdminStudentCreationForm, StudentRegistrationForm, ScholarshipApplicationForm, ExaminerCreationForm
from . import notifications



def home(request):
    if request.user.is_authenticated:
        if request.user.role == 'student':
            return redirect('student_dashboard')
        elif request.user.role == 'examiner':
            return redirect('examiner_dashboard')
        elif request.user.role == 'admin':
            return redirect('admin_dashboard')
    return render(request, 'scholarship/home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        next_url = request.POST.get('next')

        log_file = settings.BASE_DIR / 'login_debug.txt'

        # Debug logging
        with open(log_file, 'a') as f:
            f.write(f"Login attempt: username={username}, next_url={next_url}\n")

        # Try to get the user first (without authenticating)
        User = get_user_model()
        try:
            user_obj = User.objects.get(username=username)

            # Check if email is verified
            if not user_obj.is_active:
                with open(log_file, 'a') as f:
                    f.write(f"User {username} is inactive\n")
                messages.error(request, 'Akun Anda belum diverifikasi. Silakan cek email Anda dan klik link verifikasi terlebih dahulu.')
                return render(request, 'scholarship/login.html')
        except User.DoesNotExist:
            with open(log_file, 'a') as f:
                f.write(f"User {username} does not exist\n")
            pass  # Will be caught by authenticate below

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            with open(log_file, 'a') as f:
                f.write(f"Auth success for {username}. Role={user.role}, Staff={user.is_staff}, Hero={user.is_superuser}\n")
            login(request, user)
            
            # If there's a 'next' parameter, use it (highest priority)
            if next_url and next_url.strip():
                with open(log_file, 'a') as f:
                    f.write(f"Redirecting to next: {next_url}\n")
                return redirect(next_url)

            # Redirection logic:
            # 1. Superusers go to Django Admin by default unless they have an app role and came in through the app.
            # 2. Users with specific app roles go to their dashboards.
            
            if user.is_superuser and not user.role == 'admin':
                return redirect('/django-admin/')
                
            if user.role == 'student':
                return redirect('student_dashboard')
            elif user.role == 'examiner':
                return redirect('examiner_dashboard')
            elif user.role == 'admin':
                return redirect('admin_dashboard')
            
            # Fallback
            if user.is_staff or user.is_superuser:
                return redirect('/django-admin/')
            else:
                return redirect('home')
        else:
            with open(log_file, 'a') as f:
                f.write(f"Auth failed for {username}\n")
            messages.error(request, 'Username atau password salah.')
            return render(request, 'scholarship/login.html')

    return render(request, 'scholarship/login.html')

def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'student'
            user.is_active = False
            user.save()

            # Email Verification Logic
            current_site = get_current_site(request)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            domain = current_site.domain
            protocol = 'https' if request.is_secure() else 'http'
            activation_link = f"{protocol}://{domain}/activate/{uid}/{token}/"

            # Render HTML email template
            html_content = render_to_string('scholarship/emails/verification_email.html', {
                'username': user.username,
                'activation_link': activation_link,
                'domain': domain,
            })

            # Create plain text version
            text_content = strip_tags(html_content)

            # Send email with both HTML and plain text versions
            subject = 'Aktivasi Akun TahfizhQu - Verifikasi Email Anda'
            from_email = 'TahfizhQu <daisyorscry@gmail.com>'
            to_email = [user.email]

            try:
                # Create email with HTML
                email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
                email.attach_alternative(html_content, "text/html")
                email.send(fail_silently=False)

                email_sent = True
                email_error = None
            except Exception as e:
                email_sent = False
                email_error = str(e)

            # Show success state in same page
            return render(request, 'scholarship/register_student.html', {
                'form': form,
                'registration_success': True,
                'email': user.email,
                'username': user.username,
                'email_sent': email_sent,
                'email_error': email_error,
            })
    else:
        form = StudentRegistrationForm()
    return render(request, 'scholarship/register_student.html', {'form': form})

@login_required
def apply_scholarship(request):
    if request.user.role != 'student':
        return redirect('home')
    
    # Cek apakah ada pendaftaran yang masih 'Proses'
    active_app = Student.objects.filter(user=request.user, status_seleksi='Proses').first()

    if request.method == 'POST':
        # Jika ada active_app, edit yang itu. Jika tidak, buat baru (instance=None)
        form = ScholarshipApplicationForm(request.POST, instance=active_app)
        if form.is_valid():
            student_obj = form.save(commit=False)
            student_obj.user = request.user
            student_obj.email = request.user.email
            
            # Reset verifikasi jika ini pendaftaran baru
            if not active_app:
                student_obj.is_verified = False
                student_obj.status_seleksi = 'Proses'
            else:
                # Jika sedang mengedit pendaftaran yang sudah terverifikasi dan ada perubahan,
                # kembalikan status ke 'Proses' dan set is_verified False agar admin harus verifikasi ulang
                if getattr(active_app, 'is_verified', False) and form.has_changed():
                    student_obj.is_verified = False
                    student_obj.status_seleksi = 'Proses'
                    messages.warning(request, 'Perubahan disimpan. Data Anda akan diverifikasi ulang oleh admin.')
                else:
                    # Pertahankan nilai sebelumnya jika tidak ada perubahan signifikan
                    student_obj.is_verified = active_app.is_verified
                    student_obj.status_seleksi = active_app.status_seleksi
                
            student_obj.save()

            # Email logic
            try:
                html_content = render_to_string('scholarship/emails/scholarship_confirmation.html', {'student': student_obj})
                subject = 'Konfirmasi Pendaftaran Beasiswa'
                email = EmailMultiAlternatives(subject, strip_tags(html_content), 'daisyorscry@gmail.com', [request.user.email])
                email.attach_alternative(html_content, "text/html")
                email.send()
                messages.success(request, 'Berhasil dikirim!')
            except:
                messages.warning(request, 'Berhasil, tapi email gagal kirim.')

            return redirect('student_dashboard')
    else:
        form = ScholarshipApplicationForm(instance=active_app)
    
    return render(request, 'scholarship/apply_scholarship.html', {'form': form})

@login_required
def verification_list(request):
    if request.user.role != 'admin' and not request.user.is_superuser:
        return redirect('home')
    
    # Students who have applied (have Student profile) but not verified
    students_unverified = Student.objects.filter(is_verified=False)
    students_verified = Student.objects.filter(is_verified=True)
    
    return render(request, 'scholarship/verification_list.html', {
        'students_unverified': students_unverified,
        'students_verified': students_verified
    })

@login_required
def verify_student(request, student_id):
    if request.user.role != 'admin' and not request.user.is_superuser:
        return redirect('home')
    
    student = get_object_or_404(Student, id=student_id)
    student.is_verified = True
    student.save()
    
    # Also activate the user account to allow login
    student.user.is_active = True
    student.user.save()
    messages.success(request, f'Student {student.nama} has been verified.')
    
    # Send Notification Email
    notifications.send_verification_approved_email(student)
    
    return redirect('verification_list')


@login_required
def student_dashboard(request):
    if request.user.role != 'student':
        return redirect('home')
    
    student = request.user.applications.first() 
    
    if not student:
        return redirect('apply_scholarship')

    groups = student.groups.all()
    evaluations = student.evaluations.all()

    return render(request, 'scholarship/student_dashboard.html', {
        'student': student,
        'groups': groups,
        'evaluations': evaluations
    })

@login_required
def examiner_dashboard(request):
    if not hasattr(request.user, 'role') or request.user.role != 'examiner':
        return redirect('home')
    
    try:
        # Gunakan filter().first() atau get()
        # Jika di model tidak ada related_name='examiner_profile', 
        # coba ganti jadi request.user.examiner
        examiner = Examiner.objects.get(user=request.user)
    except Examiner.DoesNotExist:
        return render(request, 'scholarship/error_profile_missing.html')

    groups = Group.objects.filter(examiner=examiner)
    return render(request, 'scholarship/examiner_dashboard.html', {
        'examiner': examiner,
        'groups': groups
    })

@login_required
def admin_dashboard(request):
    if request.user.role != 'admin' and not request.user.is_superuser:
        return redirect('home')
    students = Student.objects.all()
    groups = Group.objects.all()
    evaluations = Evaluation.objects.all()

    # Compute per-group evaluated counts for dashboard indicators
    groups_stats = []
    for group in groups:
        member_ids = group.members.values_list('id', flat=True)
        evaluated_count = Evaluation.objects.filter(examiner=group.examiner, student__in=member_ids).values('student').distinct().count()
        groups_stats.append({
            'group': group,
            'member_count': group.members.count(),
            'evaluated_count': evaluated_count
        })

    return render(request, 'scholarship/admin_dashboard.html', {
        'students': students,
        'groups': groups,
        'evaluations': evaluations,
        'groups_stats': groups_stats
    })

@login_required
def create_examiner(request):
    if request.user.role != 'admin' and not request.user.is_superuser:
        return redirect('home')
    
    if request.method == 'POST':
        form = ExaminerCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Examiner created successfully.')
            return redirect('admin_dashboard')
    else:
        form = ExaminerCreationForm()
    
    return render(request, 'scholarship/create_examiner.html', {'form': form})

@login_required
def create_group(request):
    if request.user.role != 'admin' and not request.user.is_superuser:
        return redirect('home')
    
    # Filter Logic
    students = Student.objects.filter(groups__isnull=True) # Only students not in a group
    filter_type = request.GET.get('filter_type')
    filter_value = request.GET.get('filter_value')
    
    if filter_type == 'semester' and filter_value:
        students = students.filter(semester=filter_value)
    elif filter_type == 'juz' and filter_value:
        students = students.filter(jumlah_hafalan=filter_value)
    elif filter_type == 'nim': # Sort by NIM
        students = students.order_by('nim')

    if request.method == 'POST':
        nama_group = request.POST.get('nama_group')
        examiner_id = request.POST.get('examiner')
        student_ids = request.POST.getlist('students')
        whatsapp_link = request.POST.get('whatsapp_link')
        gmeet_link = request.POST.get('gmeet_link')
        
        if not nama_group or not examiner_id:
             messages.error(request, "Name and Examiner are required.")
             return redirect('create_group')

        # Ensure selected students are verified
        unverified = Student.objects.filter(id__in=student_ids, is_verified=False)
        if unverified.exists():
            names = ", ".join([u.nama for u in unverified])
            messages.error(request, f"Tidak dapat membuat grup: mahasiswa belum terverifikasi ({names}). Silakan verifikasi terlebih dahulu.")
            return redirect('create_group')

        examiner = get_object_or_404(Examiner, id=examiner_id)
        group = Group.objects.create(
            nama_group=nama_group,
            examiner=examiner,
            whatsapp_link=whatsapp_link,
            gmeet_link=gmeet_link
        )
        group.members.set(Student.objects.filter(id__in=student_ids))
        
        # Send Notification Emails to all members
        for student in group.members.all():
            notifications.send_group_assignment_email(group, student)
            
        messages.success(request, 'Group created.')
        return redirect('admin_dashboard')
        
    examiners = Examiner.objects.all()
    # Unique values for filters
    semesters = Student.objects.values_list('semester', flat=True).distinct().order_by('semester')
    juzs = Student.objects.values_list('jumlah_hafalan', flat=True).distinct().order_by('jumlah_hafalan')
    
    has_unverified = Student.objects.filter(is_verified=False).exists()
    return render(request, 'scholarship/create_group.html', {
        'examiners': examiners,
        'students': students,
        'semesters': semesters,
        'juzs': juzs,
        'has_unverified': has_unverified
    })


@login_required
def admin_students(request):
    if request.user.role != 'admin' and not request.user.is_superuser:
        return redirect('home')

    filter_type = request.GET.get('filter', 'all')
    if filter_type == 'verified':
        students = Student.objects.filter(is_verified=True)
    elif filter_type == 'unverified':
        students = Student.objects.filter(is_verified=False)
    else:
        students = Student.objects.all()

    return render(request, 'scholarship/admin_students.html', {
        'students': students,
        'filter': filter_type
    })


@login_required
def admin_groups(request):
    if request.user.role != 'admin' and not request.user.is_superuser:
        return redirect('home')

    groups = Group.objects.all().order_by('nama_group')
    return render(request, 'scholarship/admin_groups.html', {'groups': groups})


@login_required
def admin_group_detail(request, group_id):
    if request.user.role != 'admin' and not request.user.is_superuser:
        return redirect('home')

    group = get_object_or_404(Group, id=group_id)
    members = group.members.all()
    member_status = []
    for student in members:
        # Check if this student has been evaluated by this group's examiner
        evaluated = Evaluation.objects.filter(student=student, examiner=group.examiner).exists()
        eval_obj = Evaluation.objects.filter(student=student, examiner=group.examiner).order_by('-created_at').first()
        member_status.append({'student': student, 'evaluated': evaluated, 'evaluation': eval_obj})

    return render(request, 'scholarship/admin_group_detail.html', {
        'group': group,
        'member_status': member_status
    })


@login_required
def admin_evaluations(request):
    if request.user.role != 'admin' and not request.user.is_superuser:
        return redirect('home')

    evaluations = Evaluation.objects.select_related('student', 'examiner').order_by('-created_at')
    return render(request, 'scholarship/admin_evaluations.html', {'evaluations': evaluations})


@login_required
def admin_not_evaluated(request):
    if request.user.role != 'admin' and not request.user.is_superuser:
        return redirect('home')

    # Students with no evaluations at all
    students = Student.objects.filter(evaluations__isnull=True)
    return render(request, 'scholarship/admin_not_evaluated.html', {'students': students})


@login_required
def admin_recent_evaluations(request):
    if request.user.role != 'admin' and not request.user.is_superuser:
        return redirect('home')

    groups = Group.objects.all()
    recent = []
    for group in groups:
        latest = Evaluation.objects.filter(student__in=group.members.all()).order_by('-created_at')[:5]
        recent.append({'group': group, 'evaluations': latest})

    return render(request, 'scholarship/admin_recent_evaluations.html', {'recent': recent})


@login_required
def admin_examiners(request):
    if request.user.role != 'admin' and not request.user.is_superuser:
        return redirect('home')

    # Annotate examiners with number of evaluations they've done
    examiners = Examiner.objects.annotate(evaluation_count=Count('evaluations')).order_by('-evaluation_count', 'nama')
    return render(request, 'scholarship/admin_examiners.html', {'examiners': examiners})


@login_required
def admin_examiner_detail(request, examiner_id):
    if request.user.role != 'admin' and not request.user.is_superuser:
        return redirect('home')

    examiner = get_object_or_404(Examiner, id=examiner_id)
    # Evaluations by this examiner, latest first
    evaluations = Evaluation.objects.filter(examiner=examiner).select_related('student').order_by('-created_at')

    # For convenience, group evaluations per student (latest evaluation only)
    latest_per_student = {}
    for ev in evaluations:
        if ev.student.id not in latest_per_student:
            latest_per_student[ev.student.id] = ev

    return render(request, 'scholarship/admin_examiner_detail.html', {
        'examiner': examiner,
        'evaluations': list(latest_per_student.values()),
        'total_evaluations': evaluations.count()
    })

@login_required
def evaluate_student(request, student_id):
    if request.user.role != 'examiner':
        return redirect('home')
    examiner = get_object_or_404(Examiner, user=request.user)
    student = get_object_or_404(Student, id=student_id)
    
    # Ensure student is verified
    if not student.is_verified:
        messages.error(request, 'Student is not verified yet.')
        return redirect('examiner_dashboard')

    # Check if already evaluated by this examiner
    existing_eval = Evaluation.objects.filter(student=student, examiner=examiner).first()
    if existing_eval:
        messages.info(request, 'You have already evaluated this student.')
        # Could allow edit, passing instance
        form = EvaluationForm(request.POST or None, instance=existing_eval)
    else:
        form = EvaluationForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            evaluation = form.save(commit=False)
            evaluation.student = student
            evaluation.examiner = examiner
            evaluation.save()
            
            # Send Notification Email
            notifications.send_evaluation_complete_email(evaluation)
            
            messages.success(request, 'Evaluation submitted.')
            return redirect('examiner_dashboard')
    
    return render(request, 'scholarship/evaluate_student.html', {
        'form': form,
        'student': student
    })

@login_required
def announce_results(request):
    if request.user.role != 'admin' and not request.user.is_superuser:
        return redirect('home')
    # Publish results
    Evaluation.objects.all().update(is_published=True)
    
    # Send Notification Emails for each student
    evaluations = Evaluation.objects.filter(is_published=True)
    for evaluation in evaluations:
        notifications.send_final_result_email(evaluation)
        
    messages.success(request, 'Results announced successfully.')
    return redirect('admin_dashboard')

import csv
from django.http import HttpResponse

@login_required
def download_student_template(request):
    if request.user.role != 'admin' and not request.user.is_superuser:
        return redirect('home')
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="template_mahasiswa.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['username', 'nama', 'email', 'nim', 'kampus', 'asal_sekolah', 'fakultas', 'jurusan', 'jumlah_hafalan', 'ipk', 'semester', 'tanggal_lahir', 'status_seleksi'])
    # Optional: add a sample row
    writer.writerow(['mahasiswa1', 'Nama Mahasiswa', 'mhs1@example.com', '12345678', 'UMJ', 'SMAN 1', 'FT', 'Informatika', '5', '3.50', '3', '2004-01-01', 'Proses'])
    
    return response

@login_required
def download_examiner_template(request):
    if request.user.role != 'admin' and not request.user.is_superuser:
        return redirect('home')
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="template_penguji.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['username', 'nama', 'email', 'nomor_telepon'])
    # Optional: add a sample row
    writer.writerow(['penguji1', 'Nama Penguji', 'penguji1@example.com', '08123456789'])
    
    return response

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Email berhasil diverifikasi! Silakan login untuk melanjutkan.')
        return redirect('login')
    else:
        messages.error(request, 'Link aktivasi tidak valid atau sudah kadaluarsa!')
        return redirect('home')
