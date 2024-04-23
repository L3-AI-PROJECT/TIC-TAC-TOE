# frontend/console/players.py

from tic_tac_toe.game.players import Player
from tic_tac_toe.logic.exceptions import InvalidMoveError
from tic_tac_toe.logic.validators import validate_move_format
from tic_tac_toe.logic.models import GameState, Move

class ConsolePlayer(Player):
  def get_move(self, game_state: GameState) -> Move | None:
    while not game_state.has_game_ended:
      try:
        position = get_position(game_state, input(f"Player `{self.mark.value}` enter your move: "))
        return game_state.make_move_to(position)
      except ValueError as error:
        print(error)
      except InvalidMoveError as error:
        print(error)

def get_position(game_state: GameState, move: str) -> int:
  validate_move_format(move, game_state.grid.dimension)
  return game_state.get_position_from_move_format(move)



