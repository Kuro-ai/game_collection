from django.shortcuts import render, redirect
import random
import time
import math
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def lights_out(request):
    size = 5  # Define the board size (5x5)

    # Initialize the game board
    if 'board' not in request.session or request.method == 'POST' and 'restart' in request.POST:
        board = [[random.randint(0, 1) for _ in range(size)] for _ in range(size)]  # Randomized lights
        while all(cell == 0 for row in board for cell in row):  # Ensure it's not already "lights out"
            board = [[random.randint(0, 1) for _ in range(size)] for _ in range(size)]
        request.session['board'] = board
        request.session['start_time'] = int(time.time())  # Store as integer for simplicity
        request.session.modified = True
    else:
        board = request.session['board']

    # Calculate elapsed time as an integer
    elapsed_time = int(time.time()) - request.session.get('start_time', int(time.time()))

    if request.method == 'POST' and 'cell' in request.POST:
        # Get the clicked cell coordinates
        x, y = map(int, request.POST['cell'].split(','))

        # Toggle the clicked cell and its neighbors
        for dx, dy in [(0, 0), (0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < size and 0 <= ny < size:
                board[nx][ny] = 1 - board[nx][ny]  # Toggle between 0 (off) and 1 (on)

        # Update the session
        request.session['board'] = board
        request.session.modified = True

        # Check for win condition after toggling
        if all(cell == 0 for row in board for cell in row):  # Check if all cells are off
            elapsed_time = int(time.time()) - request.session.get('start_time', int(time.time()))
            return render(request, 'lights_out/home.html', {
                'board': board,
                'won': True,
                'elapsed_time': elapsed_time
            })

    return render(request, 'lights_out/home.html', {
        'board': board,
        'won': False,
        'elapsed_time': elapsed_time
    })
