from django.urls import path
from .views import Register, Loginn, AdminDashboardView, TeacherDashboardView, StudentDashboardView

urlpatterns = [
    path('register',Register.as_view(),name='register'),
    path('loginn', Loginn.as_view(), name='loginn'),
    path('admin_dashboard',AdminDashboardView.as_view(), name='admin_dashboard'),
    path('teacher_dashboard',TeacherDashboardView.as_view(), name='teacher_dashboard'),
    path('student_dashboard',StudentDashboardView.as_view(), name='student_dashboard'),
]