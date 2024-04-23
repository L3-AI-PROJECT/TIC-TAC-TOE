# frontend/play.py

from tic_tac_toe.game.engine import TicTacToe
from tic_tac_toe.game.players import RandomComputerPlayer
from tic_tac_toe.logic.entities import Mark

from console.renderers import ConsoleRenderer

def main():
  game = TicTacToe(
    player1=RandomComputerPlayer(Mark.CROSS),
    player2=RandomComputerPlayer(Mark.NAUGHT),
    renderer=ConsoleRenderer()
  )
  game.play(
    starting_mark=Mark.CROSS,
    dimension=3,
    winning_line_length=3
  )

if __name__ == '__main__':
  main()
