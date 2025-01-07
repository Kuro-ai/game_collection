from django.urls import path
from . import views

app_name='guess_number'
urlpatterns = [
    path('', views.start_game, name='guess_number_home'),
    path('guess/', views.make_guess, name='make_guess'),
    path('restart/', views.restart_game, name='restart_game'),
]
