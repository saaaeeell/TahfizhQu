from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_student, name='register_student'),
    path('apply/', views.apply_scholarship, name='apply_scholarship'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('examiner/dashboard/', views.examiner_dashboard, name='examiner_dashboard'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/', RedirectView.as_view(url='dashboard/', permanent=True)),
    path('admin/verification/', views.verification_list, name='verification_list'),
    path('admin/verify/<int:student_id>/', views.verify_student, name='verify_student'),
    path('admin/create-examiner/', views.create_examiner, name='create_examiner'),
    path('admin/create-group/', views.create_group, name='create_group'),
    path('admin/students/', views.admin_students, name='admin_students'),
    path('admin/groups/', views.admin_groups, name='admin_groups'),
    path('admin/group/<int:group_id>/', views.admin_group_detail, name='admin_group_detail'),
    path('admin/examiners/', views.admin_examiners, name='admin_examiners'),
    path('admin/examiner/<int:examiner_id>/', views.admin_examiner_detail, name='admin_examiner_detail'),
    path('examiner/evaluate/<int:student_id>/', views.evaluate_student, name='evaluate_student'),
    path('admin/evaluations/', views.admin_evaluations, name='admin_evaluations'),
    path('admin/evaluations/not-evaluated/', views.admin_not_evaluated, name='admin_not_evaluated'),
    path('admin/evaluations/recent/', views.admin_recent_evaluations, name='admin_recent_evaluations'),
    path('admin/announce/', views.announce_results, name='announce_results'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('admin/template/student/', views.download_student_template, name='download_student_template'),
    path('admin/template/examiner/', views.download_examiner_template, name='download_examiner_template'),
]