# 🕌 TahfizhQu - Sistem Seleksi Beasiswa Tahfizh

TahfizhQu adalah platform berbasis web yang dirancang untuk mengelola proses seleksi beasiswa Tahfizh secara transparan, terorganisir, dan otomatis. Sistem ini mengintegrasikan pendaftaran mahasiswa, penilaian oleh penguji, hingga perhitungan skor akhir menggunakan metode **Weighted Sum Model (WSM)**.

---

## ✨ Fitur Utama

- **Pendaftaran & Aktivasi**: Registrasi mandiri mahasiswa dengan verifikasi aktivasi melalui email.
- **Multi-Role Dashboard**: Dashboard khusus untuk Mahasiswa, Penguji, Admin, dan Super Admin.
- **Weighted Sum Model (WSM)**: Perhitungan nilai otomatis berdasarkan bobot variabel (Hafalan, Tajwid, Makhorijul Huruf, IPK, dll).
- **Manajemen Kelompok**: Pengelompokan mahasiswa dengan penguji serta integrasi link koordinasi (WhatsApp & GMeet).
- **Import/Export Data**: Kemudahan manajemen data skala besar menggunakan CSV/Excel (didukung oleh `django-import-export`).
- **Modern Admin Interface**: Antarmuka admin yang responsif dan elegan menggunakan tema `django-unfold`.
- **Notifikasi Email**: Pengiriman otomatis email konfirmasi pendaftaran, penugasan kelompok, dan hasil seleksi.

---

## 🛠️ Tech Stack

- **Framework**: [Django 6.0](https://www.djangoproject.com/)
- **UI/Admin**: [Django Unfold](https://github.com/unfoldadmin/django-unfold) (Tailwind-based)
- **Database**: SQLite (Default)
- **Email**: SMTP Gmail Integration
- **Libraries**:
  - `django-import-export` untuk manajemen data.
  - `tablib` untuk pemrosesan file spreadsheet.

---

## 🚀 Instalasi & Setup

### 1. Clone Repository
```bash
git clone https://github.com/username/TahfizhQu.git
cd TahfizhQu
```

### 2. Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# atau
venv\Scripts\activate     # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Migration
```bash
python manage.py migrate
```

### 5. Create Superuser (IT System)
```bash
python manage.py createsuperuser
```

### 6. Run Server
```bash
python manage.py runserver
```
Akses aplikasi di `http://127.0.0.1:8000/`

---

## 👥 Peran Pengguna

| Peran | Deskripsi | Akses Dashboard |
|---|---|---|
| **Student** | Pendaftar beasiswa | `/student/dashboard/` |
| **Examiner** | Penguji setoran hafalan | `/examiner/dashboard/` |
| **Admin** | Panitia operasional | `/admin/dashboard/` |
| **Super Admin** | Pengelola sistem & data | `/django-admin/` |

---

## 📖 Dokumentasi Alur
Informasi detail mengenai alur sistem dari registrasi hingga pengumuman dapat dilihat pada berkas [ALUR_SISTEM.md](ALUR_SISTEM.md).

---

## 📄 Lisensi
Proyek ini dikembangkan untuk kebutuhan internal seleksi beasiswa Tahfizh.
