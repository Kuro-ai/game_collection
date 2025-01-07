from django.urls import path
from . import views

app_name = 'snake_game'
urlpatterns = [
    path('', views.snake_game, name='snake_game_home'),
]

