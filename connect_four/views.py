from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Constants for the board
ROWS = 6
COLS = 7
EMPTY = " "

# Initialize board
def initialize_board():
    return [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]

# Check if the board is full
def is_board_full(board):
    return all(cell != EMPTY for row in board for cell in row)

# Check for a win
def check_win(board, player):
    # Horizontal Check
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == player for i in range(4)):
                return True

    # Vertical Check
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == player for i in range(4)):
                return True

    # Diagonal Check (\ direction)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True

    # Diagonal Check (/ direction)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True

    return False

@login_required(login_url='/login/')
def home(request):
    # Ensure session variables are initialized on the first visit
    if "board" not in request.session:
        request.session["board"] = initialize_board()
        request.session["current_player"] = "🔴"  # Set player 1 (red)
        request.session["winner"] = None

    # Safely fetch session variables using get(), to avoid KeyError
    board = request.session.get("board")
    current_player = request.session.get("current_player")
    winner = request.session.get("winner")

    # Handle form submission (player's move or reset game)
    if request.method == "POST":
        if "reset" in request.POST:
            # Clear only game-related session data
            for key in ["board", "current_player", "winner"]:
                if key in request.session:
                    del request.session[key]
            return redirect("connect_four:connect_four_home")

        if not winner:
            col = request.POST.get("col")  # Expect column index from the POST data

            if col is None:
                return render(request, "connect_four/home.html", {
                    "board": board,
                    "current_player": current_player,
                    "winner": winner,
                    "error": "No column selected!",
                })

            try:
                col = int(col)
            except ValueError:
                return render(request, "connect_four/home.html", {
                    "board": board,
                    "current_player": current_player,
                    "winner": winner,
                    "error": "Invalid column value!",
                })

            # Place the piece in the lowest available cell of the selected column
            for row in reversed(range(ROWS)):  # Start from the bottom row
                if board[row][col] == EMPTY:
                    board[row][col] = current_player
                    break
            else:
                # If column is full, do nothing
                return render(request, "connect_four/home.html", {
                    "board": board,
                    "current_player": current_player,
                    "winner": winner,
                    "error": "Column is full!",
                })

            # Check for a winner
            if check_win(board, current_player):
                request.session["winner"] = current_player
            elif is_board_full(board):
                # Check if the board is full (draw condition)
                request.session["winner"] = "Draw"
            else:
                # Switch players
                request.session["current_player"] = "🟡" if current_player == "🔴" else "🔴"

            # Save the updated board
            request.session["board"] = board

            # Render the page immediately with the winner message if a winner is found
            return render(request, "connect_four/home.html", {
                "board": board,
                "current_player": request.session["current_player"],
                "winner": request.session["winner"],
                "columns": range(COLS),  # Pass column indices to the template
            })

    return render(request, "connect_four/home.html", {
        "board": board,
        "current_player": current_player,
        "winner": winner,
        "columns": range(COLS),  # Pass column indices to the template
    })
