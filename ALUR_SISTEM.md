# Alur Sistem TahfizhQu (System Workflow)

Dokumen ini menjelaskan alur lengkap penggunaan aplikasi TahfizhQu menggunakan **Multi-Dashboard Support** (Admin Dashboard, Examiner Dashboard, Student Dashboard, dan Super Admin/Django Admin).

---

## 1. Peran Pengguna (Roles)
Sistem memiliki 4 entitas pengguna dengan hak akses yang berbeda:

- **Super Admin (IT System / Root)**: 
  - Memiliki akses penuh ke [Django Admin Interface](/django-admin/).
  - Mengelola seluruh basis data (Users, Students, Examiners, Groups, Evaluations).
  - Melakukan **Import & Export Data** (Student & Examiner) via CSV.
  - Reset password pengguna secara langsung.
  - Mengelola izin teknis (`is_staff`, `is_superuser`).

- **Admin (Panitia Pendaftaran)**: 
  - Mengelola operasional harian melalui [Admin Dashboard](/admin/dashboard/).
  - Melakukan verifikasi pendaftar.
  - Membuat akun Penguji (Examiner) secara manual.
  - Mengelola pengelompokan (Grouping) mahasiswa untuk ujian.
  - Mempublikasikan hasil seleksi akhir.

- **Examiner (Penguji/Ustadz)**: 
  - Mengakses [Examiner Dashboard](/examiner/dashboard/).
  - Melihat daftar kelompok dan mahasiswa yang ditugaskan.
  - Melakukan input nilai ujian (Tahfizh) secara real-time.

- **Student (Mahasiswa)**: 
  - Melakukan registrasi mandiri dan aktivasi via email.
  - Mengisi formulir pendaftaran beasiswa.
  - Memantau status pendaftaran dan melihat hasil akhir seleksi.

---

## 2. Alur Registrasi & Aktivasi (Student)
1. **Pendaftaran**: Mahasiswa mengisi form registrasi di `/register/`.
2. **Status Awal**: Akun berstatus `Inactive` (tidak bisa login).
3. **Verifikasi Email**: Sistem mengirimkan email dengan link aktivasi unik.
4. **Aktivasi**: Mahasiswa mengklik link tersebut, status akun berubah menjadi `Active`.

---

## 3. Alur Pengajuan Beasiswa
1. **Pengisian Form**: Mahasiswa login dan mengisi data (NIM, IPK, Semester, Jumlah Juz, dsb) di `/apply/`.
2. **Konfirmasi**: Mahasiswa menerima email konfirmasi bahwa data telah diterima.
3. **Status Seleksi**: Secara default, mahasiswa masuk ke status **Proses**.

---

## 4. Alur Verifikasi & Manajemen Admin/Super Admin
1. **Verifikasi Data**: Admin/Super Admin memvalidasi berkas di menu **Verifikasi**.
2. **Import Data (Optional)**: Super Admin dapat melakukan import data mahasiswa atau penguji dalam jumlah banyak melalui `/django-admin/`.
3. **Pembuatan Penguji**: Admin membuat akun penguji melalui dashboard atau super admin meng-import-nya.
4. **Pembentukan Kelompok (Grouping)**:
   - Admin/Super Admin membuat kelompok ujian.
   - Menentukan Penguji dan melampirkan link komunikasi (WhatsApp/GMeet).
   - Memilih Mahasiswa yang sudah `Verified` untuk dimasukkan ke kelompok.
   - Sistem mengirimkan email notifikasi penugasan ke Mahasiswa.

---

## 5. Alur Ujian & Penilaian (Examiner)
1. **Evaluasi**: Penguji login, memilih mahasiswa dari kelompoknya, dan mengklik **Input Nilai**.
2. **Variabel Penilaian**:
   - Makhorijul Huruf (0-100)
   - Tajwid (0-100)
   - Kelancaran (0-100)
3. **Perhitungan Otomatis (Weighted Sum Model - WSM)**:
   Sistem menghitung skor akhir (Weighted Score) secara otomatis berdasarkan bobot:
   - **Makhorijul Huruf**: 20%
   - **Tajwid**: 20%
   - **Kelancaran**: 20%
   - **Jumlah Hafalan**: 20% (Normalisasi: `(Juz / 30) * 100`)
   - **IPK**: 20% (Normalisasi: `(IPK / 4.0) * 100`)

---

## 6. Pengumuman Hasil
1. **Publikasi**: Admin/Super Admin menekan tombol **Umumkan Hasil** di dashboard.
2. **Notifikasi**: Sistem mengirimkan email hasil seleksi ke seluruh mahasiswa.
3. **Visualisasi**: Mahasiswa dapat melihat detail skor dan keputusan kelulusan di dashboard masing-masing.

---

## 7. Fitur Tambahan Super Admin
- **Custom Admin UI**: Menggunakan tema *Django Unfold* untuk antarmuka yang modern.
- **Bulk Actions**: Aktivasi/Non-aktivasi pengguna secara massal.
- **Data Integrity**: Menjamin sinkronisasi antara model `User` dan profil terkait (`Student`/`Examiner`).
- **Template Management**: Menyediakan template CSV untuk import data skala besar.
