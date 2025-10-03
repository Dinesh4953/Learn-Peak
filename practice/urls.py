from django.urls import path
from .import views


urlpatterns = [
    path('problems/', views.problem_list, name='problem_list'),
        path('problems/<int:pk>/', views.problem_detail, name='problem_detail'),  
        path('solved/', views.problem_list_1, name='solved_problems'),
         path('problems_solved/<int:pk>/', views.problem_detail_solved, name='problem_detail_solved'),
         
]
