from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('student', 'Student'),
        ('examiner', 'Examiner'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

    def __str__(self):
        return f"{self.username} ({self.role})"

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    nama = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    kampus = models.CharField(max_length=100, default='UMJ')
    asal_sekolah = models.CharField(max_length=100)
    fakultas = models.CharField(max_length=100)
    jurusan = models.CharField(max_length=100)
    jumlah_hafalan = models.IntegerField(help_text="Jumlah juz hafalan")
    nim = models.CharField(max_length=20, unique=True)
    ipk = models.DecimalField(max_digits=3, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(4)])
    semester = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(8)])
    tanggal_lahir = models.DateField(null=True, blank=True, help_text="Format: YYYY-MM-DD")
    is_verified = models.BooleanField(default=False)
    STATUS_CHOICES = [
        ('Proses', 'Proses'),
        ('Lulus', 'Lulus'),
        ('Tidak Lulus', 'Tidak Lulus'),
    ]
    status_seleksi = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Proses')

    def __str__(self):
        return self.nama

class Examiner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='examiner_profile')
    nama = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    nomor_telepon = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.nama

class Group(models.Model):
    nama_group = models.CharField(max_length=100)
    members = models.ManyToManyField(Student, related_name='groups')
    examiner = models.ForeignKey(Examiner, on_delete=models.CASCADE, related_name='groups')
    whatsapp_link = models.URLField(blank=True)
    gmeet_link = models.URLField(blank=True)

    def __str__(self):
        return self.nama_group

class Evaluation(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='evaluations')
    examiner = models.ForeignKey(Examiner, on_delete=models.CASCADE, related_name='evaluations')
    makhorijul_huruf = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    tajwid = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    lancar = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    # hafalan score removed, using Student.jumlah_hafalan quantity instead
    wsm_score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # WSM Weights
    WEIGHTS = {
        'makhorijul_huruf': 0.20,
        'tajwid': 0.20,
        'lancar': 0.20,
        'jumlah_hafalan': 0.20,
        'ipk': 0.20
    }

    def save(self, *args, **kwargs):
        # Calculate WSM score
        # Normalize Data
        # IPK: 0-4 scale -> normalize to 0-100 equivalent or just use relative scale. 
        # Here we normalize everything to 0-100 scale for consistency before applying weights.
        norm_ipk = (float(self.student.ipk) / 4.0) * 100
        
        # Hafalan: Assuming max 30 Juz. 
        norm_hafalan = (self.student.jumlah_hafalan / 30.0) * 100
        if norm_hafalan > 100: norm_hafalan = 100 # cap at 100 if somehow more?

        self.wsm_score = (
            (self.makhorijul_huruf * self.WEIGHTS['makhorijul_huruf']) +
            (self.tajwid * self.WEIGHTS['tajwid']) +
            (self.lancar * self.WEIGHTS['lancar']) +
            (norm_hafalan * self.WEIGHTS['jumlah_hafalan']) +
            (norm_ipk * self.WEIGHTS['ipk'])
        )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Evaluation for {self.student.nama} by {self.examiner.nama}"
