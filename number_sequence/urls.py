from django.urls import path
from . import views

urlpatterns = [
    path('', views.number_sequence_game, name='number_sequence_game'),
    path('restart/', views.restart_game, name='restart_game'),
]
