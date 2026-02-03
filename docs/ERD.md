# ERD (Entity Relationship Diagram) — TahfizhQu 🔧

Dokumentasi ERD untuk model-model utama pada aplikasi TahfizhQu.

## Diagram ER (Mermaid)

```mermaid
erDiagram
    USER {
        integer id PK
        string username
        string email
        string role
        boolean is_active
    }

    STUDENT {
        integer id PK
        integer user_id FK
        string nama
        string nim
        string email
        string kampus
        string fakultas
        string jurusan
        integer semester
        float ipk
        string asal_sekolah
        date tanggal_lahir
        integer jumlah_hafalan
        boolean is_verified
        string status_seleksi
        datetime created_at
    }

    EXAMINER {
        integer id PK
        integer user_id FK
        string nama
        string email
        string nomor_telepon
    }

    "GROUP" {
        integer id PK
        string nama_group
        integer examiner_id FK
        string whatsapp_link
        string gmeet_link
    }

    EVALUATION {
        integer id PK
        integer student_id FK
        integer examiner_id FK
        integer makhorijul_huruf
        integer tajwid
        integer lancar
        decimal wsm_score
        boolean is_published
        datetime created_at
    }

    %% Relationships
    USER ||--o{ STUDENT : "has applications"
    USER ||--|| EXAMINER : "is examiner profile"
    EXAMINER ||--o{ GROUP : "owns"
    GROUP }o--o{ STUDENT : "members"
    STUDENT ||--o{ EVALUATION : "has"
    EXAMINER ||--o{ EVALUATION : "performs"
```

---

## Keterangan singkat (hubungan utama)
- User (extends Django `AbstractUser`) dapat memiliki banyak `Student` (aplikasi pendaftaran). ✅
- User berhubungan satu-ke-satu dengan `Examiner` untuk role penguji. ✅
- `Group` berelasi many-to-many dengan `Student` (anggota group). ✅
- `Examiner` memiliki relasi one-to-many ke `Group` (seorang examiner mengelola banyak group). ✅
- `Evaluation` menyimpan hasil penilaian yang mengacu ke `Student` dan `Examiner`. ✅

---

Referensi implementasi: `scholarship/models.py`.

Mau saya juga buatkan gambar SVG/PNG yang lebih lengkap (kotak + garis) dan menambahkan link/preview di `README.md`? (jawab: ya/tidak) ✨