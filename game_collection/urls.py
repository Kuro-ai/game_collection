"""
URL configuration for game_collection project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('tic-tac-toe/', include('tic_tac_toe.urls')),
    path('connect-four/', include('connect_four.urls')),
    path('snake_game/', include('snake_game.urls')),
    path('guess_number/', include('guess_number.urls')),
    path('lights_out/', include('lights_out.urls')),
    path('memory_match/', include('memory_match.urls')),
    path("word_scramble/", include("word_scramble.urls")),
    path('hangman/', include('hangman.urls')),
    path('number-sequence/', include('number_sequence.urls')),
    path('2048/', include('game_2048.urls')),
]

