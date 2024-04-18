# tic_tac_toe/logic/validators.py

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from tic_tac_toe.logic.models import GameState, Grid, Mark

import re

from tic_tac_toe.logic.exceptions import InvalidGameStateError

def validate_grid(grid: Grid) -> None:
  if not isinstance(grid, Grid):
    raise ValueError("Invalid grid: grid must be an instance of Grid")
  if grid.dimension < 3:
      raise ValueError("Dimension must be >=3")
  if not len(grid.cells) == grid.dimension ** 2:
    raise ValueError(f"Invalid grid size: grid size must be {grid.dimension ** 2}")
  if re.search(r"[^XO ]", grid.cells) is not None:
    raise ValueError(f"Invalid cell value: cell value must be one of: {Mark.__members__.keys()}")
  

def validate_game_state(game_state: GameState) -> None:
  if not isinstance(game_state, GameState):
    raise ValueError("Invalid game state: game state must be an instance of GameState")
  validate_number_of_marks(game_state.grid)
  validate_starting_mark(game_state.grid, game_state.starting_mark)
  validate_winner(game_state.grid, game_state.starting_mark, game_state.winner)

def validate_number_of_marks(grid: Grid) -> None:
  if abs(grid.x_count - grid.o_count) in (0, 1):
    raise InvalidGameStateError("Invalid number of marks: difference between number of X and O must be 0 or 1")

def validate_starting_mark(grid: Grid, starting_mark: Mark) -> None:
  if grid.x_count > grid.o_count and not starting_mark == Mark.CROSS:
    raise InvalidGameStateError(f"Invalid starting mark: starting mark must be {Mark.CROSS}")
  if grid.o_count > grid.x_count and not starting_mark == Mark.NAUGHT:
    raise InvalidGameStateError(f"Invalid starting mark: starting mark must be {Mark.NAUGHT}")
  
def validate_winner(grid: Grid, starting_mark: Mark, winner: Mark | None) -> None:
  if winner is None and grid.x_count + grid.o_count < grid.dimension ** 2:
    raise InvalidGameStateError("Invalid winner: game is not finished")

  if winner is Mark.CROSS:
    validate_mark_count(grid.x_count, grid.o_count, starting_mark is Mark.CROSS)

  if winner is Mark.NOUGHT:
    validate_mark_count(grid.o_count, grid.x_count, starting_mark is Mark.NOUGHT)

def validate_mark_count(winner_count: int, loser_count: int, started: bool) -> None:
  if started and winner_count <= loser_count:
    raise InvalidGameStateError("Invalid winner: wrong number of marks")
  if not started and winner_count != loser_count:
    raise InvalidGameStateError("Invalid winner: wrong number of marks")






