from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', CatView.as_view()),
    path('details/<int:id>', CatDetails.as_view()),
    path('register/', Register.as_view())
]