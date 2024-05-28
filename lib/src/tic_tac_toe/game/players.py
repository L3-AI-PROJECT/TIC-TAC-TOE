# tic_tac_toe/game/players.py 

import abc
import time
import random

from tic_tac_toe.logic.entities import Mark
from tic_tac_toe.logic.exceptions import InvalidMoveError
from tic_tac_toe.logic.algorithms import find_best_move_minimax, find_best_move_alpha_beta
from tic_tac_toe.logic.models import GameState, Move

class Player(metaclass=abc.ABCMeta):
  """
  Abstract base class for a player in the game of Tic Tac Toe.
  
  Attributes:
  mark (Mark): The mark of the player (X or O).
  """
  
  def __init__(self, mark: Mark) -> None:
    """
    Initializes a Player with a mark.
    
    Parameters:
    mark (Mark): The mark of the player (X or O).
    """
    self.mark = mark
  
  def make_move(self, game_state: GameState) -> GameState:
    """
    Makes a move in the game.
    
    Parameters:
    game_state (GameState): The current state of the game.
    
    Returns:
    GameState: The state of the game after the move.
    """
    if self.mark is game_state.get_current_player_mark:
      if move:= self.get_move(game_state):
        return move.next_state
      raise InvalidMoveError("Info: No more moves available.")
    else:
      raise InvalidMoveError(f"It's not player ` {self.mark} `'s turn.")
  
  @abc.abstractmethod
  def get_move(self, game_state: GameState) -> Move | None:
    """
    Abstract method to get a move from the player.
    
    Parameters:
    game_state (GameState): The current state of the game.
    
    Returns:
    Move | None: The move chosen by the player, or None if no move is available.
    """
    pass

class ComputerPlayer(Player, metaclass=abc.ABCMeta):
  """
  Abstract base class for a computer player in the game of Tic Tac Toe.
  
  Attributes:
  mark (Mark): The mark of the player (X or O).
  delay (float): The delay before the computer player makes a move.
  """
  def __init__(self, mark: Mark, delay: float = 1.5) -> None:
    super().__init__(mark)
    self.delay = delay

  def get_move(self, game_state: GameState) -> Move | None:
    time.sleep(self.delay)
    return self.get_computer_move(game_state)

  @abc.abstractmethod
  def get_computer_move(self, game_state: GameState) -> Move | None:
    """
    Abstract method to get a move from the computer player.
    
    Parameters:
    game_state (GameState): The current state of the game.
    
    Returns:
    Move | None: The move chosen by the computer player, or None if no move is available.
    """
    pass

class RandomComputerPlayer(ComputerPlayer):
  """
  A computer player that chooses moves randomly.
  
  Attributes:
  mark (Mark): The mark of the player (X or O).
  """
  def __init__(self, mark: Mark) -> None:
    super().__init__(mark)

  def get_computer_move(self, game_state: GameState) -> Move | None:
    return game_state.make_random_move()

class MinimaxComputerPlayer(ComputerPlayer):
  """
  A computer player that uses the Minimax algorithm to choose moves.
  
  Attributes:
  mark (Mark): The mark of the player (X or O).
  """
  def __init__(self, mark: Mark) -> None:
    super().__init__(mark)

  def get_computer_move(self, game_state: GameState) -> Move | None:
    """
    Gets a move from the computer player using the Minimax algorithm.
    
    Parameters:
    game_state (GameState): The current state of the game.
    
    Returns:
    Move | None: The move chosen by the Minimax algorithm, or None if no move is available.
    """
    if game_state.has_game_started:
      depth = 1 if game_state.grid.dimension > 4 else 3
      return find_best_move_minimax(game_state, depth)
    return game_state.make_random_move()

class AlphaBetaComputerPlayer(ComputerPlayer):
  """
  A computer player that uses the Alpha-Beta pruning algorithm to choose moves.
  
  Attributes:
  mark (Mark): The mark of the player (X or O).
  """
  def __init__(self, mark: Mark) -> None:
    super().__init__(mark)
  
  def get_computer_move(self, game_state: GameState) -> Move | None:
    """
    Gets a move from the computer player using the Alpha-Beta pruning algorithm.
    
    Parameters:
    game_state (GameState): The current state of the game.
    
    Returns:
    Move | None: The move chosen by the Alpha-Beta pruning algorithm, or None if no move is available.
    """
    if game_state.has_game_started:
      depth = 1 if game_state.grid.dimension > 5 else 3
      return find_best_move_alpha_beta(game_state, depth)
    return game_state.make_random_move()