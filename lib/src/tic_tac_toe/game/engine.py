# tic_tac_toe/game/engine.py

from dataclasses import dataclass
from typing import Callable, TypeAlias

from tic_tac_toe.game.players import Player
from tic_tac_toe.game.renderer import Renderer
from tic_tac_toe.logic.entities import Mark
from tic_tac_toe.logic.exceptions import InvalidMoveError
from tic_tac_toe.logic.models import GameState, Grid
from tic_tac_toe.logic.validators import validate_players

ErrorHandler: TypeAlias = Callable[[Exception], None]

@dataclass(frozen=True)
class TicTacToe:
  player1: Player
  player2: Player
  renderer: Renderer
  error_handler: ErrorHandler | None = None

  def __post_init__(self):
    validate_players([self.player1, self.player2])

  def play(self, starting_mark: Mark = Mark.CROSS, dimension: int = 3, winning_line_length: int = 3) -> None:
    game_state = GameState(Grid(dimension), starting_mark, winning_line_length)
    while True:
      self.renderer.render(game_state)
      if game_state.has_game_ended:
        break
      player = self.get_current_player(game_state)
      try:
        game_state = player.make_move(game_state)
      except InvalidMoveError as e:
        if self.error_handler:
          self.error_handler(e)
  
  def get_current_player(self, game_state: GameState) -> Player:
    return self.player1 if game_state.get_current_player_mark is self.player1.mark else self.player2

