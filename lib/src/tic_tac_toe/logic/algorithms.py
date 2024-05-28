# tic_tac_toe/logic/algorithms.py

from concurrent.futures import ThreadPoolExecutor
import random
import os
# import logging


from tic_tac_toe.logic.entities import Mark
from tic_tac_toe.logic.models import Move, GameState

num_cpus = os.cpu_count()

# # logging.basicConfig(level=logging.INFO)
def find_best_move_alpha_beta(game_state: GameState, depth: int, choose_higher_score: bool = True, memo: dict = {}) -> Move:
  """
  This function uses the Alpha-Beta pruning algorithm to find the best move in a game of Tic Tac Toe.
  
  Parameters:
  game_state (GameState): The current state of the game.
  depth (int): The maximum depth to search in the game tree.
  choose_higher_score (bool): If True, the function will choose the move with the highest score. If False, it will choose the move with the lowest score.
  memo (dict): A dictionary used for memoization to store the results of previously computed states.
  
  Returns:
  Move: The best move found.
  """
  # logging.info('Starting find_best_move_alpha_beta')
  
  moves = game_state.get_valid_moves
  
  if not moves:
    # logging.error('No valid moves available')
    return None
  
  with ThreadPoolExecutor(max_workers=num_cpus) as executor:
    scores = list(executor.map(lambda move: alpha_beta_pruning(move, game_state.get_current_player_mark, depth, -float('inf'), float('inf'), choose_higher_score, memo), moves))
    # scores = [alpha_beta_pruning(move, game_state.get_current_player_mark, depth, -float('inf'), float('inf'), choose_higher_score) for move in moves]

  # Find the maximum score
  max_score = max(scores) if choose_higher_score else min(scores)

  # Find all moves with the maximum score
  best_moves = [move for move, score in zip(moves, scores) if score == max_score]

  # Prioritize moves that could lead to a win in the next turn
  for move in best_moves:
    if move.next_state.get_winner is game_state.get_current_player_mark:
      return move

  # If no such move exists, prioritize moves that block the opponent from winning in their next turn
  for move in best_moves:
    if any(next_move.next_state.get_winner is not game_state.get_current_player_mark for next_move in move.next_state.get_valid_moves):
      return move

  # If no such move exists, randomly select one of the best moves
  chosen_move = random.choice(best_moves)

  # logging.info(f'Chosen move: {chosen_move}')
  # logging.info('Ending find_best_move_alpha_beta')
  return chosen_move

def find_best_move_minimax(game_state: GameState, depth: int, choose_higher_score: bool = True, memo: dict = {}) -> Move:
  """
  This function uses the Minimax algorithm to find the best move in a game of Tic Tac Toe.
  
  Parameters:
  game_state (GameState): The current state of the game.
  depth (int): The maximum depth to search in the game tree.
  choose_higher_score (bool): If True, the function will choose the move with the highest score. If False, it will choose the move with the lowest score.
  memo (dict): A dictionary used for memoization to store the results of previously computed states.
  
  Returns:
  Move: The best move found.
  """
  
  # logging.info('Starting find_best_move_minimax')
  
  moves = game_state.get_valid_moves

  if not moves:
    # logging.error('No valid moves available')
    return None
  
  with ThreadPoolExecutor(max_workers=num_cpus) as executor:
    scores = list(executor.map(lambda move: minimax(move, game_state.get_current_player_mark, depth, choose_higher_score, memo), moves))
    # scores = [minimax(move, game_state.get_current_player_mark, depth, choose_higher_score) for move in moves]

  # Find the maximum score
  max_score = max(scores) if choose_higher_score else min(scores)

  # Find all moves with the maximum score
  best_moves = [move for move, score in zip(moves, scores) if score == max_score]

  # Prioritize moves that could lead to a win in the next turn
  for move in best_moves:
    if move.next_state.get_winner is game_state.get_current_player_mark:
      return move

  # If no such move exists, prioritize moves that block the opponent from winning in their next turn
  for move in best_moves:
    if any(next_move.next_state.get_winner is not game_state.get_current_player_mark for next_move in move.next_state.get_valid_moves):
      return move

  # If no such move exists, randomly select one of the best moves
  chosen_move = random.choice(best_moves)
  
  # logging.info(f'Chosen move: {chosen_move}')
  # logging.info('Ending find_best_move_minimax')
  return chosen_move

def alpha_beta_pruning(move: Move, maximizer: Mark, depth: int = None, alpha: int = -float('inf'), beta: int = float('inf'), choose_higher_score: bool = False, memo: dict = {}) -> int:
  """
  This function implements the Alpha-Beta pruning algorithm, which is an optimization of the Minimax algorithm.
  
  Parameters:
  move (Move): The move to evaluate.
  maximizer (Mark): The player who is maximizing their score.
  depth (int): The maximum depth to search in the game tree.
  alpha (int): The best value that the maximizer currently can guarantee at that level or above.
  beta (int): The best value that the minimizer currently can guarantee at that level or above.
  choose_higher_score (bool): If True, the function will choose the move with the highest score. If False, it will choose the move with the lowest score.
  memo (dict): A dictionary used for memoization to store the results of previously computed states.
  
  Returns:
  int: The score of the move.
  """  
  
  # logging.info(f'Starting alpha_beta_pruning - Move: {move_format} - Depth: {depth} - Choose higher score: {choose_higher_score}')
  
  # Convert the game state to a hashable format that can be used as a dictionary key
  state_key = str(move.next_state)
  
  # If the result of this state has been computed before, return the stored result
  if state_key in memo:
    return memo[state_key]
  
  
  if move.next_state.has_game_ended or depth == 0:
    return evaluate_score(move.next_state, maximizer, heuristic=depth is not None)

  max_eval = -float('inf')
  min_eval = float('inf')

  if choose_higher_score:
    for child_move in move.next_state.get_valid_moves:
      eval = alpha_beta_pruning(child_move, maximizer, depth - 1, alpha, beta, not choose_higher_score)
      max_eval = max(max_eval, eval)
      alpha = max(alpha, eval)
      if beta <= alpha:
        break
  else:
    for child_move in move.next_state.get_valid_moves:
      eval = alpha_beta_pruning(child_move, maximizer, depth - 1, alpha, beta, not choose_higher_score)
      min_eval = min(min_eval, eval)
      beta = min(beta, eval)
      if beta <= alpha:
        break
  
  # logging.info(f'Returning score: {max_eval if choose_higher_score else min_eval}')
  # logging.info('Ending alpha_beta_pruning')

  # Store the result in the memo dictionary before returning it
  result = max_eval if choose_higher_score else min_eval
  memo[state_key] = result
  return result

def minimax(move: Move, maximizer: Mark, depth: int = None, choose_higher_score: bool = False, memo: dict = {}) -> int:
  """
  This function implements the Minimax algorithm, which is a decision-making algorithm for finding the best move in a game of Tic Tac Toe.
  
  Parameters:
  move (Move): The move to evaluate.
  maximizer (Mark): The player who is maximizing their score.
  depth (int): The maximum depth to search in the game tree.
  choose_higher_score (bool): If True, the function will choose the move with the highest score. If False, it will choose the move with the lowest score.
  memo (dict): A dictionary used for memoization to store the results of previously computed states.
  
  Returns:
  int: The score of the move.
  """
  
  # logging.info(f'Starting minimax - Move: {move_format} - Depth: {depth} - Choose higher score: {choose_higher_score}')
  
  # Convert the game state to a hashable format that can be used as a dictionary key
  state_key = str(move.next_state)
  
  # If the result of this state has been computed before, return the stored result
  if state_key in memo:
    return memo[state_key]
  
  if move.next_state.has_game_ended or depth == 0:
    return evaluate_score(move.next_state, maximizer, heuristic=depth is not None)

  moves = move.next_state.get_valid_moves
  scores = [minimax(next_move, maximizer, depth - 1, not choose_higher_score) for next_move in moves]

  # logging.info(f'Returning score: {max(scores) if choose_higher_score else min(scores)}')
  # logging.info('Ending minimax')

  # Store the result in the memo dictionary before returning it
  result = max(scores) if choose_higher_score else min(scores)
  memo[state_key] = result
  return result


def evaluate_score(game_state: GameState, maximizer: Mark, heuristic: bool) -> int:
  """
  This function evaluates the score of a game state.
  
  Parameters:
  game_state (GameState): The state of the game to evaluate.
  maximizer (Mark): The player who is maximizing their score.
  heuristic (bool): If True, the function will use a heuristic to estimate the score. If False, it will calculate the exact score.
  
  Returns:
  int: The score of the game state.
  """
  
  # logging.info(f'Starting evaluate_score - Move: {game_state.get_move_format_from_index(game_state.last_move_position)}')
  score = 0
  if game_state.get_winner is maximizer:
    score = 1000
  elif game_state.is_draw:
    score = 0
  elif game_state.get_winner is not None:
    score = -1000
  elif heuristic:
    score = heuristic_score(game_state, maximizer)
  # logging.info(f'Returning score: {score} - Move: {game_state.get_move_format_from_index(game_state.last_move_position)}')
  # logging.info('Ending evaluate_score')
  return score

def heuristic_score(game_state: GameState, maximizer: Mark) -> int:
  """
  This function calculates a heuristic score for a game state.
  
  Parameters:
  game_state (GameState): The state of the game to evaluate.
  maximizer (Mark): The player who is maximizing their score.
  
  Returns:
  int: The heuristic score of the game state.
  """
  max_score = 0
  min_score = 0
  potential_moves_score = 0
  required_mark = game_state.required_marks_for_win

  for sequence in game_state.generate_sequences:
    max_score += evaluate_line(sequence, maximizer, required_mark)
    min_score += evaluate_line(sequence, maximizer.other, required_mark)
    # potential_moves_score += evaluate_potential_moves(sequence, maximizer)

  return max_score - min_score + potential_moves_score

def evaluate_potential_moves(line: str, maximizer: Mark) -> int:
  """
  This function evaluates the potential moves in a line of the game grid.
  
  Parameters:
  line (str): The line of the game grid to evaluate.
  maximizer (Mark): The player who is maximizing their score.
  
  Returns:
  int: The score of the potential moves.
  """
  
  score = 0
  for i in range(len(line)):
    # If the cell is empty and is adjacent to a cell of the player, add 1 to the score
    if line[i] == Mark.EMPTY.value and (i > 0 and line[i-1] == maximizer or i < len(line) - 1 and line[i+1] == maximizer):
      score += 1
  return score

def evaluate_line(line: str, maximizer: Mark, required_mark: int) -> int:
  """
  This function evaluates a line of the game grid.
  
  Parameters:
  line (str): The line of the game grid to evaluate.
  maximizer (Mark): The player who is maximizing their score.
  required_mark (int): The number of marks required for a win.
  
  Returns:
  int: The score of the line.
  """
  minimizer = maximizer.other
  segments = line.split(minimizer)
  max_score = 0
  for i, segment in enumerate(segments):
    # Skip dead segments and empty segments
    if segment == "" or (i > 0 and i < len(segments) - 1 and len(segment) < required_mark):
      continue
    max_score = max(max_score, segment.count(maximizer))
  return max_score
