

class Plateau():

    def __init__(self, pieces: list):
        self.grille = self.init_grille(pieces)
        pass

    def init_grille(self, pieces: list):
        grille= []
        for i in range(8):
            ligne = []
            for j in range(8):
                p = None
                if pieces:
                    for piece in pieces:

                        if piece.x-1 == j and piece.y-1==i:
                            p = piece
                if p:
                    ligne.append(p)
                else:
                    ligne.append(".")
            grille.append(ligne)
        return grille

    def montrer_grille(self):
        for i in self.grille:
            print(i)

    def liste_moves_legaux(self) -> list:
        #retourne la liste des coups légaux
        pass

    def est_pat(self) -> bool:
        #vérifie s'il y a pat
        pass

    def est_roi_contre_roi(self) -> bool:
        #vérifie s'il ne reste que des rois
        pass

    def get_piece(self, x, y):
        if self.grille[y][x] == ".":
            return None
        else:
            return self.grille[y][x]
