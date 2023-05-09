import chess_utils
from lysandre.pieces.piece import Roi, Tour, Fou, Cavalier, Dame, Pion, Piece
from lysandre.plateau import Plateau


class Partie():
    def __init__(self, type_de_partie: str = "normale", tour="blanc", points_blanc=0, points_noir=1):
        self.points_blanc = 0
        self.points_noir = 0
        self.setup = False
        self.terminee = False
        self.tour = tour
        if type_de_partie == "normale":
            self.plateau = Plateau()

    def setup_from_fen(self, fen: str):
        grille = []
        rank_strings = fen.split('/')
        for rank_index, rank_string in enumerate(rank_strings):
            ligne = []
            file_index = 0
            y = rank_index
            for symbol in rank_string:
                if symbol.isdigit():
                    empty_fields = int(symbol)
                    for _ in range(empty_fields):
                        ligne.append(None)
                    file_index += empty_fields
                else:
                    piece_class, couleur = self.piece_from_symbol(symbol)
                    piece = piece_class(x=file_index, y=y, couleur=couleur)
                    ligne.append(piece)
                    file_index += 1
            grille.append(ligne)
        self.plateau = Plateau(grille)
        self.setup = True

    def piece_from_symbol(self, symbol: str):
        symbol_piece_dict = {
            'K': (Roi, "blanc"), 'Q': (Dame, "blanc"), 'R': (Tour, "blanc"), 'B': (Fou, "blanc"),
            'N': (Cavalier, "blanc"), 'P': (Pion, "blanc"),
            'k': (Roi, "noir"), 'q': (Dame, "noir"), 'r': (Tour, "noir"), 'b': (Fou, "noir"),
            'n': (Cavalier, "noir"), 'p': (Pion, "noir")
        }
        return symbol_piece_dict[symbol]

    def run(self):
        if self.setup:
            self.plateau.montrer_grille()
            while not self.terminee:
                inp_piece = input("Sélectionner une pièce :")
                if inp_piece == "q":
                    self.terminee = True
                    break
                if inp_piece == "p":
                    print(self.points_blanc, self.points_noir)
                    continue
                piece_selectionner: Piece = chess_utils.get_piece(p.plateau.get_grille(), int(inp_piece.split(',')[0]),
                                                                  int(inp_piece.split(',')[1]))
                while not piece_selectionner:
                    inp_piece = input("Sélectionner une pièce :")
                    piece_selectionner: Piece = chess_utils.get_piece(p.plateau.get_grille(),
                                                                      int(inp_piece.split(',')[0]),
                                                                      int(inp_piece.split(',')[1]))
                if piece_selectionner.couleur != self.tour:
                    print("Cette pièce n'est pas votre")
                    continue
                print(f"Vous avez sélectionné {piece_selectionner.type_de_piece}")
                print(
                    f"Voici la liste de coups possible : {piece_selectionner.liste_coups_legaux(p.plateau.get_grille())}")
                inp_coup = input("Sélectionner nouvelle coordonnées :")
                if inp_coup == "r":
                    continue
                coup = piece_selectionner.move(int(inp_coup.split(',')[0]), int(inp_coup.split(',')[1]),
                                               self.plateau.get_grille(), self)
                while not coup:
                    inp_coup = input("Sélectionner nouvelle coordonnées :")
                    coup = piece_selectionner.move(int(inp_coup.split(',')[0]), int(inp_coup.split(',')[1]),
                                                   self.plateau.get_grille(), self)
                    print(coup)
                self.plateau.set_grille(coup)
                self.plateau.montrer_grille()
                if self.tour == "blanc":
                    self.tour = "noir"
                else:
                    self.tour = "blanc"

        else:
            print("Erreur, vous n'avez pas setup la position initiale")


p = Partie()
p.setup_from_fen("8/8/8/8/8/8/3PPP2/3PK2R")
p.run()
# grille = p.plateau.get_grille()
# p.plateau.montrer_grille()
# roi: Union[Cavalier, Piece] = chess_utils.get_piece(p.plateau.get_grille(),0, 0)
# print(roi.liste_coups_legaux(grille))
# p.plateau.set_grille(roi.move(1, 0, grille, p))
# p.plateau.montrer_grille()
