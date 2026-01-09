from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from unfold.admin import ModelAdmin
from unfold.forms import UserChangeForm, UserCreationForm
from django.utils.safestring import mark_safe
from django.urls import reverse
from .models import User, Student, Examiner, Group, Evaluation

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

@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ("username", "email", "role", "is_active", "is_staff")
    list_filter = ("role", "is_active", "is_staff")
    
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {"fields": ("role",)}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {"fields": ("role",)}),
    )

    inlines = [StudentInline, ExaminerInline]

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        
        # Only show relevant inline based on role
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

@admin.register(Student)
class StudentAdmin(ModelAdmin):
    list_display = ('nama', 'nim', 'semester', 'jumlah_hafalan', 'is_verified', 'status_seleksi', 'change_password_link')
    search_fields = ('nama', 'nim', 'user__username', 'email')
    list_filter = ('is_verified', 'status_seleksi', 'semester', 'jumlah_hafalan')
    compressed_fields = True 
    list_filter_sheet = True 

    def change_password_link(self, obj):
        if obj.user:
            url = reverse("admin:scholarship_user_change", args=[obj.user.id]) + "password/"
            return mark_safe(f'<a href="{url}" class="bg-primary-600 text-white px-3 py-1 rounded-md text-xs font-bold hover:bg-primary-700 transition">Ubah Password</a>')
        return "-"
    change_password_link.short_description = "Aksi Akun"

@admin.register(Examiner)
class ExaminerAdmin(ModelAdmin):
    list_display = ('nama', 'email', 'nomor_telepon', 'user', 'change_password_link')
    search_fields = ('nama', 'email', 'user__username')
    list_filter = ('groups',)

    def change_password_link(self, obj):
        if obj.user:
            url = reverse("admin:scholarship_user_change", args=[obj.user.id]) + "password/"
            return mark_safe(f'<a href="{url}" class="bg-primary-600 text-white px-3 py-1 rounded-md text-xs font-bold hover:bg-primary-700 transition">Ubah Password</a>')
        return "-"
    change_password_link.short_description = "Aksi Akun"

@admin.register(Group)
class GroupAdmin(ModelAdmin):
    list_display = ('nama_group', 'examiner', 'get_member_count')
    search_fields = ('nama_group', 'examiner__nama')
    filter_horizontal = ('members',)
    
    def get_member_count(self, obj):
        return obj.members.count()
    get_member_count.short_description = "Jumlah Anggota"

@admin.register(Evaluation)
class EvaluationAdmin(ModelAdmin):
    list_display = ('student', 'examiner', 'wsm_score', 'is_published', 'created_at')
    list_filter = ('is_published', 'examiner', 'created_at')
    search_fields = ('student__nama', 'examiner__nama')
    readonly_fields = ('wsm_score',)
