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
from .models import User, Student, Examiner, Group, Evaluation
from .models import User, Student, Examiner, Group, Evaluation
from .forms import EvaluationForm, AdminStudentCreationForm, StudentRegistrationForm, ScholarshipApplicationForm, ExaminerCreationForm

# ... (existing imports)

# ... (existing imports)

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

        # Try to get the user first (without authenticating)
        User = get_user_model()
        try:
            user_obj = User.objects.get(username=username)

            # Check if email is verified
            if not user_obj.is_active:
                messages.error(request, 'Akun Anda belum diverifikasi. Silakan cek email Anda dan klik link verifikasi terlebih dahulu.')
                return render(request, 'scholarship/login.html')
        except User.DoesNotExist:
            pass  # Will be caught by authenticate below

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            
            # If there's a 'next' parameter, use it
            if next_url:
                return redirect(next_url)

            # Redirect based on role / staff status
            if user.is_staff or user.is_superuser:
                return redirect('/django-admin/')
            elif user.role == 'student':
                return redirect('student_dashboard')
            elif user.role == 'examiner':
                return redirect('examiner_dashboard')
            elif user.role == 'admin':
                return redirect('admin_dashboard')
            else:
                return redirect('home')
        else:
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
    
    # Check if student profile already exists
    try:
        student = request.user.student_profile
        # If exists, maybe redirect to dashboard or allow edit? 
        # For now, let's assume they can edit if they want or just redirect
        if student.status_seleksi != 'Proses' and student.status_seleksi != 'Lulus' and student.status_seleksi != 'Tidak Lulus':
             pass # just checking
        # But if they are just created from register, they have no student_profile
    except Student.DoesNotExist:
        student = None

    if request.method == 'POST':
        form = ScholarshipApplicationForm(request.POST, instance=student)
        if form.is_valid():
            student_obj = form.save(commit=False)
            student_obj.user = request.user
            student_obj.email = request.user.email  # Ensure email is synced from User
            student_obj.save()

            # Send Confirmation Email
            html_content = render_to_string('scholarship/emails/scholarship_confirmation.html', {
                'student_name': student_obj.nama,
                'nim': student_obj.nim,
                'fakultas': student_obj.fakultas,
                'jurusan': student_obj.jurusan,
                'semester': student_obj.semester,
                'ipk': student_obj.ipk,
                'jumlah_hafalan': student_obj.jumlah_hafalan,
                'status': student_obj.status_seleksi,
            })

            text_content = strip_tags(html_content)
            subject = 'Konfirmasi Pendaftaran Beasiswa TahfizhQu'
            from_email = 'TahfizhQu <daisyorscry@gmail.com>'
            to_email = [request.user.email]

            try:
                email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
                email.attach_alternative(html_content, "text/html")
                email.send(fail_silently=False)
                messages.success(request, 'Pendaftaran beasiswa berhasil dikirim. Email konfirmasi telah dikirim ke ' + request.user.email)
            except Exception as e:
                # If email fails, still show success for the application but warn about email
                messages.warning(request, f'Pendaftaran berhasil, tetapi gagal mengirim email konfirmasi: {e}')

            return redirect('student_dashboard')
    else:
        form = ScholarshipApplicationForm(instance=student)
    
    return render(request, 'scholarship/apply_scholarship.html', {'form': form})

@login_required
def verification_list(request):
    if request.user.role != 'admin':
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
    if request.user.role != 'admin':
        return redirect('home')
    
    student = get_object_or_404(Student, id=student_id)
    student.is_verified = True
    student.save()
    
    # Also activate the user account to allow login
    student.user.is_active = True
    student.user.save()
    messages.success(request, f'Student {student.nama} has been verified.')
    return redirect('verification_list')


@login_required
def student_dashboard(request):
    if request.user.role != 'student':
        return redirect('home')

    # Safely get student profile
    try:
        student = request.user.student_profile
    except Student.DoesNotExist:
        # If student profile doesn't exist, redirect to scholarship application
        messages.info(request, 'Silakan lengkapi data beasiswa Anda untuk melanjutkan.')
        return redirect('apply_scholarship')

    groups = student.groups.all()
    evaluations = Evaluation.objects.filter(student=student)
    return render(request, 'scholarship/student_dashboard.html', {
        'student': student,
        'groups': groups,
        'evaluations': evaluations
    })

@login_required
def examiner_dashboard(request):
    if request.user.role != 'examiner':
        return redirect('home')
    
    # Safely get examiner profile
    try:
        examiner = request.user.examiner_profile
    except Examiner.DoesNotExist:
         return render(request, 'scholarship/error_profile_missing.html')

    groups = Group.objects.filter(examiner=examiner)
    return render(request, 'scholarship/examiner_dashboard.html', {
        'examiner': examiner,
        'groups': groups
    })

@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        return redirect('home')
    students = Student.objects.all()
    groups = Group.objects.all()
    evaluations = Evaluation.objects.all()
    return render(request, 'scholarship/admin_dashboard.html', {
        'students': students,
        'groups': groups,
        'evaluations': evaluations
    })

@login_required
@login_required
def create_examiner(request):
    if request.user.role != 'admin':
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
    if request.user.role != 'admin':
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
             # Re-render with existing context is better, but redirecting for simplicity now
             return redirect('create_group')

        examiner = get_object_or_404(Examiner, id=examiner_id)
        group = Group.objects.create(
            nama_group=nama_group,
            examiner=examiner,
            whatsapp_link=whatsapp_link,
            gmeet_link=gmeet_link
        )
        group.members.set(Student.objects.filter(id__in=student_ids))
        messages.success(request, 'Group created.')
        return redirect('admin_dashboard')
        
    examiners = Examiner.objects.all()
    # Unique values for filters
    semesters = Student.objects.values_list('semester', flat=True).distinct().order_by('semester')
    juzs = Student.objects.values_list('jumlah_hafalan', flat=True).distinct().order_by('jumlah_hafalan')
    
    return render(request, 'scholarship/create_group.html', {
        'examiners': examiners,
        'students': students,
        'semesters': semesters,
        'juzs': juzs
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
            messages.success(request, 'Evaluation submitted.')
            return redirect('examiner_dashboard')
    
    return render(request, 'scholarship/evaluate_student.html', {
        'form': form,
        'student': student
    })

@login_required
def announce_results(request):
    if request.user.role != 'admin':
        return redirect('home')
    # Publish results
    Evaluation.objects.all().update(is_published=True)
    messages.success(request, 'Results announced successfully.')
    return redirect('admin_dashboard')

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
