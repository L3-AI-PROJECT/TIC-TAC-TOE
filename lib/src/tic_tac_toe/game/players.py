# tic_tac_toe/game/players.py 

import abc
import time
import random

from tic_tac_toe.logic.entities import Mark
from tic_tac_toe.logic.exceptions import InvalidMoveError
from tic_tac_toe.logic.models import GameState, Move

class Player(metaclass=abc.ABCMeta):
  def __init__(self, mark: Mark) -> None:
    self.mark = mark
  
  def make_move(self, game_state: GameState) -> GameState:
    if self.mark is game_state.get_current_player_mark:
      if move:= self.get_move(game_state):
        return move.next_state
      raise InvalidMoveError("Info: No more moves available.")
    else:
      raise InvalidMoveError(f"It's not player ` {self.mark} `'s turn.")
  
  def get_move(self, game_state: GameState) -> Move | None:
    pass

class ComputerPlayer(Player, metaclass=abc.ABCMeta):
  def __init__(self, mark: Mark, delay: float = 1.5) -> None:
    super().__init__(mark)
    self.delay = delay

  def get_move(self, game_state: GameState) -> Move | None:
    time.sleep(self.delay)
    # return self.find_best_move(game_state)
    return self.get_computer_move(game_state)

  @abc.abstractmethod
  def get_computer_move(self, game_state: GameState) -> Move | None:
    pass

class RandomComputerPlayer(ComputerPlayer):
  def get_computer_move(self, game_state: GameState) -> Move | None:
    try:
      if not game_state.has_game_started:
        return game_state.make_move_to(random.randint(0, game_state.grid.count - 1))
      return game_state.make_move_to(random.choice(game_state.get_valid_moves))
    except Exception:
      return None

