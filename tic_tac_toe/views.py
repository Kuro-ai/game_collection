from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

# Define winning combinations
WINNING_COMBINATIONS = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
]

# Initial game state
def get_initial_game_state():
    return {
        "board": [""] * 9,  # 9 cells, empty initially
        "isCircleTurn": False,
        "winner": None,
        "draw": False,
    }

# Main view for the game
@login_required(login_url='/login/')
def home(request):
    if "game_state" not in request.session:
        request.session["game_state"] = get_initial_game_state()
    return render(request, "tic_tac_toe/home.html", {"game_state": request.session["game_state"]})

# Handle move requests
def make_move(request):
    if request.method == "POST":
        cell_index = int(request.POST.get("cell_index"))
        game_state = request.session.get("game_state", get_initial_game_state())

        # If cell is already taken or game over, return
        if game_state["board"][cell_index] or game_state["winner"] or game_state["draw"]:
            return JsonResponse({"status": "invalid move"})

        # Determine the current player
        current_class = "O" if game_state["isCircleTurn"] else "X"
        game_state["board"][cell_index] = current_class

        # Check for win or draw
        if check_win(game_state["board"], current_class):
            game_state["winner"] = current_class
        elif all(cell != "" for cell in game_state["board"]):
            game_state["draw"] = True

        # Switch turn
        game_state["isCircleTurn"] = not game_state["isCircleTurn"]

        # Save state back to session
        request.session["game_state"] = game_state
        return JsonResponse({"status": "success", "game_state": game_state})

    return JsonResponse({"status": "invalid request"})

# Reset game
def reset_game(request):
    request.session["game_state"] = get_initial_game_state()
    return redirect("tic_tac_toe:tic_tac_toe_home")

# Helper to check win
def check_win(board, current_class):
    return any(all(board[i] == current_class for i in combo) for combo in WINNING_COMBINATIONS)
