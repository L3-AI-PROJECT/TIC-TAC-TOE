# frontend/console/args.py

import argparse
from typing import NamedTuple

from tic_tac_toe.game.players import Player, RandomComputerPlayer, MinimaxComputerPlayer, AlphaBetaComputerPlayer
from tic_tac_toe.logic.entities import Mark

from .players import ConsolePlayer

PLAYER_CLASSES = {
  "human": ConsolePlayer,
  "random": RandomComputerPlayer,
  "minimax": MinimaxComputerPlayer,
  "alpha_beta": AlphaBetaComputerPlayer,
}

class Args(NamedTuple):
  player_x: Player
  player_o: Player
  starting_mark: str
  required_marks_for_win: int
  dimension: int

def create_player(player_type: str, mark: Mark) -> Player:
  return PLAYER_CLASSES[player_type](mark)

def parse_args() -> Args:
  parser = argparse.ArgumentParser()
  parser.add_argument(
    "-X", 
    dest="player_x",
    choices=PLAYER_CLASSES.keys(),
    default="human",
  )
  parser.add_argument(
    "-O",
    dest="player_o",
    choices=PLAYER_CLASSES.keys(),
    default="random",
  )
  parser.add_argument(
    "--starting",
    dest="starting_mark",
    type=str,
    default=Mark.CROSS.value,
  )
  parser.add_argument(
    "--required",
    dest="required_marks_for_win",
    type=int,
    default=3,
  )
  parser.add_argument(
    "--dimension",
    dest="dimension",
    type=int,
    default=3,
  )
  args = parser.parse_args()

  player1 = create_player(args.player_x, Mark.CROSS)
  player2 = create_player(args.player_o, Mark.NAUGHT)

  if args.starting_mark == Mark.NAUGHT:
    player1, player2 = player2, player1
  
  return Args(player1, player2, args.starting_mark, args.required_marks_for_win, args.dimension)