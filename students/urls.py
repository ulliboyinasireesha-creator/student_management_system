from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.student_create, name='student_create'),
    path('students/<int:pk>/', views.student_detail, name='student_detail'),
    path('students/<int:pk>/edit/', views.student_update, name='student_update'),
    path('students/<int:pk>/delete/', views.student_delete, name='student_delete'),
    path('students/export/', views.student_export_csv, name='student_export_csv'),

    path('departments/', views.department_list, name='department_list'),
    path('departments/add/', views.department_create, name='department_create'),

    path('courses/', views.course_list, name='course_list'),
    path('courses/add/', views.course_create, name='course_create'),
]
