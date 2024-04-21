# tic_tac_toe/game/engine.py

from dataclasses import dataclass
from typing import Callable, TypeAlias

from tic_tac_toe.game.players import Player
from tic_tac_toe.game.renderer import Renderer
from tic_tac_toe.logic.mark import Mark
from tic_tac_toe.logic.exceptions import InvalidMoveError
from tic_tac_toe.logic.models import GameState, Grid
from tic_tac_toe.logic.validators import validate_player

ErrorHandler: TypeAlias = Callable[[Exception], None]

@dataclass(frozen=True)
class TicTacToe:
  player1: Player
  player2: Player
  renderer: Renderer
  error_handler: ErrorHandler | None = None

  def __post_init__(self):
    validate_player(self.player1, self.player2)

  def play(self, starting_mark: Mark = Mark.CROSS) -> None:
    game_state = GameState(Grid(3), starting_mark)
    while True:
      self.renderer.render(game_state)
      if game_state.is_game_over:
        break
      player = self.get_current_player(game_state)
      try:
        game_state = player.make_move(game_state)
      except InvalidMoveError as e:
        if self.error_handler:
          self.error_handler(e)
  
  def get_current_player(self, game_state: GameState) -> Player:
    return self.player1 if game_state.current_mark is self.player1.mark else self.player2

