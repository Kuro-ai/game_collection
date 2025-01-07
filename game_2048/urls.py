from django.urls import path
from . import views

urlpatterns = [
    path('2048/', views.game, name='2048'),
]
