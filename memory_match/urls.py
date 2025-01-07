from django.urls import path
from . import views

app_name = 'memory_match'

urlpatterns = [
    path('play/', views.play_game, name='play_game'),
]
