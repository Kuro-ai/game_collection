from django.urls import path
from . import views

urlpatterns = [
    path('', views.play, name='hangman_play'),
    path('reset/', views.reset, name='hangman_reset'),
]
