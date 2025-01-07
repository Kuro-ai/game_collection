from django.shortcuts import render, redirect
import random
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def start_game(request):
    """Initialize the game and set a random number in session."""
    if 'number' not in request.session:
        request.session['number'] = random.randint(1, 100)
        request.session['attempts'] = 0
    return render(request, 'guess_number/home.html')

def make_guess(request):
    """Handle the player's guess and provide range-based feedback."""
    if request.method == 'POST':
        guess = int(request.POST['guess'])
        target = request.session.get('number')
        request.session['attempts'] += 1
        difference = abs(guess - target)

        # Provide feedback based on the range
        if guess < target:
            if difference > 30:
                message = "Way too low! Try a much higher number."
            elif difference > 20:
                message = "Too low, but getting warmer!"
            elif difference > 10:
                message = "A bit low! You're close."
            else:
                message = "Very close, but still a little low!"
        elif guess > target:
            if difference > 30:
                message = "Way too high! Try a much lower number."
            elif difference > 20:
                message = "Too high, but getting warmer!"
            elif difference > 10:
                message = "A bit high! You're close."
            else:
                message = "Very close, but still a little high!"
        else:
            return render(request, 'guess_number/result.html', {
                'attempts': request.session['attempts']
            })

        return render(request, 'guess_number/home.html', {
            'message': message,
        })

    return redirect('guess_number:guess_number_home')

def restart_game(request):
    """Restart the game."""
    request.session.flush()  # Clear session data
    return redirect('guess_number:guess_number_home')
