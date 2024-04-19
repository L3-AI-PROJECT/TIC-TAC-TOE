# tic_tac_toe/logic/validators.py

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from tic_tac_toe.logic.models import GameState, Grid

from tic_tac_toe.logic.mark import Mark
from tic_tac_toe.logic.exceptions import InvalidGameStateError, InvalidMoveError

import re

def validate_grid(grid: Grid) -> None:
  if grid.dimension < 3:
      raise ValueError("Dimension must be >=3")
  if len(grid.cells) != grid.dimension ** 2:
    raise ValueError(f"Invalid grid size: grid size must be {grid.dimension ** 2}")
  if re.search(f"[^{Mark.CROSS.value}{Mark.NAUGHT.value}{Mark.EMPTY.value}]", grid.cells) is not None:
    raise ValueError(f"Invalid cell value: cell value must be one of: {Mark.CROSS.value}, {Mark.NAUGHT.value}, {Mark.EMPTY.value}")

def validate_game_state(game_state: GameState) -> None:
  validate_number_of_marks(game_state.grid)
  validate_starting_mark(game_state.grid, game_state.starting_mark)
  validate_winner(game_state.grid, game_state.starting_mark, game_state.winner)

def validate_number_of_marks(grid: Grid) -> None:
  if not abs(grid.x_count - grid.o_count) in (0, 1):
    raise InvalidGameStateError(f"Invalid number of marks: difference between number of {Mark.CROSS} and {Mark.NAUGHT} must be 0 or 1")

def validate_starting_mark(grid: Grid, starting_mark: Mark) -> None:
  if grid.x_count > grid.o_count and starting_mark != Mark.CROSS:
    raise InvalidGameStateError(f"Invalid starting mark: starting mark must be {Mark.CROSS}")
  if grid.o_count > grid.x_count and starting_mark != Mark.NAUGHT:
    raise InvalidGameStateError(f"Invalid starting mark: starting mark must be {Mark.NAUGHT}")

def validate_winner(grid: Grid, starting_mark: Mark, winner: Mark | None) -> None:
  if winner == Mark.CROSS:
    validate_mark_count(grid.x_count, grid.o_count, starting_mark == Mark.CROSS)

  if winner == Mark.NAUGHT:
    validate_mark_count(grid.o_count, grid.x_count, starting_mark == Mark.NAUGHT)

def validate_mark_count(winner_count: int, loser_count: int, started: bool) -> None:
  if started and winner_count <= loser_count:
    raise InvalidGameStateError("Invalid winner: wrong number of marks")
  if not started and winner_count != loser_count:
    raise InvalidGameStateError("Invalid winner: wrong number of marks")

def validate_move(game_state: GameState, index: int) -> None:
  if game_state.grid.cells[index] != Mark.EMPTY:
    raise InvalidMoveError(f"Invalid move: cell[{index}] is not empty")
  # if index not in game_state.possible_moves:
  #   raise InvalidMoveError(f"Invalid move: cell[{index}] is not neighbor of an existing mark")






