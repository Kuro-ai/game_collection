from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def snake_game(request):
    """
    Render the Snake game page.
    """
    return render(request, 'snake_game/home.html')

