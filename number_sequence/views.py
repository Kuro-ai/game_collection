import random
import time
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def generate_sequence():
    """Generate a more advanced sequence."""
    sequence_type = random.choice(["arithmetic", "geometric", "squares", "cubes", "fibonacci"])

    if sequence_type == "arithmetic":
        start = random.randint(1, 10)
        diff = random.randint(1, 5)
        return [start + diff * i for i in range(5)]

    elif sequence_type == "geometric":
        start = random.randint(1, 5)
        ratio = random.randint(2, 4)
        return [start * (ratio ** i) for i in range(5)]

    elif sequence_type == "squares":
        start = random.randint(1, 3)
        return [start**2 + i**2 for i in range(5)]

    elif sequence_type == "cubes":
        start = random.randint(1, 3)
        return [start**3 + i**3 for i in range(5)]

    elif sequence_type == "fibonacci":
        a, b = random.randint(1, 5), random.randint(1, 5)
        sequence = [a, b]
        for _ in range(3):
            sequence.append(sequence[-1] + sequence[-2])
        return sequence

@login_required(login_url='/login/')
def number_sequence_game(request):
    # Initialize game state if not already set
    if 'sequence' not in request.session:
        request.session['sequence'] = generate_sequence()
        request.session['score'] = 0
        request.session['step'] = 4  # Index of the number the user guesses
        request.session['lives'] = 3  # Player starts with 3 lives

    sequence = request.session['sequence']
    step = request.session['step']
    lives = request.session['lives']
    game_over = False  # Flag to indicate game over state

    # Check the user's guess
    if request.method == 'POST':
        user_guess = request.POST.get('guess')
        if user_guess.isdigit() and int(user_guess) == sequence[step]:
            request.session['score'] += 1
            # Generate a new sequence immediately
            request.session['sequence'] = generate_sequence()
            request.session['step'] = 4
        else:
            request.session['lives'] = max(0, lives - 1)
            if request.session['lives'] == 0:
                game_over = True  # Set the game-over flag

    context = {
        'sequence': request.session['sequence'][:4],  # Display the first four numbers
        'score': request.session['score'],
        'lives': request.session['lives'],
        'game_over': game_over,
        'correct_answer': sequence[step] if game_over else None,
    }
    return render(request, 'number_sequence/game.html', context)

def restart_game(request):
    """Restart the game by clearing the session data."""
    # Clear only game-related session data
    for key in ["sequence", "score", "step", "lives"]:
        if key in request.session:
            del request.session[key]
    return redirect('number_sequence_game')



