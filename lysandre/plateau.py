from lysandre.pieces.piece import *

class Plateau():

    def __init__(self, grille=None):
        self.grille = grille

    #Montre la grille mais en 8 lignes pour faire plus beau
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

    #Vérifie s'il y a au moins un roi de chaque couleur restant, si non, retourne la couleur gagnante
    def check_si_roi_restant(self):
        compteur_de_roi = {"blanc":0, "noir":0}
        for i in self.grille:
            for j in i:
                if j and j.type_de_piece == "roi":
                    if j.couleur == "blanc":
                        compteur_de_roi["blanc"] += 1
                    if j.couleur == "noir":
                        compteur_de_roi["noir"] += 1

        if compteur_de_roi["blanc"] == 0:
            return "noir"
        elif compteur_de_roi["noir"] == 0:
            return "blanc"
        else:
            return False

    #Change le plateau en le plateau donné
    def set_grille(self, grille):
        self.grille = grille

    # retourne la liste des coups légaux de toutes les pièces du joueur de couleur donnée
    def liste_moves_legaux(self, couleur: str) -> list:
        moves = []
        for i in self.grille:
            for j in i:
                if j:
                    if j.couleur == couleur:
                        moves += j.liste_coups_legaux()
        return moves


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

