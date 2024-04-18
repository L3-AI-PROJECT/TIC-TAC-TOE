# tic_tac_toe/logic/models.py
from __future__ import annotations

from enum import Enum
from dataclasses import dataclass
from functools import cached_property

from tic_tac_toe.logic.validators import validate_game_state, validate_grid

class Mark(str, Enum):
  CROSS = "X"
  NAUGHT = "O"
  EMPTY = " "

  @property
  def other(self) -> Mark:
    switch = {
      Mark.CROSS: Mark.NAUGHT,
      Mark.NAUGHT: Mark.CROSS,
      Mark.EMPTY: Mark.EMPTY
    }
    return switch[self]
  
@dataclass(frozen=True)
class Grid:
  cells: str
  dimension: int = 3

  def __post_init__(self):
    validate_grid(self)
    
  @cached_property
  def x_count(self) -> int:
    return self.cells.count(Mark.CROSS.value)
  
  @cached_property
  def o_count(self) -> int:
    return self.cells.count(Mark.NAUGHT.value)
  
  @cached_property
  def empty_count(self) -> int:
    return self.cells.count(Mark.EMPTY.value)
  
@dataclass(frozen=True)
class Move:
  mark: Mark
  cell_index: int
  previous_state: GameState
  next_state: GameState

@dataclass(frozen=True)
class GameState:
  grid: Grid
  starting_mark: Mark = Mark.CROSS

  def __post_init__(self):
    validate_game_state(self)

  @cached_property
  def current_mark(self) -> Mark:
    return self.starting_mark if self.grid.x_count is self.grid.o_count else self.starting_mark.other
  
  @cached_property
  def is_game_started(self) -> bool:
    return not self.grid.empty_count == self.grid.dimension ** 2
  
  @cached_property
  def is_game_over(self) -> bool:
    return self.is_game_started and (self.is_winner or self.is_tie)
  
  @cached_property
  def is_winner(self) -> bool:
    return any(self._is_winner(i) for i in range(self.grid.dimension))
  
  @cached_property
  def is_tie(self) -> bool:
    return not self.is_winner and self.grid.empty_count == 0

  @cached_property
  def winner(self) -> Mark | None:
    return None

  @cached_property
  def winning_cells(self) -> list[int]:
    return []

