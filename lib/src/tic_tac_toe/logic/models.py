# tic_tac_toe/logic/models.py

from __future__ import annotations
from enum import Enum

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
  
