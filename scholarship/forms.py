from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

from .models import Student, Examiner, Evaluation

class AdminStudentCreationForm(forms.ModelForm):
    # Field yang diperlukan untuk User
    username = forms.CharField(max_length=150, help_text="Akan diisi otomatis dengan Email/NIM jika kosong")
    
    class Meta:
        model = Student
        fields = ['nama', 'email', 'tanggal_lahir', 'kampus', 'asal_sekolah', 'fakultas', 'jurusan', 'jumlah_hafalan', 'nim', 'ipk', 'semester']
        widgets = {
            'tanggal_lahir': forms.DateInput(attrs={'type': 'date'}),
        }

    def save(self, commit=True):
        # Custom save to create User and Student linked
        student = super().save(commit=False)
        
        # Create User
        # Username default to NIM if available, else email
        username = self.cleaned_data['nim']
        email = self.cleaned_data['email']
        
        # Generate Password from DOB (DDMMYY)
        dob = self.cleaned_data['tanggal_lahir']
        if dob:
            password = dob.strftime('%d%m%y')
        else:
            password = 'password123' # Fallback
            
        user = User.objects.create_user(username=username, email=email, password=password)
        user.role = 'student'
        user.save()
        
        
        student.user = user

class ExaminerCreationForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    
    class Meta:
        model = Examiner
        fields = ['nama', 'email', 'nomor_telepon']
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and not email.endswith('@app.ocm'):
            raise forms.ValidationError("Email harus menggunakan domain @app.ocm")
        return email

    def save(self, commit=True):
        examiner = super().save(commit=False)
        
        # Create User for Examiner
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        password = 'password123' # Default password
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.role = 'examiner'
        user.save()
        
        examiner.user = user
        if commit:
            examiner.save()
        return examiner

class StudentRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        help_texts = {
            'username': 'Gunakan satu kata (nama panggilan) atau gabung tanpa spasi.',
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )

    def save(self, commit=True):
        user = super().save(commit=False)
        # Hash the password properly
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class ScholarshipApplicationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['nama', 'tanggal_lahir', 'kampus', 'asal_sekolah', 'fakultas', 'jurusan', 'jumlah_hafalan', 'nim', 'ipk', 'semester']
        labels = {
            'nama': 'Nama Lengkap',
            'tanggal_lahir': 'Tanggal Lahir',
            'kampus': 'Asal Kampus',
            'asal_sekolah': 'Pendidikan Terakhir (Sekolah Asal)',
            'fakultas': 'Fakultas',
            'jurusan': 'Program Studi / Jurusan',
            'jumlah_hafalan': 'Jumlah Juz Hafalan',
            'nim': 'NIM (Nomor Induk Mahasiswa)',
            'ipk': 'IPK Terakhir',
            'semester': 'Semester Saat Ini',
        }
        widgets = {
            'tanggal_lahir': forms.DateInput(attrs={'type': 'date', 'class': 'w-full p-2 border rounded'}),
            'nama': forms.TextInput(attrs={'placeholder': 'Contoh: Ahmad Abdullah', 'class': 'w-full p-2 border rounded'}),
            'email': forms.EmailInput(attrs={'placeholder': 'ahm@example.com', 'class': 'w-full p-2 border rounded'}),
            'kampus': forms.TextInput(attrs={'placeholder': 'Contoh: UMJ / UI / ITB', 'class': 'w-full p-2 border rounded'}),
            'asal_sekolah': forms.TextInput(attrs={'placeholder': 'Contoh: MAN 1 Jakarta', 'class': 'w-full p-2 border rounded'}),
            'fakultas': forms.TextInput(attrs={'placeholder': 'Contoh: Teknik', 'class': 'w-full p-2 border rounded'}),
            'jurusan': forms.TextInput(attrs={'placeholder': 'Contoh: Informatika', 'class': 'w-full p-2 border rounded'}),
            'jumlah_hafalan': forms.NumberInput(attrs={'placeholder': 'Contoh: 30', 'class': 'w-full p-2 border rounded'}),
            'nim': forms.TextInput(attrs={'placeholder': 'Nomor Induk Mahasiswa', 'class': 'w-full p-2 border rounded'}),
            'ipk': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'Skala 4.00', 'class': 'w-full p-2 border rounded'}),
            'semester': forms.NumberInput(attrs={'min': '1', 'max': '8', 'placeholder': '1-8', 'class': 'w-full p-2 border rounded'}),
        }
        help_texts = {
            'jumlah_hafalan': 'Masukkan angka jumlah juz yang sudah dihafal.',
            'ipk': 'Gunakan titik (.) sebagai pemisal desimal.',
        }

class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ['makhorijul_huruf', 'tajwid', 'lancar']