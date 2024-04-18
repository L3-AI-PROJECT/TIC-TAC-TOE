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
  cells: str = " " * 9

  def __post_init__(self) -> None:
    if not re.match(r"^[\sXO]{9}$", self.cells):
      raise ValueError("Must contain 9 cells with only X, O or space")
    
  @cached_property
  def x_count(self) -> int:
    return self.cells.count(Mark.CROSS.value)
  
  @cached_property
  def o_count(self) -> int:
    return self.cells.count(Mark.NAUGHT.value)
  
  @cached_property
  def empty_count(self) -> int:
    return self.cells.count(Mark.EMPTY.value)