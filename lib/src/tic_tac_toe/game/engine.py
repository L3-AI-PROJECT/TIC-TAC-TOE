# tic_tac_toe/game/engine.py

from dataclasses import dataclass
from typing import Callable, TypeAlias

from tic_tac_toe.game.players import Player
from tic_tac_toe.game.renderer import Renderer
from tic_tac_toe.logic.entities import Mark
from tic_tac_toe.logic.exceptions import InvalidMoveError
from tic_tac_toe.logic.models import GameState, Grid
from tic_tac_toe.logic.validators import validate_players, validate_starting_mark

ErrorHandler: TypeAlias = Callable[[Exception], None]

def default_error_handler(e: Exception):
    print(f"\nAn error occurred:\n{str(e)}")

@dataclass(frozen=True)
class TicTacToe:
  player1: Player
  player2: Player
  renderer: Renderer
  error_handler: ErrorHandler | None = default_error_handler

  def __post_init__(self):
    validate_players([self.player1, self.player2])
  
  def play(self, starting_mark: str, dimension: int, required_marks_for_win: int) -> None:
    try:
      validate_starting_mark(starting_mark)
      game_state = GameState(Grid(dimension), Mark(starting_mark), required_marks_for_win)
      while True:
        self.renderer.render(game_state)
        if game_state.has_game_ended:
          break
        player = self.get_current_player(game_state)
        game_state = player.make_move(game_state)
    except KeyboardInterrupt as _:
      self.error_handler(Exception("Error: The game was interrupted by the user."))
    except Exception as e:
      self.error_handler(e)
  
  def get_current_player(self, game_state: GameState) -> Player:
    return self.player1 if game_state.get_current_player_mark is self.player1.mark else self.player2

