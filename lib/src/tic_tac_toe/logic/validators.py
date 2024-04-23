# tic_tac_toe/logic/validators.py

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from tic_tac_toe.game.players import Player
  from tic_tac_toe.logic.models import GameState, Grid

from tic_tac_toe.logic.entities import Mark
from tic_tac_toe.logic.exceptions import InvalidGameStateError, InvalidMoveError

import re

def validate_starting_mark(mark: str) -> None:
  if mark not in [Mark.CROSS.value, Mark.NAUGHT.value]:
    raise ValueError(f"Error: Invalid mark. The starting mark must be either ` {Mark.CROSS.value} ` or ` {Mark.NAUGHT.value} `.")

def validate_game_board(game_board: Grid) -> None:
  if game_board.dimension < 3:
      raise ValueError("Error: Invalid game board dimension. The dimension of the game board must be 3 or greater.")
  if len(game_board.cells) != game_board.dimension ** 2:
    raise ValueError("Error: Invalid game board size. The size of the game board must be the square of the dimension.")
  if re.search(f"[^{Mark.CROSS.value}{Mark.NAUGHT.value}{Mark.EMPTY.value}]", game_board.cells) is not None:
    raise ValueError(f"Error: Invalid cell value. The value of each cell must be one of: `{Mark.CROSS.value}`, `{Mark.NAUGHT.value}`, `{Mark.EMPTY.value}`.")

def validate_game_state(game_state: GameState) -> None:
  validate_mark_counts(game_state.grid)
  validate_initial_player_mark(game_state.grid, game_state.initial_player_mark)
  validate_game_winner(game_state.grid, game_state.initial_player_mark, game_state.get_winner)

def validate_mark_counts(game_board: Grid) -> None:
  if not abs(game_board.cross_marks_count - game_board.naught_marks_count) in (0, 1):
    raise InvalidGameStateError(f"Error: Invalid number of marks. The difference between the number of ` {Mark.CROSS} ` marks and ` {Mark.NAUGHT} ` marks must be 0 or 1.")

def validate_initial_player_mark(game_board: Grid, initial_player_mark: Mark) -> None:
  if game_board.cross_marks_count > game_board.naught_marks_count and initial_player_mark != Mark.CROSS:
    raise InvalidGameStateError(f"Error: Invalid starting mark. The player with the ` {Mark.CROSS.value} ` mark must start the game.")
  if game_board.naught_marks_count > game_board.cross_marks_count and initial_player_mark != Mark.NAUGHT:
    raise InvalidGameStateError(f"Error: Invalid starting mark. The player with the ` {Mark.NAUGHT.value} ` mark must start the game.")

def validate_game_winner(game_board: Grid, initial_player_mark: Mark, game_winner: Mark | None) -> None:
  if game_winner == Mark.CROSS:
    validate_mark_count(game_board.cross_marks_count, game_board.naught_marks_count, initial_player_mark == Mark.CROSS)

  if game_winner == Mark.NAUGHT:
    validate_mark_count(game_board.naught_marks_count, game_board.cross_marks_count, initial_player_mark == Mark.NAUGHT)

def validate_mark_count(winner_mark_count: int, loser_mark_count: int, winner_mark_started: bool) -> None:
  if winner_mark_started and winner_mark_count <= loser_mark_count:
    raise InvalidGameStateError("Error: Invalid game state. The player who started the game must have at least as many marks as the other player.")
  if not winner_mark_started and winner_mark_count != loser_mark_count:
    raise InvalidGameStateError("Error: Invalid game state. If the player who started the game did not win, both players must have the same number of marks.")

def validate_player_move(game_state: GameState, position: int) -> None:
  if game_state.grid.is_position_filled(position):
    raise InvalidMoveError(f"Error: Invalid move. The cell at position {game_state.get_move_format_from_index(position)} is already filled.")
  if game_state.has_game_started and position not in game_state.get_valid_moves:
    raise InvalidMoveError(f"Error: Invalid move. The cell at position {game_state.get_move_format_from_index(position)} is not adjacent to an existing mark.")

def validate_players(players: list[Player]) -> None:
  validate_player_counts(players)
  validate_player_marks(players[0], players[1])

def validate_player_counts(players: list[Player]) -> None:
  if len(players) != 2:
    raise ValueError("Error: Invalid number of players. The game must have exactly two players.")

def validate_player_marks(player1: Player, player2: Player) -> None:
  validate_player_mark(player1)
  validate_player_mark(player2)
  if player1.mark is player2.mark:
    raise ValueError("Error: Both players have chosen the same mark. Each player must choose a unique mark.")

def validate_player_mark(player: Player) -> None:
  if player.mark not in [Mark.CROSS, Mark.NAUGHT]:
    raise ValueError(f"Error: Invalid player mark. The player's mark must be either ` {Mark.CROSS.value} ` or ` {Mark.NAUGHT.value} `.")

def validate_move_format(move: str, grid_dimension: int) -> None:
  if len(move) != 2 or not re.match(r"^[A-{}][1-{}]$".format(chr(64 + grid_dimension), grid_dimension), move):
    raise ValueError("Error: Invalid move. Please enter a move in the format 'A1'.")