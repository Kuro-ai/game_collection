from django.shortcuts import render, redirect
import random
from django.contrib.auth.decorators import login_required

# Original list of words for the game
WORDS = [
    "python",
    "django",
    "algorithm",
    "function",
    "variable",
    "iteration",
    "recursion",
    "framework",
    "backend",
    "frontend",
    "database",
    "template",
    "json",
    "html",
    "css",
    "javascript",
    "bootstrap",
    "react",
    "angular",
    "node",
    "flask",
    "array",
    "stack",
    "queue",
    "binary",
    "network",
    "encryption",
    "server",
    "client",
    "software",
    "compiler",
    "syntax",
    "debugging",
    "testing",
    "docker",
    "kubernetes",
    "api",
    "git",
    "repository",
    "commit",
    "branch",
    "merge",
    "authentication",
    "authorization",
    "session",
    "cookie",
    "hashing",
    "virtualization",
    "cloud",
    "protocol",
    "port",
    "firewall",
    "proxy",
    "cache",
    "thread",
    "process",
    "virtual",
    "kernel",
    "command",
    "interpreter",
    "loop",
    "script",
    "container",
    "token",
    "logic",
    "parsing",
    "regex",
    "metadata",
    "overflow",
    "pointer",
    "operator",
    "event",
    "iterator",
    "pipeline",
    "lambda",
]

@login_required(login_url='/login/')
def play(request):
    """Main game logic."""
    # Initialize game state if not already done
    if 'word' not in request.session:
        # Shuffle the word list and pick the first word
        shuffled_words = WORDS[:]
        random.shuffle(shuffled_words)
        request.session['word'] = random.choice(shuffled_words)
        request.session['guessed'] = []  # Store guessed letters
        request.session['lives'] = 6  # Number of lives
        request.session['display'] = '_' * len(request.session['word'])

    if request.method == 'POST':
        guess = request.POST.get('guess', '').lower()

        # Validate the input
        if len(guess) == 1 and guess.isalpha() and guess not in request.session['guessed']:
            request.session['guessed'].append(guess)
            word = request.session['word']
            display = list(request.session['display'])

            if guess in word:
                # Reveal guessed letter in display
                for index, letter in enumerate(word):
                    if letter == guess:
                        display[index] = guess
                request.session['display'] = ''.join(display)
            else:
                # Deduct a life for incorrect guess
                request.session['lives'] -= 1

            request.session.modified = True

    # Check for win or loss
    if '_' not in request.session['display']:
        message = 'Congratulations! You guessed the word!'
        return render(request, 'hangman/play.html', {'message': message, 'won': True})
    elif request.session['lives'] <= 0:
        message = f'Sorry, you lost! The word was {request.session["word"]}.'
        return render(request, 'hangman/play.html', {'message': message, 'lost': True})

    return render(request, 'hangman/play.html', {
        'display': request.session['display'],
        'lives': request.session['lives'],
        'guessed': request.session['guessed'],
    })


def reset(request):
    """Reset the game."""
    for key in ['word', 'guessed', 'lives', 'display']:
        request.session.pop(key, None)
    return redirect('hangman_play')
