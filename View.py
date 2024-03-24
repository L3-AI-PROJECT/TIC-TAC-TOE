class View:
    def __init__(self):
        print("Bienvenue au jeu Tic Tac Toe")
        print("Votre symbole de pièce d'échecs est X et le symbole de pièce d'échecs informatique est O.")

    def showChessBoard(self, chessBoard):
        chess = [''] * 9
        for i in range(9):
            if chessBoard[i] == -1:
                chess[i] = 'X'
            elif chessBoard[i] == 0:
                chess[i] = '-'
            else:
                chess[i] = 'O'
        print("----------------------------")
        print("|" + chess[0] + "|" + chess[1] + "|" + chess[2] + "|")
        print("|" + chess[3] + "|" + chess[4] + "|" + chess[5] + "|")
        print("|" + chess[6] + "|" + chess[7] + "|" + chess[8] + "|")
        print("----------------------------")

    def showUser(self):
        print("----------------------------")
        print("1 2 3")
        print("4 5 6")
        print("7 8 9")
        print("C'est votre tour, veuillez entrer la position d'échecs :")

    def showFirst(self):
        print("Voulez-vous jouer en premier ? Veuillez saisir le chiffre 1 si vous souhaitez passer en premier, sinon, veuillez saisir le chiffre 2 !")

