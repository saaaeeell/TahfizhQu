from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings

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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    nama = models.CharField(max_length=100)
    nim = models.CharField(max_length=20)
    email = models.EmailField()
    kampus = models.CharField(max_length=100)
    fakultas = models.CharField(max_length=100)
    jurusan = models.CharField(max_length=100)
    semester = models.IntegerField()
    ipk = models.FloatField()
    asal_sekolah = models.CharField(max_length=100)
    tanggal_lahir = models.DateField()
    jumlah_hafalan = models.IntegerField()
    is_verified = models.BooleanField(default=False)
    status_seleksi = models.CharField(
        max_length=20, 
        choices=[('Proses', 'Proses'), ('Lulus', 'Lulus'), ('Tidak Lulus', 'Tidak Lulus')],
        default='Proses'
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.nama} - {self.created_at.strftime('%Y')}"

class Examiner(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='examiner_profile')
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
    wsm_score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    WEIGHTS = {
        'makhorijul_huruf': 0.20,
        'tajwid': 0.20,
        'lancar': 0.20,
        'jumlah_hafalan': 0.20,
        'ipk': 0.20
    }

    def compute_wsm(self):
        """Compute WSM score following steps:
        - Determine max values per criterion (from dataset where appropriate)
        - Normalize each criterion value to [0,1]
        - Compute weighted sum (0..1)
        - Convert to percentage (0..100) and return rounded Decimal
        """
        from django.db.models import Max
        # Determine maxima using dataset, with sensible fallbacks
        # For evaluation fields, the scale is 0-100, so we can use 100 as theoretical max
        max_makh = 100.0
        max_tajwid = 100.0
        max_lancar = 100.0

        # For student attributes, use observed max with fallback
        stu_agg = Student.objects.aggregate(
            max_ipk=Max('ipk'),
            max_hafalan=Max('jumlah_hafalan')
        )
        max_ipk = float(stu_agg.get('max_ipk') or 4.0)
        max_hafalan = float(stu_agg.get('max_hafalan') or 30.0)

        # Prevent division by zero
        if max_ipk <= 0: max_ipk = 4.0
        if max_hafalan <= 0: max_hafalan = 30.0

        # Normalize to 0..1
        norm_makh = (float(self.makhorijul_huruf) / max_makh) if max_makh else 0.0
        norm_tajwid = (float(self.tajwid) / max_tajwid) if max_tajwid else 0.0
        norm_lancar = (float(self.lancar) / max_lancar) if max_lancar else 0.0
        norm_ipk = (float(self.student.ipk) / max_ipk)
        norm_hafalan = (float(self.student.jumlah_hafalan) / max_hafalan)

        # Cap normalized values to 1.0
        norm_makh = min(max(norm_makh, 0.0), 1.0)
        norm_tajwid = min(max(norm_tajwid, 0.0), 1.0)
        norm_lancar = min(max(norm_lancar, 0.0), 1.0)
        norm_ipk = min(max(norm_ipk, 0.0), 1.0)
        norm_hafalan = min(max(norm_hafalan, 0.0), 1.0)

        # Weighted sum (0..1)
        weighted = (
            norm_makh * self.WEIGHTS['makhorijul_huruf'] +
            norm_tajwid * self.WEIGHTS['tajwid'] +
            norm_lancar * self.WEIGHTS['lancar'] +
            norm_hafalan * self.WEIGHTS['jumlah_hafalan'] +
            norm_ipk * self.WEIGHTS['ipk']
        )

        # Convert to percentage 0..100 and round to 2 decimals
        score_percent = round(weighted * 100, 2)
        return score_percent

    def get_wsm_breakdown(self):
        """Return detailed breakdown for WSM components and contribution."""
        from django.db.models import Max
        # maxima
        max_makh = 100.0
        max_tajwid = 100.0
        max_lancar = 100.0
        stu_agg = Student.objects.aggregate(max_ipk=Max('ipk'), max_hafalan=Max('jumlah_hafalan'))
        max_ipk = float(stu_agg.get('max_ipk') or 4.0)
        max_hafalan = float(stu_agg.get('max_hafalan') or 30.0)

        comps = []
        # makhorijul_huruf
        norm_makh = min(max(float(self.makhorijul_huruf) / max_makh, 0.0), 1.0)
        contrib_makh = norm_makh * self.WEIGHTS['makhorijul_huruf']
        comps.append({'name': 'makhorijul_huruf', 'raw': float(self.makhorijul_huruf), 'max': max_makh, 'normalized': round(norm_makh, 4), 'weight': self.WEIGHTS['makhorijul_huruf'], 'contribution': round(contrib_makh, 6)})

        # tajwid
        norm_taj = min(max(float(self.tajwid) / max_tajwid, 0.0), 1.0)
        contrib_taj = norm_taj * self.WEIGHTS['tajwid']
        comps.append({'name': 'tajwid', 'raw': float(self.tajwid), 'max': max_tajwid, 'normalized': round(norm_taj, 4), 'weight': self.WEIGHTS['tajwid'], 'contribution': round(contrib_taj, 6)})

        # lancar
        norm_lan = min(max(float(self.lancar) / max_lancar, 0.0), 1.0)
        contrib_lan = norm_lan * self.WEIGHTS['lancar']
        comps.append({'name': 'lancar', 'raw': float(self.lancar), 'max': max_lancar, 'normalized': round(norm_lan, 4), 'weight': self.WEIGHTS['lancar'], 'contribution': round(contrib_lan, 6)})

        # jumlah_hafalan
        norm_haf = min(max(float(self.student.jumlah_hafalan) / max_hafalan, 0.0), 1.0)
        contrib_haf = norm_haf * self.WEIGHTS['jumlah_hafalan']
        comps.append({'name': 'jumlah_hafalan', 'raw': float(self.student.jumlah_hafalan), 'max': max_hafalan, 'normalized': round(norm_haf, 4), 'weight': self.WEIGHTS['jumlah_hafalan'], 'contribution': round(contrib_haf, 6)})

        # ipk
        norm_ipk = min(max(float(self.student.ipk) / max_ipk, 0.0), 1.0)
        contrib_ipk = norm_ipk * self.WEIGHTS['ipk']
        comps.append({'name': 'ipk', 'raw': float(self.student.ipk), 'max': max_ipk, 'normalized': round(norm_ipk, 4), 'weight': self.WEIGHTS['ipk'], 'contribution': round(contrib_ipk, 6)})

        total_weighted = sum([c['contribution'] for c in comps])
        score_percent = round(total_weighted * 100, 2)
        return {'components': comps, 'weighted_sum': round(total_weighted, 6), 'score_percent': score_percent}

    def save(self, *args, **kwargs):
        # Compute WSM score and assign
        self.wsm_score = self.compute_wsm()

        # Determine pass/fail based on >=70 threshold
        if float(self.wsm_score) >= 70.0:
            self.student.status_seleksi = 'Lulus'
        else:
            self.student.status_seleksi = 'Tidak Lulus'

        self.student.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Evaluation for {self.student.nama} by {self.examiner.nama}"