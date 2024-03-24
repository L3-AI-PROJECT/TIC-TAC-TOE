class ChessBoard:
    def __init__(self):
        # La valeur par d��faut est 0, -1 pour les pi��ces du joueur et 1 pour les pi��ces de l'ordinateur
        self.board = [0] * 9
    def clearBoard(self):
        self.board = [0] * 9