# tic_tac_toe/logic/exceptions.py


class InvalidGameStateError(Exception):
  """Exception raised for invalid game state."""

class InvalidMoveError(Exception):
  """Exception raised for invalid player move."""