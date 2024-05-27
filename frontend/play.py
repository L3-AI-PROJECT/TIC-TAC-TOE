from tic_tac_toe.logic.algorithms import minimax, find_best_move_minimax
from tic_tac_toe.logic.models import GameState, Grid, Mark

def preview(grid: str, dimension: int):
  for i in range(0, len(grid), dimension):
    print(grid[i:i+dimension])
  print("-" * 10)


from tic_tac_toe.logic.algorithms import find_best_move_minimax, find_best_move_alpha_beta
from tic_tac_toe.logic.models import GameState, Grid, Mark, Move

dimension = 6

# Create a list representing the initial state of the grid
# "." represents an empty cell
cells = ["."] * (dimension * dimension)

# Add some marks to the grid
cells[dimension*1 + 1] = "X"
cells[dimension*2 + 2] = "X"
cells[dimension*3 + 3] = "X"
cells[dimension*1 + 2] = "O"
cells[dimension*2 + 3] = "O"
cells[dimension*3 + 4] = "O"

# Convert the list back to a string
cells = "".join(cells)

game_state = GameState(
  grid=Grid(dimension, cells), 
  initial_player_mark=Mark("X"),
  required_marks_for_win=4  # Adjust this value as needed
)

def printMove(move: Move):
  print(f"Position: {game_state.get_move_format_from_index(move.position)}")

# Print the initial state of the grid
preview(game_state.grid.cells, dimension)

# Find the best move using the minimax algorithm
# best_move = find_best_move_minimax(game_state, depth=2)

# Find the best move using the alpha-beta pruning algorithm
best_move = find_best_move_alpha_beta(game_state, depth=3)

# Print the best move
printMove(best_move)

