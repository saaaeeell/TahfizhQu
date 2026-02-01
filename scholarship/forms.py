from django import forms
from django.contrib.auth import get_user_model
from .models import Student, Examiner, Evaluation

User = get_user_model()


# =====================================================
# ADMIN CREATE STUDENT
# =====================================================
class AdminStudentCreationForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        help_text="Akan diisi otomatis dengan NIM"
    )

    class Meta:
        model = Student
        fields = [
            'nama', 'email', 'tanggal_lahir', 'kampus',
            'asal_sekolah', 'fakultas', 'jurusan',
            'jumlah_hafalan', 'nim', 'ipk', 'semester'
        ]
        widgets = {
            'tanggal_lahir': forms.DateInput(attrs={'type': 'date'}),
        }

    def save(self, commit=True):
        student = super().save(commit=False)

        username = self.cleaned_data['nim']
        email = self.cleaned_data['email']

        dob = self.cleaned_data.get('tanggal_lahir')
        password = dob.strftime('%d%m%y') if dob else 'password123'

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.role = 'student'
        user.save()

        student.user = user
        if commit:
            student.save()
        return student


# =====================================================
# EXAMINER FORM
# =====================================================
class ExaminerCreationForm(forms.ModelForm):
    username = forms.CharField(max_length=150)

    class Meta:
        model = Examiner
        fields = ['nama', 'email', 'nomor_telepon']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username sudah digunakan.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email sudah digunakan.")
        return email

    def save(self, commit=True):
        examiner = super().save(commit=False)

        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password='password123'
        )
        user.role = 'examiner'
        user.save()

        examiner.user = user
        if commit:
            examiner.save()
        return examiner


# =====================================================
# STUDENT USER REGISTRATION
# =====================================================
class StudentRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        help_texts = {
            'username': 'Gunakan satu kata tanpa spasi.',
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email sudah digunakan.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password') != cleaned_data.get('confirm_password'):
            raise forms.ValidationError("Password tidak sama.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


# =====================================================
# SCHOLARSHIP APPLICATION FORM (MAHASISWA)
# =====================================================
class ScholarshipApplicationForm(forms.ModelForm):

    FAKULTAS_CHOICES = [
        ('Teknik', 'Teknik'),
    ]

    JURUSAN_CHOICES = [
        ('Arsitektur', 'Arsitektur'),
        ('Teknik Sipil', 'Teknik Sipil'),
        ('Teknik Industri', 'Teknik Industri'),
        ('Teknik Elektro', 'Teknik Elektro'),
        ('Teknik Informatika', 'Teknik Informatika'),
        ('D3 Otomotif Alat Berat', 'D3 Otomotif Alat Berat'),
        ('Teknik Kimia', 'Teknik Kimia'),
        ('Teknik Mesin', 'Teknik Mesin'),
    ]

    class Meta:
        model = Student
        fields = [
            'nama', 'tanggal_lahir', 'kampus', 'asal_sekolah',
            'fakultas', 'jurusan', 'jumlah_hafalan',
            'nim', 'ipk', 'semester'
        ]

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
            'tanggal_lahir': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full p-2 border rounded'
            }),
            'nama': forms.TextInput(attrs={
                'class': 'w-full p-2 border rounded',
                'oninput': 'this.value=this.value.replace(/[^a-zA-Z\\s]/g,"")'
            }),
            'kampus': forms.TextInput(attrs={
                'class': 'w-full p-2 border rounded',
                'oninput': 'this.value=this.value.replace(/[^a-zA-Z\\s]/g,"")'
            }),
            'asal_sekolah': forms.TextInput(attrs={
                'class': 'w-full p-2 border rounded'
            }),
            'fakultas': forms.Select(attrs={
                'class': 'w-full p-2 border rounded'
            }),
            'jurusan': forms.Select(attrs={
                'class': 'w-full p-2 border rounded'
            }),
            'jumlah_hafalan': forms.NumberInput(attrs={
                'min': '0',
                'max': '30',
                'class': 'w-full p-2 border rounded'
            }),
            'nim': forms.TextInput(attrs={
                'class': 'w-full p-2 border rounded',
                'inputmode': 'numeric',
                'pattern': '[0-9]*',
                'oninput': 'this.value=this.value.replace(/[^0-9]/g,"")'
            }),
            'ipk': forms.NumberInput(attrs={
                'step': '0.01',
                'min': '0',
                'max': '4',
                'class': 'w-full p-2 border rounded'
            }),
            'semester': forms.NumberInput(attrs={
                'min': '1',
                'max': '8',
                'class': 'w-full p-2 border rounded'
            }),
        }

        help_texts = {
            'jumlah_hafalan': 'Maksimal hafalan adalah 30 juz.',
            'ipk': 'Gunakan titik (.) sebagai pemisah desimal (contoh: 3.75).',
        }

    # dropdown override
    fakultas = forms.ChoiceField(choices=FAKULTAS_CHOICES)
    jurusan = forms.ChoiceField(choices=JURUSAN_CHOICES)

    # backend validation (anti-bypass)
    def clean_semester(self):
        semester = self.cleaned_data.get('semester')
        if semester and semester > 8:
            raise forms.ValidationError("Semester maksimal adalah 8.")
        return semester

    def clean_jumlah_hafalan(self):
        jumlah = self.cleaned_data.get('jumlah_hafalan')
        if jumlah and jumlah > 30:
            raise forms.ValidationError("Jumlah hafalan maksimal adalah 30 juz.")
        return jumlah

    def clean_nama(self):
        nama = self.cleaned_data.get('nama')
        if not nama.replace(' ', '').isalpha():
            raise forms.ValidationError("Nama hanya boleh mengandung huruf dan spasi.")
        return nama


# =====================================================
# EVALUATION FORM
# =====================================================
class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ['makhorijul_huruf', 'tajwid', 'lancar']
