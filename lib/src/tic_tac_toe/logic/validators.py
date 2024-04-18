# tic_tac_toe/logic/validators.py

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from tic_tac_toe.logic.models import GameState, Grid, Mark

import re

from tic_tac_toe.logic.exceptions import InvalidGameStateError, InvalidMoveError

def validate_grid(grid: Grid) -> None:
  if grid.dimension < 3:
      raise ValueError("Dimension must be >=3")
  if len(grid.cells) != grid.dimension ** 2:
    raise ValueError(f"Invalid grid size: grid size must be {grid.dimension ** 2}")
  if re.search(r"[^XO ]", grid.cells) is not None:
    raise ValueError(f"Invalid cell value: cell value must be one of: X, O, or empty space")
  

def validate_game_state(game_state: GameState) -> None:
  validate_number_of_marks(game_state.grid)
  validate_starting_mark(game_state.grid, game_state.starting_mark)
  validate_winner(game_state.grid, game_state.starting_mark, game_state.winner)

def validate_number_of_marks(grid: Grid) -> None:
  if not abs(grid.x_count - grid.o_count) in (0, 1):
    raise InvalidGameStateError("Invalid number of marks: difference between number of X and O must be 0 or 1")

def validate_starting_mark(grid: Grid, starting_mark: Mark) -> None:
  if grid.x_count > grid.o_count and starting_mark != "X":
    raise InvalidGameStateError(f"Invalid starting mark: starting mark must be X")
  if grid.o_count > grid.x_count and starting_mark != "O":
    raise InvalidGameStateError("Invalid starting mark: starting mark must be O")
  
def validate_winner(grid: Grid, starting_mark: Mark, winner: Mark | None) -> None:
  if winner == "X":
    validate_mark_count(grid.x_count, grid.o_count, starting_mark is Mark.CROSS)

  if winner == "O":
    validate_mark_count(grid.o_count, grid.x_count, starting_mark is Mark.NOUGHT)

def validate_mark_count(winner_count: int, loser_count: int, started: bool) -> None:
  if started and winner_count <= loser_count:
    raise InvalidGameStateError("Invalid winner: wrong number of marks")
  if not started and winner_count != loser_count:
    raise InvalidGameStateError("Invalid winner: wrong number of marks")
  
def validate_move(game_state: GameState, index: int) -> None:
  if game_state.grid.cells[index] != " ":
    raise InvalidMoveError("Invalid move: cell is not empty")






