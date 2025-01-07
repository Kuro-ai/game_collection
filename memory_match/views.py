from django.shortcuts import render
from random import shuffle
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def play_game(request):
    # 20 pairs of icons (40 cards)
    icons = [
        '🍎', '🍌', '🍇', '🍓', '🍉', '🥝', '🍒', '🍍', 
        '🍋', '🥥', '🥭', '🍑', '🍏', '🍐', '🍊', '🍔',
        '🍕', '🌮', '🌯', '🥗'
    ]
    # Create 40 cards by duplicating each icon for matching pairs
    cards = [{'id': i, 'value': icon} for i, icon in enumerate(icons * 2, 1)]  # Duplicate each icon
    shuffle(cards)  # Shuffle the cards for randomness
    context = {'cards': cards}
    return render(request, 'memory_match/play.html', context)
