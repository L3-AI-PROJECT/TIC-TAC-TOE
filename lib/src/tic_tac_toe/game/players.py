# tic_tac_toe/game/players.py 

import abc
import time
import random

from tic_tac_toe.logic.mark import Mark
from tic_tac_toe.logic.exceptions import InvalidMoveError
from tic_tac_toe.logic.models import GameState, Move

class Player(metaclass=abc.ABCMeta):
  def __init__(self, mark: Mark) -> None:
    self.mark = mark
  
  def make_move(self, game_state: GameState) -> GameState:
    if self.mark is game_state.current_mark:
      if move:= self.get_move(game_state):
        return move.next_state
      raise InvalidMoveError("No more moves available")
    else:
      raise InvalidMoveError("It's not your turn")
        
  def get_move(self, game_state: GameState) -> Move | None:
    pass

class ComputerPlayer(Player, metaclass=abc.ABCMeta):
  def __init__(self, mark: Mark, delay: float = 0.25) -> None:
    super().__init__(mark)
    self.delay = delay

  def get_move(self, game_state: GameState) -> Move | None:
    time.sleep(self.delay)
    # return self.find_best_move(game_state)
    return self.get_move(game_state)

  @abc.abstractmethod
  def get_move(self, game_state: GameState) -> Move | None:
    pass

class RandomComputerPlayer(ComputerPlayer):
  def get_move(self, game_state: GameState) -> Move | None:
    try:
      return random.choice(game_state.possible_moves)
    except IndexError:
      return None

