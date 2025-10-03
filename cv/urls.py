from django.contrib import admin
from django.urls import path, include
from cv import views
urlpatterns = [
    path('accept/', views.accept, name="accept"),

]

