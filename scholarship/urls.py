from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_student, name='register_student'),
    path('apply/', views.apply_scholarship, name='apply_scholarship'),
    path('create-examiner/', views.create_examiner, name='create_examiner'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('examiner/dashboard/', views.examiner_dashboard, name='examiner_dashboard'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/verification/', views.verification_list, name='verification_list'),
    path('admin/verify/<int:student_id>/', views.verify_student, name='verify_student'),
    path('admin/create-examiner/', views.create_examiner, name='create_examiner'),
    path('admin/create-group/', views.create_group, name='create_group'),
    path('examiner/evaluate/<int:student_id>/', views.evaluate_student, name='evaluate_student'),
    path('admin/announce/', views.announce_results, name='announce_results'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
]