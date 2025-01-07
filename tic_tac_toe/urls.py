from django.urls import path
from . import views

app_name = 'tic_tac_toe'

urlpatterns = [
    path('', views.home, name='tic_tac_toe_home'),
    path("make_move/", views.make_move, name="make_move"),
    path("reset_game/", views.reset_game, name="reset_game"),
]
