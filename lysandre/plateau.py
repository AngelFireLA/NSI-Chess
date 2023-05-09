from lysandre.pieces.piece import *

class Plateau():

    def __init__(self, grille=None):

        self.grille = grille

    def init_grille(self, pieces: list):
        self.grille= []
        for i in range(8):
            ligne = []
            for j in range(8):
                p = None
                if pieces:
                    for piece in pieces:

                        if piece.x-1 == j and piece.y-1==i:
                            p = piece
                if p:
                    #Une des classes pièces
                    ligne.append(p)
                else:
                    ligne.append(None)
            self.grille.append(ligne)
        return self.grille

    def montrer_grille(self):
        for i in self.grille:
            ligne = []
            for j in i:
                if j:
                    ligne.append(j.type_de_piece)
                else:
                    ligne.append(None)
            print(ligne)

    def get_grille(self):
        return self.grille

    def set_grille(self, grille):
        self.grille = grille

    # retourne la liste des coups légaux
    def liste_moves_legaux(self, couleur: str) -> list:
        moves = []
        for i in self.grille:
            for j in i:
                if j:
                    if j.couleur == couleur:
                        moves += j.liste_coups_legaux()
        return moves

    # vérifie s'il y a pat
    def est_pat(self) -> bool:

        pass

    # vérifie s'il ne reste que des rois sur le plateau
    def roi_contre_roi(self) -> bool:
        pieces_restantes = []
        for i in self.grille:
            for j in i:
                if j:
                    pieces_restantes.append(j)
        for piece in pieces_restantes:
            if not isinstance(piece, Roi):
                return False
        return True

