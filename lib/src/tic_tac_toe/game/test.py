


from tic_tac_toe.logic.entities import Mark
from tic_tac_toe.logic.models import GameState, Grid


grid_cells = "XOXXO.XOXOO.O..XOX..O.X.."
game_state = GameState(
  grid=Grid(dimension=5, cells=grid_cells),
  initial_player_mark=Mark.CROSS,
)

winner = game_state.get_winner

print(winner)  # None