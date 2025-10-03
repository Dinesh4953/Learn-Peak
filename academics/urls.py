# academics/urls.py

from django.urls import path
from .views import CourseListView, CourseDetailView, SubjectList, branch_subject_view, ask_gemini
from academics import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('courses/', CourseListView.as_view(), name='course_list'),
    path('course/<int:pk>/', CourseDetailView.as_view(), name='course_detail'),
    path('subjects', SubjectList.as_view(), name='subject_list'),
    path('subjects/select-branch/', views.branch_subject_view, name='branch_subjects'),
    path("ai/", views.ask_gemini, name="ask_gemini"),
    path("run_code/", views.run_code, name="run_code"),
    path("run_code_big/", views.run_code_big, name="run_code_big")
    # path("languages/", views.languages, name="languages"),
    # path("languages/python", views.python_language, name="python_language")
    
]
