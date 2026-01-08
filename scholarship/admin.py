from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from unfold.admin import ModelAdmin
from .models import User, Student, Examiner, Group, Evaluation

@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    # Disable delete permission
    def has_delete_permission(self, request, obj=None):
        return False

    actions = ['activate_users', 'deactivate_users']

    def activate_users(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "Selected users have been activated.")
    activate_users.short_description = "Activate selected users"

    def deactivate_users(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "Deactivate selected users")
    deactivate_users.short_description = "Deactivate selected users"

@admin.register(Student)
class StudentAdmin(ModelAdmin):
    list_display = ('nama', 'nim', 'semester', 'jumlah_hafalan', 'kampus')
    search_fields = ('nama', 'nim')
    list_filter = ('semester', 'jumlah_hafalan')

@admin.register(Examiner)
class ExaminerAdmin(ModelAdmin):
    list_display = ('nama', 'email', 'nomor_telepon')
    search_fields = ('nama', 'email')

@admin.register(Group)
class GroupAdmin(ModelAdmin):
    list_display = ('nama_group', 'examiner')
    search_fields = ('nama_group',)
    filter_horizontal = ('members',)

@admin.register(Evaluation)
class EvaluationAdmin(ModelAdmin):
    list_display = ('student', 'examiner', 'wsm_score', 'is_published', 'created_at')
    list_filter = ('is_published', 'examiner')
    readonly_fields = ('wsm_score',)
