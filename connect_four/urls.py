from django.urls import path
from . import views

app_name = "connect_four"

urlpatterns = [
    path("", views.home, name="connect_four_home"),
]
