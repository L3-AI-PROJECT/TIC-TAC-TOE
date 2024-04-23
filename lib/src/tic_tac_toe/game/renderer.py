# tic_tac_toe/game/renderer.py

import abc

from tic_tac_toe.logic.models import GameState

class Renderer(metaclass=abc.ABCMeta):
  @abc.abstractmethod
  def render(self, game_state: GameState) -> None:
    pass
