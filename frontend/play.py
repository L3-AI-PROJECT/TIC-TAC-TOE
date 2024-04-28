from tic_tac_toe.logic.algorithms import minimax, find_best_move_minimax
from tic_tac_toe.logic.models import GameState, Grid, Mark

def preview(grid: str, dimension: int):
  for i in range(0, len(grid), dimension):
    print(grid[i:i+dimension])
  print("-" * 10)

dimension = 10

cells = "."*34
cells += "X" + "."*9
cells += "X" + "."*9
cells += "XO" + "."*10
cells += "O" + "."*33

game_state = GameState(
  grid=Grid(dimension, cells), 
  initial_player_mark=Mark("X"),
  required_marks_for_win=5
)

moves = [game_state.make_move_to(position) for position in game_state.get_valid_moves]

preview(game_state.grid.cells, dimension)
for move in moves:
  print("Move: ", game_state.get_move_format_from_index(move.position))
  # min_score = minimax(move, maximizer=Mark("O"),  depth=2, choose_higher_score=False)
  min_score = minimax(move, maximizer=Mark("X"),  depth=2, choose_higher_score=True)
  max_score = minimax(move, maximizer=Mark("O"),  depth=2, choose_higher_score=True)
  print(f"Min Score: {min_score}\nMax Score: {max_score}")
  preview(move.next_state.grid.cells, dimension)

# best_move = find_best_move_minimax(
#   game_state, 
#   depth=3, 
#   choose_higher_score=True,
#   )

# print("(MAX) Best Move: " + game_state.get_move_format_from_index(best_move.position))
# preview(best_move.next_state.grid.cells, dimension)

# best_move = find_best_move_minimax(
#   game_state, 
#   depth=3, 
#   choose_higher_score=False,
#   )

# print("(MIN) Best Move: " + game_state.get_move_format_from_index(best_move.position))
# preview(best_move.next_state.grid.cells, dimension)