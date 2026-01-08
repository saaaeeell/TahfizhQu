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
        
    def save(self, commit=True):
        examiner = super().save(commit=False)
        
        # Create User for Examiner
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        password = 'password123' # Default password, or maybe generate one
        
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

class ScholarshipApplicationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['nama', 'tanggal_lahir', 'kampus', 'asal_sekolah', 'fakultas', 'jurusan', 'jumlah_hafalan', 'nim', 'ipk', 'semester']
        widgets = {
            'tanggal_lahir': forms.DateInput(attrs={'type': 'date'}),
        }

class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ['makhorijul_huruf', 'tajwid', 'lancar']