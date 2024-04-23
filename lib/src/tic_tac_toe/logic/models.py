# tic_tac_toe/logic/models.py

from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property

from tic_tac_toe.logic.entities import Mark
from tic_tac_toe.logic.validators import validate_game_state, validate_game_board, validate_player_move

@dataclass(frozen=True)
class LineGenerator:
  length: int
  dimension: int

  def generate_horizontal_lines(self, occupied_cells: list[int], column_numbers: list[int], row_numbers: list[int]) -> list[list[int]]:
    lines = []
    for i in range(len(occupied_cells)):
        if column_numbers[i] + self.length > self.dimension:
          continue
        line = []
        for k in range(i, len(occupied_cells)):
          if len(line) == self.length or column_numbers[k] - column_numbers[i] >= self.length:
            break
          if k < len(occupied_cells) and row_numbers[k] == row_numbers[i]:
            line.append(occupied_cells[k])
        if len(line) == self.length:
          lines.append(line)
    return lines

  def generate_vertical_lines(self, occupied_cells: list[int], column_numbers: list[int], row_numbers: list[int]) -> list[list[int]]:
    lines = []
    for i in range(len(occupied_cells)):
      if row_numbers[i] + self.length > self.dimension:
        break
      line = []
      for k in range(i, len(occupied_cells)):
        if len(line) == self.length or row_numbers[k] - row_numbers[i] >= self.length:
          break
        if k < len(occupied_cells) and column_numbers[k] == column_numbers[i]:
          line.append(occupied_cells[k])
      if len(line) == self.length:
        lines.append(line)
    return lines
  
  def generate_diagonal_lines_tl_br(self, occupied_cells: list[int], column_numbers: list[int], row_numbers: list[int]) -> list[list[int]]:
    lines = []
    for i in range(len(occupied_cells)):
      if column_numbers[i] + self.length > self.dimension:
        continue
      if row_numbers[i] + self.length > self.dimension:
        break
      line = []
      for k in range(i, len(occupied_cells)):
        if len(line) == self.length or row_numbers[k] - row_numbers[i] >= self.length:
          break
        if k < len(occupied_cells) and row_numbers[k] - row_numbers[i] == column_numbers[k] - column_numbers[i]:
          line.append(occupied_cells[k])
      if len(line) == self.length:
        lines.append(line)
    return lines
  
  def generate_diagonal_lines_tr_bl(self, occupied_cells: list[int], column_numbers: list[int], row_numbers: list[int]) -> list[list[int]]:
    lines = []
    for i in range(len(occupied_cells)):
      if column_numbers[i] - self.length < -1: 
        continue
      if row_numbers[i] + self.length > self.dimension:
        break
      line = []
      for k in range(i, len(occupied_cells)):
        if len(line) == self.length or row_numbers[k] - row_numbers[i] >= self.length:
          break
        if k < len(occupied_cells) and row_numbers[k] - row_numbers[i] == column_numbers[i] - column_numbers[k]:
          line.append(occupied_cells[k])
      if len(line) == self.length:
        lines.append(line)
    return lines

@dataclass(frozen=True)
class Grid:
  dimension: int = 3
  cells: str = None
  
  def __post_init__(self):
    if self.cells is None:
      object.__setattr__(self, "cells", Mark.EMPTY * self.dimension ** 2)
    validate_game_board(self)
  
  @cached_property
  def cross_marks_count(self) -> int:
    return self.cells.count(Mark.CROSS.value)
  
  @cached_property
  def naught_marks_count(self) -> int:
    return self.cells.count(Mark.NAUGHT.value)
  
  @cached_property
  def empty_cells_count(self) -> int:
    return self.cells.count(Mark.EMPTY.value)

  @cached_property
  def count(self) -> int:
    return self.dimension ** 2
  
  @cached_property
  def filled_positions(self) -> list[int]:
    return [i for i, cell in enumerate(self.cells) if cell != Mark.EMPTY]

  def is_position_filled(self, index: int) -> bool:
    return self.cells[index] != Mark.EMPTY
  
  def get_position(self, index: int) -> tuple[str, int]:
    row = (index // self.dimension) + 1
    column = chr((index % self.dimension) + 65)  # Convert column number to uppercase letter
    return column, row
  
  def generate_potential_victory_sequences(self, victory_sequence_length: int) -> list[list[int]]:
    # Get all occupied cells
    filled_positions = self.filled_positions

    # Pre-calculate column and row numbers
    column_numbers = [cell % self.dimension for cell in filled_positions]
    row_numbers = [cell // self.dimension for cell in filled_positions]
  
    # Generate all possible potential victory sequences
    potential_victory_sequences = []
    victory_sequence_generator = LineGenerator(victory_sequence_length, self.dimension)
    potential_victory_sequences += victory_sequence_generator.generate_horizontal_lines(filled_positions, column_numbers, row_numbers)
    potential_victory_sequences += victory_sequence_generator.generate_vertical_lines(filled_positions, column_numbers, row_numbers)
    potential_victory_sequences += victory_sequence_generator.generate_diagonal_lines_tl_br(filled_positions, column_numbers, row_numbers)
    potential_victory_sequences += victory_sequence_generator.generate_diagonal_lines_tr_bl(filled_positions, column_numbers, row_numbers)
    return potential_victory_sequences

  def generate_possible_moves(self) -> list[int]:
    visited_cells = set()
    valid_moves = []
    for current_cell in self.filled_positions:
      valid_moves += self.search_neighboring_cells(current_cell, visited_cells, max_depth=1)
    return valid_moves
  
  def search_neighboring_cells(self, index: int, visited_cells: set[int], max_depth: int, current_depth: int = 1) -> list[int]:
    if current_depth > max_depth:
      return []
    visited_cells.add(index)
    neighbors = []
    for neighboring_cell in self.get_neighboring_cells(index):
      if neighboring_cell not in visited_cells and self.cells[neighboring_cell] == Mark.EMPTY:
        neighbors.append(neighboring_cell)
        visited_cells.add(neighboring_cell)
        neighbors += self.search_neighboring_cells(neighboring_cell, visited_cells, max_depth, current_depth + 1)
    return neighbors
  
  def get_neighboring_cells(self, current_index: int) -> list[int]:
    neighbor_offsets = [
      (-1, 0), (1, 0),  # Left, Right
      (0, -1), (0, 1),  # Top, Bottom
      (-1, -1), (1, 1),  # Top-left, Bottom-right
      (1, -1), (-1, 1)  # Top-right, Bottom-left
    ]
    neighbors = []
    for dx, dy in neighbor_offsets:
      x, y = current_index % self.dimension + dx, current_index // self.dimension + dy
      if 0 <= x < self.dimension and 0 <= y < self.dimension:
        neighbors.append(y * self.dimension + x)
    return neighbors

@dataclass(frozen=True)
class Move:
  player_mark: Mark
  position: int
  previous_state: GameState
  next_state: GameState

@dataclass(frozen=True)
class GameState:
  grid: Grid
  initial_player_mark: Mark = Mark.CROSS
  required_marks_for_win: int = 3
  last_move_position: int = None

  def __post_init__(self):
    validate_game_state(self)

  @cached_property
  def get_current_player_mark(self) -> Mark:
    return self.initial_player_mark if self.grid.cross_marks_count is self.grid.naught_marks_count else self.initial_player_mark.other
  
  @cached_property
  def has_game_started(self) -> bool:
    return self.grid.empty_cells_count != self.grid.dimension ** 2
  
  @cached_property
  def has_game_ended(self) -> bool:
    return self.has_game_started and (self.get_winner is not None or self.is_draw)
  
  @cached_property
  def is_draw(self) -> bool:
    return self.get_winner is None and self.grid.empty_cells_count == 0

  @cached_property
  def get_winner(self) -> Mark | None:
    return Mark(self.grid.cells[self.get_winning_sequence[0]]) if self.get_winning_sequence else None
  
  @cached_property
  def get_winning_sequence(self) -> list[int]:
    potential_winning_sequences = self.grid.generate_potential_victory_sequences(self.required_marks_for_win)

    # Check each sequence to see if it's a winning sequence
    for sequence in potential_winning_sequences:
      if all(self.grid.cells[i] == self.grid.cells[sequence[0]] for i in sequence):
        return sequence  # Return the winning sequence
    # If no winning sequence is found, return an empty list
    return []
  
  @cached_property
  def get_valid_moves(self) -> list[int]:
    # possible_moves = []
    if not self.has_game_ended:
      valid_move_indexes = self.grid.generate_possible_moves()
      # possible_moves = [self.generate_move_to(index) for index in valid_move_indexes]
    return valid_move_indexes

  @cached_property
  def get_last_move(self) ->tuple[str, int]:
    return self.grid.get_position(self.last_move_position) if self.last_move_position is not None else None
    
  def make_move_to(self, index: int) -> Move:
    validate_player_move(self, index)
    return self.generate_move_to(index)
  
  def generate_move_to(self, index: int) -> Move:
    return Move(
      player_mark=self.get_current_player_mark,
      position=index,
      previous_state=self,
      next_state=GameState(
        Grid(
          dimension=self.grid.dimension,
          cells=self.grid.cells[:index] + self.get_current_player_mark.value + self.grid.cells[index + 1:]
        ),
        initial_player_mark=self.initial_player_mark,
        required_marks_for_win=self.required_marks_for_win,
        last_move_position=index
      )
    )











