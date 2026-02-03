# Use Case Diagram — TahfizhQu ✅

Dokumentasi singkat use case untuk proyek TahfizhQu.

## Aktor
- **Student** — pengguna mahasiswa yang mendaftar beasiswa dan melihat dashboard.
- **Examiner** — penguji yang melakukan evaluasi ke mahasiswa.
- **Admin** — pengelola sistem (verifikasi, membuat examiner/group, mengumumkan hasil, melihat laporan).
- **System (Email)** — subsistem yang mengirim notifikasi/verifikasi email.

---

## Diagram Use Case (Mermaid)

```mermaid
%%{init: {'theme':'base'}}%%
usecaseDiagram
    actor Student
    actor Examiner
    actor Admin
    actor System as Email

    Student --> (Register)
    Student --> (Verify Email)
    Student --> (Login)
    Student --> (Apply for Scholarship)
    Student --> (View Student Dashboard)

    Examiner --> (Login)
    Examiner --> (View Examiner Dashboard)
    Examiner --> (Evaluate Student)

    Admin --> (Login)
    Admin --> (View Admin Dashboard)
    Admin --> (Verify Student)
    Admin --> (Create Examiner)
    Admin --> (Create Group)
    Admin --> (Assign Students to Group)
    Admin --> (View Students/Groups/Evaluations)
    Admin --> (Announce Results)
    Admin --> (Download Templates)

    Email --> (Send Verification Email)
    Email --> (Send Confirmation Email)
    Email --> (Send Evaluation Notification)
    Email --> (Send Final Result Email)

    (Register) ..> (Send Verification Email) : <<include>>
    (Apply for Scholarship) ..> (Send Confirmation Email) : <<include>>
    (Verify Student) ..> (Send Verification Email) : <<extend>>
    (Evaluate Student) ..> (Send Evaluation Notification) : <<include>>
    (Announce Results) ..> (Send Final Result Email) : <<include>>
```

---

## Keterangan singkat use case
1. **Register**: mahasiswa membuat akun; sistem mengirim email verifikasi. (views: `register_student`)
2. **Verify Email / Activate**: mahasiswa klik tautan aktivasi, akun diaktifkan. (views: `activate`)
3. **Login**: autentikasi dan redirect ke dashboard sesuai peran. (views: `login_view`)
4. **Apply for Scholarship**: mahasiswa mengisi atau mengedit pendaftaran beasiswa; konfirmasi email dikirim. (views: `apply_scholarship`)
5. **Verify Student**: admin memverifikasi data mahasiswa, mengaktifkan akun, sistem kirim email notifikasi. (views: `verify_student`, `verification_list`)
6. **Create Examiner / Group**: admin menambahkan penguji dan membuat grup, mengundang mahasiswa (email). (views: `create_examiner`, `create_group`)
7. **Evaluate Student**: penguji mengisi evaluasi; sistem kirim notifikasi selesai evaluasi. (views: `evaluate_student`)
8. **Announce Results**: admin mem-publish hasil evaluasi dan mengirim email final ke mahasiswa. (views: `announce_results`)
9. **Download Templates**: admin mengunduh template CSV untuk import. (views: `download_student_template`, `download_examiner_template`)

---

Jika Anda mau, saya bisa: 
- menambahkan file gambar PNG/SVG dari diagram (meng-generate dengan PlantUML atau mermaid-cli) ✅
- menambahkan use case lebih rinci untuk tiap endpoint 🔧

Mau saya tambahkan output gambar diagramnya juga? 💡