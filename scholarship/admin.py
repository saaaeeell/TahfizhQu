from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from unfold.admin import ModelAdmin
from unfold.decorators import action
from import_export.admin import ImportMixin, ExportMixin
from unfold.contrib.import_export.forms import ExportForm, ImportForm
from unfold.forms import UserChangeForm, UserCreationForm, AdminPasswordChangeForm
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.shortcuts import redirect

from .models import User, Student, Examiner, Group, Evaluation
from .resources import StudentResource, ExaminerResource


# =====================================================
# INLINE PROFILE
# =====================================================
class StudentInline(admin.StackedInline):
    model = Student
    can_delete = False
    verbose_name_plural = 'Profil Mahasiswa'
    fk_name = 'user'


class ExaminerInline(admin.StackedInline):
    model = Examiner
    can_delete = False
    verbose_name_plural = 'Profil Penguji'
    fk_name = 'user'


# =====================================================
# USER ADMIN
# =====================================================
@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

    list_display = ("username", "email", "role", "is_active", "is_staff")
    list_filter = ("role", "is_active", "is_staff")
    search_fields = ("username", "email")

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Informasi Pribadi", {"fields": ("first_name", "last_name", "email", "role")}),
        (
            "Izin & Akses",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Riwayat", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {"fields": ("role",)}),
    )

    inlines = [StudentInline, ExaminerInline]

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []

        inline_instances = []
        for inline_class in self.inlines:
            if inline_class == StudentInline and obj.role == 'student':
                inline_instances.append(inline_class(self.model, self.admin_site))
            elif inline_class == ExaminerInline and obj.role == 'examiner':
                inline_instances.append(inline_class(self.model, self.admin_site))
        return inline_instances

    actions = ['activate_users', 'deactivate_users']

    @admin.action(description="Aktifkan pengguna terpilih")
    def activate_users(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "Pengguna terpilih telah diaktifkan.")
    activate_users.icon = "check_circle"

    @admin.action(description="Nonaktifkan pengguna terpilih")
    def deactivate_users(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "Pengguna terpilih telah dinonaktifkan.")
    deactivate_users.icon = "cancel"


# =====================================================
# STUDENT ADMIN
# =====================================================
@admin.register(Student)
class StudentAdmin(ImportMixin, ExportMixin, ModelAdmin):
    resource_class = StudentResource
    import_form_class = ImportForm
    export_form_class = ExportForm

    list_display = (
        'nama', 'nim', 'semester', 'jumlah_hafalan',
        'is_verified', 'status_seleksi', 'change_password_link'
    )
    search_fields = ('nama', 'nim', 'user__username', 'email')
    list_filter = ('is_verified', 'status_seleksi', 'semester', 'jumlah_hafalan')

    compressed_fields = True
    list_filter_sheet = True
    actions_list = ["download_template_action"]

    @action(description="Unduh Template CSV", icon="download")
    def download_template_action(self, request):
        return redirect("download_student_template")

    def change_password_link(self, obj):
        if obj.user:
            url = reverse("admin:scholarship_user_change", args=[obj.user.id]) + "password/"
            return mark_safe(
                f'<a href="{url}" '
                f'class="inline-flex items-center px-2.5 py-1.5 text-xs font-medium rounded '
                f'text-white bg-emerald-600 hover:bg-emerald-700 transition">'
                f'🔑 Ubah Sandi</a>'
            )
        return "-"
    change_password_link.short_description = "Aksi Akun"


# =====================================================
# EXAMINER ADMIN
# =====================================================
@admin.register(Examiner)
class ExaminerAdmin(ImportMixin, ExportMixin, ModelAdmin):
    resource_class = ExaminerResource
    import_form_class = ImportForm
    export_form_class = ExportForm

    list_display = ('nama', 'email', 'nomor_telepon', 'user', 'change_password_link')
    search_fields = ('nama', 'email', 'user__username')
    list_filter = ('groups',)

    compressed_fields = True
    list_filter_sheet = True
    actions_list = ["download_template_action"]

    @action(description="Unduh Template CSV", icon="download")
    def download_template_action(self, request):
        return redirect("download_examiner_template")

    def change_password_link(self, obj):
        if obj.user:
            url = reverse("admin:scholarship_user_change", args=[obj.user.id]) + "password/"
            return mark_safe(
                f'<a href="{url}" '
                f'class="inline-flex items-center px-2.5 py-1.5 text-xs font-medium rounded '
                f'text-white bg-emerald-600 hover:bg-emerald-700 transition">'
                f'🔑 Ubah Sandi</a>'
            )
        return "-"
    change_password_link.short_description = "Aksi Akun"


# =====================================================
# GROUP ADMIN (✨ DIBATASI: HANYA STUDENT TERVERIFIKASI)
# =====================================================
@admin.register(Group)
class GroupAdmin(ModelAdmin):
    list_display = ('nama_group', 'examiner', 'get_member_count')
    search_fields = ('nama_group', 'examiner__nama')
    filter_horizontal = ('members',)

    compressed_fields = True

    def get_member_count(self, obj):
        return obj.members.count()
    get_member_count.short_description = "Jumlah Anggota"

    # 🔒 PEMBATASAN UTAMA:
    # HANYA STUDENT DENGAN is_verified=True YANG BISA DIPILIH
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "members":
            kwargs["queryset"] = Student.objects.filter(is_verified=True)
        return super().formfield_for_manytomany(db_field, request, **kwargs)


# =====================================================
# EVALUATION ADMIN
# =====================================================
@admin.register(Evaluation)
class EvaluationAdmin(ModelAdmin):
    list_display = ('student', 'examiner', 'wsm_score', 'is_published', 'created_at')
    list_filter = ('is_published', 'examiner', 'created_at')
    search_fields = ('student__nama', 'examiner__nama')

    readonly_fields = ('wsm_score',)

    compressed_fields = True
    list_filter_sheet = True
