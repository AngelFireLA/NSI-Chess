import chess_utils
from lysandre.plateau import Plateau
from lysandre.pieces.piece import Roi, Tour, Fou, Cavalier, Dame, Pion

class Partie():
    def __init__(self, type_de_partie: str ="normale", tour="blanc", points_blanc=0, points_noir=1):
        self.points_blanc = 0
        self.points_noir = 0
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

    def piece_from_symbol(self, symbol: str):
        symbol_piece_dict = {
            'K': (Roi, "blanc"), 'Q': (Dame, "blanc"), 'R': (Tour, "blanc"), 'B': (Fou, "blanc"),
            'N': (Cavalier, "blanc"), 'P': (Pion, "blanc"),
            'k': (Roi, "noir"), 'q': (Dame, "noir"), 'r': (Tour, "noir"), 'b': (Fou, "noir"),
            'n': (Cavalier, "noir"), 'p': (Pion, "noir")
        }
        return symbol_piece_dict[symbol]

p = Partie()
p.setup_from_fen("6bq/7b/8/8/8/8/8/8")
p.plateau.montrer_grille()
roi = chess_utils.get_piece(p.plateau.get_grille(),7, 0)
print(roi.liste_coups_legaux(p.plateau.get_grille()))