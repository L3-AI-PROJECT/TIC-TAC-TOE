# tic_tac_toe/logic/models.py
from __future__ import annotations

import re
from enum import Enum
from dataclasses import dataclass
from functools import cached_property

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
  dimension: int

  def __post_init__(self):
    if self.dimension < 3:
      raise ValueError("Dimension must be >=3")
    if len(self.cells) != self.dimension * self.dimension or any(c not in Mark for c in self.cells):
      raise ValueError("Invalid grid")
    
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
  previous_state: "GameState"
  next_state: "GameState"