from tic_tac_toe.logic.models import GameState, Grid, Mark

game_state = GameState(Grid())
print(game_state.is_game_started)
print(game_state.is_game_over)
print(game_state.is_tie)
print(game_state.winner is None)
print(game_state.winning_cells)

game_state = GameState(Grid(cells="XOXOXOXXO"))
print(game_state.starting_mark)
print(game_state.current_mark)
print(game_state.is_game_started)
print(game_state.is_game_over)
print(game_state.is_tie)
print(game_state.winner)
print(game_state.winning_cells)

game_state = GameState(Grid(cells="XXOXOX  O"))
print(game_state.possible_moves)