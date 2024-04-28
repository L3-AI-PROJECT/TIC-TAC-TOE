# tic_tac_toe/game/players.py 

import abc
import time

from tic_tac_toe.logic.entities import Mark
from tic_tac_toe.logic.exceptions import InvalidMoveError
from tic_tac_toe.logic.algorithms import find_best_move_minimax
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
    return self.get_computer_move(game_state)

  @abc.abstractmethod
  def get_computer_move(self, game_state: GameState) -> Move | None:
    pass

class RandomComputerPlayer(ComputerPlayer):
  def get_computer_move(self, game_state: GameState) -> Move | None:
    return game_state.make_random_move()

class MinimaxComputerPlayer(ComputerPlayer):
  def get_computer_move(self, game_state: GameState) -> Move | None:
    if game_state.has_game_started:
      return find_best_move_minimax(
        game_state, 
        depth=1, 
        choose_higher_score=False,
        evaluate_score=self.evaluate_score
        )
    return game_state.make_random_move()
  
  def evaluate_score(self, min_score: int, max_score: int) -> int:
    if abs(min_score) > abs(max_score):
      return min_score 
    else:
      return max_score 
  
# class AlphaBetaComputerPlayer(ComputerPlayer):
#   def __init__(self, mark: Mark, delay: float = 0) -> None:
#     super().__init__(mark, delay)
  
#   def get_computer_move(self, game_state: GameState) -> Move | None:
#     if game_state.has_game_started:
#       return find_best_move_alpha_beta(game_state, max_depth=10)
#     return game_state.make_random_move()
