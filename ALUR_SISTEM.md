# Alur Sistem TahfizhQu (System Workflow)

Dokumen ini menjelaskan alur lengkap penggunaan aplikasi TahfizhQu menggunakan **Satu Pintu Admin Dashboard** dan **Verifikasi Email Mandiri**.

## 1. Role (Peran Pengguna)
Sistem memiliki 4 entitas pengguna:
- **Admin (Panitia)**: Pengelola operasional beasiswa (Dashboard `/admin/dashboard/`).
- **Superuser (IT System)**: Pengelola teknis basis data (Dashboard `/django-admin/`).
- **Student (Mahasiswa)**: Pendaftar beasiswa.
- **Examiner (Penguji)**: Dosen/Ustadz yang melakukan penilaian hafalan.

---

## 2. Alur Registrasi & Aktivasi Akun (Student)
Sistem menggunakan verifikasi email otomatis untuk memastikan validitas pendaftar.

1. **Mahasiswa Mendaftar** (`/register`):
   - Mengisi Username, Email, dan Password.
   - **Status Akun**: `Inactive` (Belum bisa login).
   - Sistem mengirimkan email aktivasi (dikirim via terminal di lingkungan dev).
2. **Aktivasi Mandiri**:
   - Mahasiswa mengklik link aktivasi dari email.
   - **Status Akun**: `Active` (Dapat login).

---

## 3. Alur Pengajuan & Verifikasi Beasiswa
Mahasiswa yang sudah aktif harus melengkapi profil beasiswa.

1. **Pengisian Formulir (`/apply`)**:
   - Mahasiswa memasukkan data diri: NIM, IPK, Semester, Jumlah Juz, dll.
   - Data otomatis tersimpan dalam status **Proses**.
2. **Verifikasi Panitia (Admin Dashboard)**:
   - Admin memeriksa data mahasiswa di menu **Verifikasi Data**.
   - Admin melakukan verifikasi berkas/data.
   - **Status Mahasiswa**: `Verified` (Hanya yang terverifikasi yang bisa dikelompokkan dan diuji).

---

## 4. Manajemen Penguji & Kelompok (Admin Dashboard)

1.  **Pembuatan Akun Penguji**:
    -   Admin membuat akun Penguji secara manual di Dashboard.
    -   **Ketentuan**: Email harus menggunakan domain `@app.ocm`.
    -   Sistem otomatis membuatkan User dengan role `examiner`.
2.  **Manajemen Kelompok (Grouping)**:
    -   Admin membuat kelompok ujian melalui menu **Buat Kelompok**.
    -   Admin menentukan **Nama Kelompok**, memilih **Penguji**, dan melampirkan link komunikasi (**WhatsApp** & **GMeet**).
    -   Admin memilih mahasiswa yang sudah `Verified` untuk dimasukkan ke kelompok.

---

## 5. Alur Ujian & Penilaian (Examiner)

1.  **Input Nilai**:
    -   Penguji login dan melihat daftar kelompok serta mahasiswa di Dashboard-nya.
    -   Penguji memberikan skor (0-100) untuk kriteria:
        -   Makhorijul Huruf
        -   Tajwid
        -   Kelancaran
2.  **Perhitungan Otomatis (WSM)**:
    -   Sistem menghitung **WSM Score** secara otomatis saat nilai disimpan.
    -   **Kriteria & Bobot (20% masing-masing)**:
        1. Makhorijul Huruf (Input Penguji)
        2. Tajwid (Input Penguji)
        3. Kelancaran (Input Penguji)
        4. Jumlah Hafalan (Normalisasi: `Juz / 30 * 100`)
        5. IPK (Normalisasi: `IPK / 4.0 * 100`)

---

## 6. Pengumuman Hasil (Admin Dashboard)

1.  **Monitoring**:
    -   Admin memantau jumlah evaluasi yang masuk melalui statistik dashboard.
2.  **Publikasi**:
    -   Admin menekan tombol **Umumkan Hasil**.
    -   Semua skor seleksi akan diterbitkan dan dapat dilihat oleh mahasiswa.
3.  **Visualisasi Mahasiswa**:
    -   Mahasiswa login ke dashboard dan melihat hasil seleksi akhir mereka.
