# tic_tac_toe/logic/models.py

from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property

import random

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
  
  def generate_row_sequences(self, required_mark: int, strict: bool = False) -> list[list[int]]:
        # Get all occupied cells
    filled_positions = self.filled_positions

    # Pre-calculate column and row numbers
    column_numbers = [cell % self.dimension for cell in filled_positions]
    row_numbers = [cell // self.dimension for cell in filled_positions]

    sequence_beginning = min(column_numbers)
    sequence_end = required_mark if strict else max(max(column_numbers) + 1, sequence_beginning + required_mark)

    # Generate row sequences
    row_sequences = []
    for row in range(min(row_numbers), max(row_numbers) + 1):
      sequence = [row * self.dimension + column for column in range(sequence_beginning, sequence_end)]
      if any(i < len(self.cells) and self.cells[i] != Mark.EMPTY for i in sequence):
        line = []
        for i in sequence:
          if i < len(self.cells):
            line.append(i)
        row_sequences.append(line)
        # row_sequences.append("".join(self.cells[i] if i < len(self.cells) else "" for i in sequence))
    # Remove duplicates and return the list of row sequences
    return row_sequences
  
  def generate_column_sequences(self, required_mark: int, strict: bool = False) -> list[list[int]]:
    # Get all occupied cells
    filled_positions = self.filled_positions

    # Pre-calculate column and row numbers
    column_numbers = [cell % self.dimension for cell in filled_positions]
    row_numbers = [cell // self.dimension for cell in filled_positions]

    sequence_beginning = min(row_numbers)
    sequence_end = required_mark if strict else max(max(row_numbers) + 1, sequence_beginning + required_mark)

    # Generate column sequences
    column_sequences = []
    for column in range(min(column_numbers), max(column_numbers) + 1):
      sequence = [row * self.dimension + column for row in range(sequence_beginning, sequence_end)]
      if any(i < len(self.cells) and self.cells[i] != Mark.EMPTY for i in sequence):
        line = []
        for i in sequence:
          if i < len(self.cells):
            line.append(i)
        column_sequences.append(line)
        # column_sequences.append("".join(self.cells[i] if i < len(self.cells) else "" for i in sequence))
    # Remove duplicates and return the list of row sequences
    return column_sequences
  
  def generate_diagonal_sequences(self, required_mark: int, strict: bool = False) -> list[list[int]]:
    # Get all occupied cells
    filled_positions = self.filled_positions

    # Pre-calculate column and row numbers
    column_numbers = [cell % self.dimension for cell in filled_positions]
    row_numbers = [cell // self.dimension for cell in filled_positions]

    sequence_row_beginning = min(row_numbers)
    sequence_row_end = max(max(row_numbers), sequence_row_beginning + required_mark - 1)
    sequence_column_beginning = min(column_numbers)
    sequence_column_end = max(max(column_numbers), sequence_column_beginning + required_mark - 1)

    sequence_stop = max(1 + sequence_row_end - sequence_row_beginning, required_mark)

    sequence_end = sequence_column_end + (sequence_row_end - sequence_row_beginning)
    sequence_beginning = sequence_column_beginning - (sequence_row_end - sequence_row_beginning)


    # Generate diagonal sequences
    diagonal_sequences = []
    # Helper function to generate a sequence and append it to diagonal_sequences if it contains any non-empty cells
    def generate_sequence(col, increment):
      if 0 <= col < self.dimension:
        sequence = []
        for i in range(sequence_stop):
          res = sequence_row_beginning * self.dimension + col + i * increment
          if res < 0 or res >= self.count:
            break
          index = res % self.dimension
          sequence.append(res)
          if index == 0 or index == self.dimension:
            break
          # sequence = [sequence_row_beginning * self.dimension + col + i * increment for i in range(end)]
        if any(self.cells[i] != Mark.EMPTY for i in sequence):
          line = []
          for i in sequence:
            if i < len(self.cells):
              line.append(i)
          diagonal_sequences.append(line)

    # Generate diagonal sequences right to left
    for col in range(sequence_column_beginning, sequence_end + 1):
      generate_sequence(col, self.dimension - 1)

    # Generate diagonal sequences left to right
    for col in range(sequence_beginning, sequence_column_end + 1):
      generate_sequence(col, self.dimension + 1)
    
    return diagonal_sequences

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
  
  def fill_sequences(self, sequence: list[int]) -> str:
    return "".join(self.grid.cells[i] if i < len(self.grid.cells) else "" for i in sequence)

  @cached_property
  def generate_sequences(self) -> list[str]:
    sequences = []

    for row in self.row_sequences:
      sequences.append(self.fill_sequences(row))
    for column in self.column_sequences:
      sequences.append(self.fill_sequences(column))
    for diagonal in self.diagonal_sequences:
      sequences.append(self.fill_sequences(diagonal))
    
    return sequences

  @cached_property
  def row_sequences(self) -> list[list[int]]:
    return self.grid.generate_row_sequences(self.required_marks_for_win)

  @cached_property
  def column_sequences(self) -> list[list[int]]:
    return self.grid.generate_column_sequences(self.required_marks_for_win)
  
  @cached_property
  def diagonal_sequences(self) -> list[list[int]]:
    return self.grid.generate_diagonal_sequences(self.required_marks_for_win)

  def ee(self, sequence: list[int], start: int, current_mark: Mark) -> list[int]:
    winning_sequence = []
    for i in range(start, start + self.required_marks_for_win):
      if self.grid.cells[sequence[i]] == Mark.EMPTY.value:
        break
      if self.grid.cells[sequence[i]] != current_mark:
        break
      winning_sequence.append(sequence[i])
    return winning_sequence

  @cached_property
  def get_winning_sequence(self) -> list[int]:
    potential_winning_sequences = self.grid.generate_potential_victory_sequences(self.required_marks_for_win)
    if not self.has_game_started:
      return []
    
    # potential_winning_sequences = []

    # potential_winning_sequences.extend(self.row_sequences)
    # potential_winning_sequences.extend(self.column_sequences)
    # potential_winning_sequences.extend(self.diagonal_sequences)

    for sequence in potential_winning_sequences:
      # check if there is a winning sequence of required length
      if len(sequence) < self.required_marks_for_win:
        continue
      
      for i in range(0, len(sequence), self.required_marks_for_win):
        if i + self.required_marks_for_win > len(sequence):
          break
        winning_mark = Mark.CROSS
        winning_sequence = self.ee(sequence, i, winning_mark)
        if len(winning_sequence) == self.required_marks_for_win:
          return winning_sequence
        winning_sequence = self.ee(sequence, i, winning_mark.other)
        if len(winning_sequence) == self.required_marks_for_win:
          return winning_sequence
    return []
  
  def get_winning_sequence_positions(self, required_mark: int) ->  list[list[int]]:
    return self.grid.generate_potential_victory_sequences(required_mark)
  
  @cached_property
  def get_valid_moves(self) -> list[Move]:
    valid_moves = []
    if not self.has_game_ended:
      valid_move_indexes = self.grid.generate_possible_moves()
      valid_moves = [self.generate_move_to(index) for index in valid_move_indexes]
    return valid_moves

  @cached_property
  def get_last_move(self) -> str:
    return self.get_move_format_from_index(self.last_move_position) if self.last_move_position is not None else None
  
  def get_move_format_from_index(self, index: int) -> str:
    row = (index // self.grid.dimension) + 1 # Convert row number to 1-based index
    column = chr((index % self.grid.dimension) + 65)  # Convert column number to uppercase letter
    return f"{column}{row}"
  
  def get_position_from_move_format(self, move: str) -> int:
    column, row = move[0], int(move[1:])
    return (row - 1) * self.grid.dimension + (ord(column) - 65)
  
  def make_move_to(self, index: int) -> Move:
    validate_player_move(self, index)
    return self.generate_move_to(index)
  
  def make_random_move(self) -> Move:
    if self.has_game_started:
      return random.choice(self.get_valid_moves)
    return self.make_move_to(random.randint(0, self.grid.count - 1))
  
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
