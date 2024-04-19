# tic_tac_toe/logic/models.py

from __future__ import annotations

from dataclasses import dataclass, field
from functools import cached_property
from collections import deque

from tic_tac_toe.logic.mark import Mark
from tic_tac_toe.logic.validators import validate_game_state, validate_grid, validate_move

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
          if len(line) == self.length:
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
      if column_numbers[i] + self.length > self.dimension or row_numbers[i] + self.length > self.dimension:
        break
      line = []
      for k in range(i, len(occupied_cells)):
        if len(line) == self.length:
          break
        if k < len(occupied_cells) and row_numbers[k] - row_numbers[i] == column_numbers[k] - column_numbers[i]:
          line.append(occupied_cells[k])
      if len(line) == self.length:
        lines.append(line)
    return lines
  
  def generate_diagonal_lines_tr_bl(self, occupied_cells: list[int], column_numbers: list[int], row_numbers: list[int]) -> list[list[int]]:
    lines = []
    for i in range(len(occupied_cells)):
      if column_numbers[i] - self.length < -1 or row_numbers[i] + self.length > self.dimension:
        continue
      line = []
      for k in range(i, len(occupied_cells)):
        if len(line) == self.length:
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
  occupied_cells: list[int] = field(default_factory=list)
  
  def __post_init__(self):
    if self.cells is None:
      object.__setattr__(self, "cells", Mark.EMPTY * self.dimension ** 2)
    
    validate_grid(self)
    object.__setattr__(self, "occupied_cells", self.get_filled_cells())
  
  @cached_property
  def x_count(self) -> int:
    return self.cells.count(Mark.CROSS.value)
  
  @cached_property
  def o_count(self) -> int:
    return self.cells.count(Mark.NAUGHT.value)
  
  @cached_property
  def empty_count(self) -> int:
    return self.cells.count(Mark.EMPTY.value)
  
  def get_filled_cells(self) -> list[int]:
    return [i for i, cell in enumerate(self.cells) if cell != Mark.EMPTY]

  def generate_possible_win_patterns(self, length: int) -> list[list[int]]:
    # Get all occupied cells
    occupied_cells = self.occupied_cells

    # Pre-calculate column and row numbers
    column_numbers = [cell % self.dimension for cell in occupied_cells]
    row_numbers = [cell // self.dimension for cell in occupied_cells]
  
    # Generate all possible lines
    lines = []
    generator = LineGenerator(length, self.dimension)
    lines += generator.generate_horizontal_lines(occupied_cells, column_numbers, row_numbers)
    lines += generator.generate_vertical_lines(occupied_cells, column_numbers, row_numbers)
    lines += generator.generate_diagonal_lines_tl_br(occupied_cells, column_numbers, row_numbers)
    lines += generator.generate_diagonal_lines_tr_bl(occupied_cells, column_numbers, row_numbers)
    return lines

  def generate_possible_moves(self) -> list[int]:
    visited = set()
    moves = []
    for cell in self.occupied_cells:
      moves += self.search_neighboring_cells(cell, visited, max_depth=1)
    return moves
  
  def search_neighboring_cells(self, index: int, visited: set[int], max_depth: int, current_depth: int = 1) -> list[int]:
    if current_depth > max_depth:
      return []
    visited.add(index)
    neighbors = []
    for neighbor in self.get_neighbors(index):
      if neighbor not in visited and self.cells[neighbor] == Mark.EMPTY:
        neighbors.append(neighbor)
        visited.add(neighbor)
        neighbors += self.search_neighboring_cells(neighbor, visited, max_depth, current_depth + 1)
    return neighbors
  
  def get_neighbors(self, current_index: int) -> list[int]:
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
  mark: Mark
  cell_index: int
  previous_state: GameState
  next_state: GameState

@dataclass(frozen=True)
class GameState:
  grid: Grid
  starting_mark: Mark = Mark.CROSS
  winning_line_length: int = 3

  def __post_init__(self):
    validate_game_state(self)

  @cached_property
  def current_mark(self) -> Mark:
    return self.starting_mark if self.grid.x_count is self.grid.o_count else self.starting_mark.other
  
  @cached_property
  def is_game_started(self) -> bool:
    return not self.grid.empty_count == self.grid.dimension ** 2
  
  @cached_property
  def is_game_over(self) -> bool:
    return self.is_game_started and (self.winner is not None or self.is_tie)
  
  @cached_property
  def is_tie(self) -> bool:
    return self.winner is None and self.grid.empty_count == 0

  @cached_property
  def winner(self) -> Mark | None:
    return Mark(self.grid.cells[self.winning_cells[0]]) if self.winning_cells else None
  
  @cached_property
  def winning_cells(self) -> list[int]:
    lines = self.grid.generate_possible_win_patterns(self.winning_line_length)

    # Check each line to see if it's a winning line
    for line in lines:
      if all(self.grid.cells[i] == self.grid.cells[line[0]] for i in line):
        return line  # Return the winning line
    # If no winning line is found, return an empty list
    return []
  
  @cached_property
  def possible_moves(self) -> list[Move]:
    moves = []
    if not self.is_game_over:
      indexes = self.grid.generate_possible_moves()
      moves = [self.make_move_to(index) for index in indexes]
    return moves

  def make_move_to(self, index: int) -> Move:
    validate_move(self, index)
    return Move(
      mark=self.current_mark,
      cell_index=index,
      previous_state=self,
      next_state=GameState(
        Grid(
          dimension=self.grid.dimension,
          cells=self.grid.cells[:index] + self.current_mark.value + self.grid.cells[index + 1:]
        ),
        starting_mark=self.starting_mark
      )
    )











