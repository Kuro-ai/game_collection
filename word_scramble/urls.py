from django.urls import path
from . import views

urlpatterns = [
    path('', views.game, name='word_scramble'),
    path('word_scramble/next/', views.next_word, name='next_word_scramble'),  
    path('word_scramble/check/', views.check_answer, name='check_word_scramble'),
    path('word_scramble/hint/', views.show_hint, name='show_hint'),
    path('word_scramble/restart/', views.restart_game, name='restart_word_scramble'),
]
