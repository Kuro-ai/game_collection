from django.shortcuts import render
from django.http import JsonResponse
import random
from django.contrib.auth.decorators import login_required

def initialize_game():
    """Initialize a 4x4 grid with two random tiles."""
    grid = [[0] * 4 for _ in range(4)]
    add_random_tile(grid)
    add_random_tile(grid)
    return grid

def add_random_tile(grid):
    """Add a random tile (2 or 4) to an empty spot on the grid."""
    empty_cells = [(r, c) for r in range(4) for c in range(4) if grid[r][c] == 0]
    if empty_cells:
        r, c = random.choice(empty_cells)
        grid[r][c] = random.choice([2, 4])

def move_left(grid):
    """Move and merge tiles to the left."""
    moved = False
    score = 0
    for row in grid:
        non_zero = [x for x in row if x != 0]
        merged_row = []
        skip = False
        for i in range(len(non_zero)):
            if skip:
                skip = False
                continue
            if i + 1 < len(non_zero) and non_zero[i] == non_zero[i + 1]:
                merged_row.append(non_zero[i] * 2)
                score += non_zero[i] * 2
                skip = True
            else:
                merged_row.append(non_zero[i])
        merged_row.extend([0] * (4 - len(merged_row)))
        if merged_row != row:
            moved = True
        row[:] = merged_row
    return moved, score

def rotate_grid(grid):
    """Rotate the grid clockwise."""
    return [list(reversed(col)) for col in zip(*grid)]

def move(grid, direction):
    """
    Handle movement in the specified direction:
    0 = up, 1 = right, 2 = down, 3 = left.
    """
    # Adjust rotations for each direction
    rotation_mapping = {0: 3, 1: 2, 2: 1, 3: 0}  # Adjusted mapping

    for _ in range(rotation_mapping[direction]):
        grid = rotate_grid(grid)
    moved, score = move_left(grid)
    for _ in range(4 - rotation_mapping[direction]):
        grid = rotate_grid(grid)
    if moved:
        add_random_tile(grid)
    return moved, score, grid


def is_game_over(grid):
    """Check if the game is over."""
    for r in range(4):
        for c in range(4):
            if grid[r][c] == 0:
                return False
            if r > 0 and grid[r][c] == grid[r - 1][c]:
                return False
            if c > 0 and grid[r][c] == grid[r][c - 1]:
                return False
    return True

@login_required(login_url='/login/')
def game(request):
    """Handle game rendering and AJAX requests."""
    if request.method == "GET":
        grid = initialize_game()
        request.session['grid'] = grid
        request.session['score'] = 0
        return render(request, '2048/home.html', {'grid': grid, 'score': 0})
    elif request.method == "POST":
        direction = int(request.POST.get('direction'))
        grid = request.session['grid']
        score = request.session['score']
        moved, points, grid = move(grid, direction)
        score += points
        request.session['grid'] = grid
        request.session['score'] = score
        game_over = is_game_over(grid)
        return JsonResponse({'grid': grid, 'score': score, 'game_over': game_over})
