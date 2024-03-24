import random

from View import View
from ChessBoard import ChessBoard
from Algo import Algo

# Indique la difficult�� du jeu en termes de nombre de fois que le joueur peut l'utiliser
FREQ_EASY = 9;
FREQ_MEDIUM = 6;
FREQ_HARD = 3;

class Game:
  def __init__(self):
    self.freq_human = 0
    self.gameContinue = False
    self.chessBoard = ChessBoard()
    self.view = View()

  def start(self):
    print("La difficulté que vous voulez choisir:Easy:0,Medium:1,Hard:2")
    difficulte = int(input())
    if difficulte == 0:
      self.freq_human = FREQ_EASY
    elif difficulte == 1:
      self.freq_human = FREQ_MEDIUM
    else:
      self.freq_human = FREQ_HARD
    self.gameContinue = True
    while self.gameContinue:
      self.view.showFirst()
      whoFirst = int(input())
      if whoFirst == 1 or whoFirst == 2:
        self.startGame(whoFirst)
      else:
        print("Erreur de données d'entrée, veuillez les saisir à nouveau !")
        continue
      print("Voulez-vous continuer le jeu ? Entrez 1 pour continuer et 2 pour quitter le jeu !")
      next = int(input())
      while not (next == 1 or next == 2):
        print("Erreur de données d'entrée, veuillez les saisir à nouveau !")
        next = int(input())
      if next == 1:
        self.chessBoard.clearBoard()
      else:
        self.gameContinue = False
        print("Merci d'avoir joué, au revoir !")

  def startGame(self, first):
    if first == 2:
      pos = [0, 2, 6, 8]
      random.seed()
      self.chessBoard.board[pos[random.randint(0, 2) + 1]] = 1
      print("AI round:")
      self.view.showChessBoard(self.chessBoard.board)
    over = False
    while not over:
      if self.humanRound():
        break
      over = self.AIRound()

  def humanRound(self):
    self.view.showUser()
    pos = int(input())
    while self.chessBoard.board[pos - 1] != 0:
      print("Il y a déjà une pièce d'échecs dans cette position, veuillez choisir à nouveau !")
      pos = int(input())
    self.chessBoard.board[pos - 1] = -1
    self.view.showChessBoard(self.chessBoard.board)
    self.freq_human -= 1
    return self.result()

  def AIRound(self):
    self.chessBoard.board[Algo.elagage_minimax(self.chessBoard.board, -1000, 1000, True)[0]] = 1
    print("AI round")
    self.view.showChessBoard(self.chessBoard.board)
    return self.result()

  def result(self):
    result = Algo.get_result(self.chessBoard.board)
    if result == 1:
      print("L'IA a gagné la partie")
    elif result == 0:
      print("Dessine, rejouons")
    elif result == -1:
      print("Félicitations pour avoir gagné ce match")
    return result != 2