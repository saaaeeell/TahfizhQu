# Alur Sistem TahfizhQu (System Workflow)

Dokumen ini menjelaskan alur lengkap penggunaan aplikasi TahfizhQu menggunakan **Satu Pintu Admin Dashboard** dan **Verifikasi Email Mandiri**.

## 1. Role (Peran Pengguna)
Sistem ini memiliki 3 role utama:
- **Admin**: Pengelola utama sistem (via Dashboard Admin).
- **Student (Mahasiswa)**: Pendaftar beasiswa.
- **Examiner (Penguji)**: Dosen/Ustadz yang menguji halafan.

---

## 2. Alur Registrasi & Aktivasi Akun
Demi keamanan dan kemudahan, sistem menggunakan verifikasi email otomatis.

1. **Mahasiswa Mendaftar** (`/register`):
   - Mengisi Username, Email, dan Password.
   - **Status Akun**: `Inactive` (Tidak bisa login).
   - Sistem mengirimkan **Email Verifikasi** (Lihat di Console/Terminal).

2. **Verifikasi Mandiri**:
   - Mahasiswa mengklik link aktivasi dari email.
   - **Status Akun**: `Active` (Otomatis Aktif).
   - Mahasiswa login ke sistem.

---

## 3. Alur Pengajuan Beasiswa

1. **Pengisian Data (`/apply`)**:
   - Setelah login, mahasiswa diarahkan mengisi formulir data diri & hafalan.
   - Data tersimpan dan masuk antrian verifikasi.

2. **Verifikasi Admin (Dashboard Admin)**:
   - Admin login dan masuk ke **Dashboard Admin**.
   - Mengklik menu / tombol **Verifikasi Data**.
   - Admin melihat daftar pendaftar baru.
   - Admin menekan tombol **Verify** pada mahasiswa yang datanya valid.
   - **Status Student**: `Verified` (Siap untuk ujian).

---

## 4. Manajemen Penguji & Kelompok (Dashboard Admin)

1.  **Tambah Penguji (Create Examiner)**:
    -   Admin membuat akun untuk Dosen/Ustadz Penguji.
    -   Menu: **Tambah Penguji**.
    -   Mengisi: Username, Nama, Email, No. HP.

2.  **Grouping / Pembagian Kelompok**:
    -   Di Dashboard, Admin memilih menu **Buat Kelompok**.
    -   Menentukan Nama Kelompok dan memilih **Examiner** (Penguji) yang sudah dibuat.
    -   Memasukkan mahasiswa yang sudah diverifikasi ke dalam kelompok tersebut.

---

## 5. Alur Ujian (Exam Flow)

1.  **Proses Ujian (Examiner)**:
    -   Penguji login dan masuk ke **Dashboard Examiner**.
    -   Mengklik nama mahasiswa dalam kelompoknya.
    -   Mengisi nilai (Makhorijul Huruf, Tajwid, Kelancaran).
    -   Menyimpan nilai.

---

## 6. Alur Penentuan & Pengumuman

1. **Monitoring Nilai (Dashboard Admin)**:
   - Admin dapat melihat statistik nilai masuk di Dashboard (Card "Evaluasi Masuk").
   - Sistem otomatis menghitung skor akhir (**WSM Score**).

2. **Pengumuman (Dashboard Admin)**:
   - Jika seleksi selesai, Admin menekan tombol **Umumkan Hasil** di Dashboard.
   - Status nilai berubah menjadi *Published*.

3. **Hasil Seleksi (Student)**:
   - Mahasiswa login dan melihat status kelulusan di Dashboard mereka masing-masing.
