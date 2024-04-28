# tic_tac_toe/logic/algorithms.py

from functools import partial

import random

from tic_tac_toe.logic.entities import Mark
from tic_tac_toe.logic.models import Move, GameState

import random
from typing import Callable

def find_best_move_minimax(game_state: GameState, depth: int, choose_higher_score: bool = True) -> Move:
  moves = [game_state.make_move_to(position) for position in game_state.get_valid_moves]
  scores = [minimax(move, game_state.get_current_player_mark, depth, choose_higher_score) for move in moves]

  # Find the maximum score
  max_score = max(scores) if choose_higher_score else min(scores)

  # Find all moves with the maximum score
  best_moves = [move for move, score in zip(moves, scores) if score == max_score]

  # Randomly select one of the best moves
  return random.choice(best_moves)

def minimax(move: Move, maximizer: Mark, depth: int = None, choose_higher_score: bool = False) -> int:
  if move.next_state.has_game_ended or depth == 0:
    return evaluate_score(move.next_state, maximizer, heuristic=depth is not None)

  moves = [move.next_state.make_move_to(position) for position in move.next_state.get_valid_moves]
  scores = [minimax(next_move, maximizer, depth - 1, not choose_higher_score) for next_move in moves]

  return max(scores) if choose_higher_score else min(scores)

def evaluate_score(game_state: GameState, maximizer: Mark, heuristic: bool) -> int:
  if game_state.get_winner is maximizer:
    return 10
  if game_state.is_draw:
    return 0
  if game_state.get_winner is not None:
    return -10
  if heuristic:
    return heuristic_score(game_state, maximizer)
  else:
    return 0

def heuristic_score(game_state: GameState, maximizer: Mark) -> int:
  max_score = 0
  required_mark = game_state.required_marks_for_win
  for row in game_state.row_sequences:
    max_score = max(max_score, evaluate_line(row, maximizer, required_mark))
  for column in game_state.column_sequences:
    max_score = max(max_score, evaluate_line(column, maximizer, required_mark))
  for diagonal in game_state.diagonal_sequences:
    max_score = max(max_score, evaluate_line(diagonal, maximizer, required_mark))
  return max_score

def evaluate_line(line: str, maximizer: Mark, required_mark: int) -> int:
  minimizer = maximizer.other
  segments = line.split(minimizer)
  max_score = 0
  for i, segment in enumerate(segments):
    # Skip dead segments and empty segments
    if segment == "" or (i > 0 and i < len(segments) - 1 and len(segment) < required_mark):
      continue
    max_score = max(max_score, segment.count(maximizer))
  return max_score
