from django.urls import path
from . import views

app_name='lights_out'
urlpatterns = [
    path('lights_out/', views.lights_out, name='lights_out_home'),
]
