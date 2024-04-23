# frontend/console/cli.py

from tic_tac_toe.game.engine import TicTacToe

from .args import parse_args
from .renderers import ConsoleRenderer

def main() -> None:
  player1, player2, starting_mark, required_marks_for_win, dimension = parse_args()
  TicTacToe(player1, player2, ConsoleRenderer()).play(starting_mark, dimension, required_marks_for_win)
