# frontend/console/renderers.py

import math
import textwrap
from typing import Iterable

from tic_tac_toe.game.renderer import Renderer
from tic_tac_toe.logic.entities import Mark
from tic_tac_toe.logic.models import GameState

class ConsoleRenderer(Renderer):
  def render(self, game_state: GameState) -> None:
    clear_screen()
    if game_state.has_game_started:
        print(f"Player ` {game_state.get_current_player_mark.other.value} ` has chosen to play in position {game_state.get_last_move}.")
    if game_state.get_winner:
      print_blinking(game_state.grid.cells, game_state.get_winning_sequence)
      print(f"{game_state.get_winner.value} wins! \N{party popper}")
    else:
      print_solid(game_state.grid.cells)
      if game_state.is_draw:
        print("It's a tie! \N{neutral face}")


def clear_screen() -> None:
  print("\033c", end="")

def blink(text: str) -> str:
  return f"\033[33;5m{text}\033[0m"

def print_blinking(cells: Iterable[str], positions: Iterable[int]) -> None:
    mutable_cells = list(cells)
    for position in positions:
        mutable_cells[position] = blink(mutable_cells[position])
    print_solid(mutable_cells)

def print_solid(cells: Iterable[str]) -> None:
  n = int(math.sqrt(len(cells)))
  cells = iter(cells)
  max_width = len(str(n))
  print(textwrap.dedent(
f"""
{" " * (max_width + 4) + "   ".join(chr(i + 65).rjust(max_width - 1) for i in range(n))}
{" " * (max_width + 2) + "----" * n}
{"".join(f"{i+1}".rjust(max_width) + " ┆  " + " | ".join(color_cell(next(cells)) for _ in range(n)) + "\n" + " " * (max_width + 1) + "┆ " + "───┼" * (n-1) + "───\n" for i in range(n))}
"""
  ))

def color_cell(cell: str) -> str:
  if cell == Mark.CROSS:
    return '\033[34m' + cell + '\033[0m'  # Blue
  elif cell == Mark.NAUGHT:
    return '\033[31m' + cell + '\033[0m'  # Red
  else:
    return cell

