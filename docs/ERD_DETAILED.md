# ERD Rinci — TahfizhQu (Versi Lampiran)

ERD ini disusun mengikuti diagram yang Anda lampirkan (entitas: Admin, Dosen, Mahasiswa, Bidang Kompetensi, Bidang Pendukung, Peminatan, Kuis).

```mermaid
erDiagram
    ADMIN {
        integer id_admin PK
        string nama_admin
        string email
    }

    DOSEN {
        integer id_dosen PK
        string nip
        string nama_dosen
        string email
    }

    MAHASISWA {
        integer id_mahasiswa PK
        string nim
        string nama_mahasiswa
        string program_studi
        string fakultas
        string tahun_masuk
        ...
    }

    BIDANG_KOMPETENSI {
        integer id_kompetensi PK
        string nama_kompetensi
        string deskripsi
    }

    BIDANG_PENDUKUNG {
        integer id_pendukung PK
        string nama_pendukung
        integer bobot_nilai
    }

    PEMINATAN {
        integer id_peminatan PK
        string nama_peminatan
        string deskripsi
    }

    KUIS {
        integer id_kuis PK
        string pertanyaan
        integer bobot
    }

    %% Relasi inti (mengikuti notasi pada lampiran)
    ADMIN ||--o{ DOSEN : "mengelola"
    DOSEN ||--o{ MAHASISWA : "membimbing/menilai"
    MAHASISWA }o--o{ BIDANG_KOMPETENSI : "direkomendasikan"
    MAHASISWA }o--o{ BIDANG_PENDUKUNG : "mengikuti"
    BIDANG_KOMPETENSI ||--o{ PEMINATAN : "terkait / tersedia di"
    BIDANG_PENDUKUNG }o--o{ PEMINATAN : "memiliki / mendukung"
    PEMINATAN ||--o{ KUIS : "memiliki"

    %% Catatan: Many-to-many (M..N) direpresentasikan sebagai M..N (Mermaid erDiagram menggunakan }o--o{ )
```

---

## Penjelasan singkat
- **Admin** mengelola banyak **Dosen** (1..M).  
- **Dosen** dapat membimbing/ merekomendasikan banyak **Mahasiswa** (1..M).  
- **Mahasiswa** dapat terkait ke banyak **Bidang Kompetensi** dan banyak **Bidang Pendukung** (M..N).  
- **Peminatan** mengumpulkan/berkaitan dengan beberapa **Bidang Kompetensi** dan **Bidang Pendukung**; Peminatan juga memiliki beberapa **Kuis**.  

Jika Anda ingin, saya bisa:  
- menambahkan tabel junction (mis. `mahasiswa_kompetensi`, `mahasiswa_pendukung`, `peminatan_bidang`) dengan atribut (nilai, timestamp),  
- menghasilkan DDL SQL, atau  
- men-generate PNG/SVG berkualitas dari ERD ini.

Mau saya lanjutkan ke salah satu opsi tersebut? (contoh: "tambah junction + SQL + PNG")