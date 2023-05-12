import chess_utils

#Vérifie si le type d'une pièce créer est valide
def type_valide(type_de_piece) -> bool:
    if not (type == "pion", type == "tour", type == "cavalier", type == "fou", type == "dame", type == "roi"):
        return False
    else:
        return True

# classe de base qui sera héritée par toute les pièces
class Piece():
    def __init__(self, couleur: str, capturee: bool == False, type_de_piece: str, x: int, y: int, valeur: int):
        # couleur de la pièce
        if couleur.lower() == "blanc" or couleur.lower() == "noir":
            self.couleur = couleur
        else:
            print("Une pièce a été définie avec une couleur invalide.")

        # position de la pièce sur la grille de 8x8 avec x en abscisse et y en ordonnée, allant de 0 jusqu'à 7
        self.x, self.y = x, y

        # Piece est capturée ou pas
        self.capturee = capturee

        # le type de la pièce
        if not type_valide(type_de_piece):
            print("Une pièce a été définie avec un type invalide.")
        else:
            self.type_de_piece = type_de_piece

        # vérifie si la pièce a déja bougée
        self.moved = False

        #Valeur de la pièce, propre à chaque pièce
        self.valeur = valeur

    #Change le type de pièce
    def set_type(self, type_de_piece):
        self.type_de_piece = type_de_piece

    #Change la couleur de la pièce
    def set_color(self, couleur):
        self.couleur = couleur


class Roi(Piece):
    def __init__(self, couleur: str, capturee: bool = False, x: int = 0, y: int = 0):
        super().__init__(couleur, capturee, "roi", x, y, 0)

    #Pareil pour toutes les pièces : Récupère tout les mouvements possible s'il  avait 0 pièces autour de la pièce, et autres coups spéciaux
    #Vérifie aussi si la pièce ne vas pas en dehors du plateau
    def get_patterne_possible(self, x, y):
        #Mouvements possibles à partir de notre pièce en fonction de notre position actuelle, première valeur est x et la seconde est y
        patterne = [(+1, +0), (+1, +1), (+0, +1), (-1, +1), (-1, +0), (-1, -1), (+0, -1), (+1, -1)]
        # Vérifie si la pièce ne va pas en dehors du plateau
        for i in range(len(patterne) - 1, -1, -1):
            if x + patterne[i][0] < 0 or x + patterne[i][0] > 7 or y + patterne[i][1] < 0 or y + \
                    patterne[i][1] > 7:
                patterne.pop(i)
        #Pour le roi, c'est les mouvements de roc s'il n'a pas encore bouger
        if not self.moved:
            patterne.append((2, 0))
            patterne.append((-2, 0))
        return patterne

    #Pareil pour toutes les pièces :  Vérifie si chaque coup est légal en prenant en comptes les autres pièces
    def liste_coups_legaux(self, grille: list):
        patterne = self.get_patterne_possible(self.x, self.y)
        move_legaux = []

        # Pour chaque coup, vérifie s'il est valide
        for move in patterne:
            # Le prochain if et elif sont les cas spéciaux du roc
            # petit roc
            if move == (2, 0):
                if self.x + move[0] <= 7:
                    # Vérifie si la case où il devrait y avoir la tour est vide
                    if not chess_utils.get_piece(grille, self.x + 3, self.y):
                        move_legaux.append(move)
                    else:
                        # Récupère la tour et si elle y est, la déplace où elle devrait
                        piece = chess_utils.get_piece(grille, self.x + 3, self.y)
                        if not (piece.type_de_piece == "tour" or piece.couleur == self.couleur or not piece.moved):
                            move_legaux.append(move)
                        else:
                            if chess_utils.get_piece(grille, self.x + 2, self.y) or chess_utils.get_piece(grille,
                                                                                                          self.x + 1,
                                                                                                          self.y):
                                move_legaux.append(move)
            # grand roc
            elif move == (-2, 0):
                if self.x + move[0] >= 0:
                    # même commentaires que pour l'autre roc
                    if not chess_utils.get_piece(grille, self.x - 4, self.y):
                        move_legaux.append(move)
                    else:
                        piece: Piece = chess_utils.get_piece(grille, self.x - 4, self.y)
                        if not (piece.type_de_piece == "tour" or piece.couleur == self.couleur or not piece.moved):
                            move_legaux.append(move)
                        else:
                            if chess_utils.get_piece(grille, self.x - 3, self.y) or chess_utils.get_piece(grille,
                                                                                                          self.x - 2,
                                                                                                          self.y) or chess_utils.get_piece(
                                    grille, self.x - 1, self.y):
                                move_legaux.append(move)

            # Vérifie s'il n'y a pas une pièce de même couleur là où on veut aller
            if grille[self.y + move[1]][self.x + move[0]] and grille[self.y + move[1]][
                self.x + move[0]].couleur == self.couleur:
                move_legaux.append(move)

        # Retourne la liste des coups légaux
        return move_legaux

    #Pareil pour toutes les pièces: bouge la pièce à l'endroit donnée, si le mouvement est valide
    def move(self, x_added, y_added, grille: list, partie):
        #vérifie si le coup est légal
        if (x_added, y_added) in self.liste_coups_legaux(grille):
            self.moved = True
            #cas spéciaux pour les rocs
            if (x_added, y_added) == (2, 0):
                #récupère la tour
                tour: Tour = grille[self.y + y_added][self.x + x_added+1]
                #la bouge
                grille = tour.move(-2, 0,grille, partie, True)
                #vide la case où nle roi était
                grille[self.y][self.x] = None
                self.x += x_added
                self.y += y_added
                #met à jour le plateau avec le roi à la nouvelle position
                grille[self.y][self.x] = self
                return grille
            if (x_added, y_added) == (-2, 0):
                #même commentaire que autre roc
                tour: Tour = grille[self.y + y_added][self.x + x_added - 2]
                grille = tour.move(3, 0, grille, partie, True)
                grille[self.y][self.x] = None
                self.x += x_added
                self.y += y_added
                grille[self.y][self.x] = self
                return grille

            #coups qui ne sont pas le roc
            else:
                #Si une pièce est trouvée sur la nouvelle case, la capturée car grâce à liste_coups_legaux, une pièce trouvée ne peut que être de couleur opposée
                if grille[self.y + y_added][self.x + x_added]:
                    self.capture(grille[self.y + y_added][self.x + x_added], partie)
                #voir commentaires des rocs
                grille[self.y][self.x] = None
                self.x += x_added
                self.y += y_added
                grille[self.y][self.x] = self
            return grille
        else:
            print(f"Le coup ({x_added}, {y_added}) n'est pas valide pour la pièce de couleur {self.couleur}.")
            return None

    def capture(self, piece_capturee: Piece, partie):
        piece_capturee.capturee = True
        # met la pièce capturée en (-1, -1) pour dire qu'elle n'est plus dans le plateau
        piece_capturee.x = -1
        piece_capturee.y = -1

        #Ajoute les points selon la couleur et pièce capturée
        if self.couleur == "blanc":
            partie.points_blanc += piece_capturee.valeur
            print(f"Les blancs ont maintenant {partie.points_blanc} points")
        if self.couleur == "noir":
            partie.points_noir += piece_capturee.valeur
            print(f"Les noirs ont maintenant {partie.points_noir} points")


class Pion(Piece):
    def __init__(self, couleur: str, capturee: bool = False, x: int = 0, y: int = 0):
        super().__init__(couleur, capturee, "pion", x, y, 1)

    def get_patterne_possible(self, grille: list):
        if self.couleur == "blanc":
            patterne = []
            # verifie si une piece is devant le pion:
            if not grille[self.y - 1][self.x]:
                # todo : vérifier s'il peut pas en passant
                patterne.append((0, -1))
            #si le pion est sur la bonne ligne et pas de pièces devant, lui laisse avancé de 2 cases
            if self.y == 6 and not chess_utils.get_piece(grille, self.x, 5):
                patterne.append((0, -2))
            return patterne
        else:
            #pareil mais si le pion est noir
            patterne = []
            if not grille[self.y + 1][self.x]:
                # todo : vérifier s'il peut pas en passant
                patterne.append((0, +1))
            if self.y == 1 and not chess_utils.get_piece(grille, self.x, 2):
                patterne.append((0, +2))
            return patterne

    def liste_coups_legaux(self, grille: list):
        patterne = self.get_patterne_possible(grille)
        #ajoute les coups de captures s'il y a une pièce de couleur opposée en diagonal
        if self.couleur == "blanc":
            if self.y - 1 >= 0 and self.x - 1 >= 0:
                if grille[self.y - 1][self.x - 1] and not grille[self.y - 1][self.x - 1].couleur == self.couleur:
                    patterne.append((-1, -1))
            if self.y - 1 >= 0 and self.x + 1 <= 7:
                if grille[self.y - 1][self.x + 1] and not grille[self.y - 1][self.x + 1].couleur == self.couleur:
                    patterne.append((1, -1))
        else:
            if self.x - 1 >= 0 and self.y + 1 <= 7:
                if grille[self.y + 1][self.x - 1] and not grille[self.y + 1][self.x - 1].couleur == self.couleur:
                    patterne.append((-1, +1))
            if self.y + 1 <= 7 and self.x + 1 <= 7:
                if grille[self.y + 1][self.x + 1] and not grille[self.y + 1][self.x + 1].couleur == self.couleur:
                    patterne.append((1, +1))
        return patterne

    def move(self, x_added, y_added, grille: list, partie):
        if (x_added, y_added) in self.liste_coups_legaux(grille):
            #Code mouvement basique
            self.moved = True
            if grille[self.y + y_added][self.x + x_added]:
                self.capture(grille[self.y + y_added][self.x + x_added], partie)
            grille[self.y][self.x] = None
            self.x += x_added
            self.y += y_added
            grille[self.y][self.x] = self
            #Code gérant la promotion en dame
            if (self.couleur == "blanc" and self.y == 0) or (self.couleur == "noir" and self.y == 7):
               new_piece = Dame(self.couleur)
               return self.promote(grille, new_piece)
            else:
                return grille
        else:
            print(f"Le coup ({x_added}, {y_added}) n'est pas valide pour la pièce de couleur {self.couleur}.")
            return None

    def capture(self, piece_capturee: Piece, partie):
        #Code basique de capture
        piece_capturee.capturee = True
        piece_capturee.x = -1
        piece_capturee.y = -1

        if self.couleur == "blanc":
            partie.points_blanc += piece_capturee.valeur
            print(f"Les blancs ont maintenant {partie.points_blanc} points")
        if self.couleur == "noir":
            partie.points_noir += piece_capturee.valeur
            print(f"Les noirs ont maintenant {partie.points_noir} points")

    #Fonction gérant la promotion du pion
    def promote(self, grille: list, new_piece: Piece):
        #Créer une nouvelle pièce (une dame) et remplace le pion par cette dame à qui on donne les bons attributs
        grille[self.y][self.x] = new_piece
        new_piece.x = self.x
        new_piece.y = self.y
        new_piece.moved = True
        return grille


class Cavalier(Piece):
    def __init__(self, couleur: str, capturee: bool = False, x: int = 0, y: int = 0):
        super().__init__(couleur, capturee, "cavalier", x, y, 3)

    #Rien de spécial
    def get_patterne_possible(self):
        patterne = [(+2, +1), (+2, -1), (-2, +1), (-2, -1), (+1, +2), (+1, -2), (-1, +2), (-1, -2)]
        #vérifie si la pièce ne va pas en dehors du plateau
        for i in range(len(patterne) - 1, -1, -1):
            if self.x + patterne[i][0] < 0 or self.x + patterne[i][0] > 7 or self.y + patterne[i][1] < 0 or self.y + \
                    patterne[i][1] > 7:
                patterne.pop(i)
        return patterne

    def liste_coups_legaux(self, grille: list):
        coups = self.get_patterne_possible()
        move_illegaux = []
        for coup in coups:
            if grille[self.y+coup[1]][self.x+coup[0]] and not grille[self.y+coup[1]][self.x+coup[0]].couleur == self.couleur:
                move_illegaux.append(coup)
        for move in move_illegaux:
            coups.remove(move)
        return coups

    def move(self, x_added, y_added, grille: list, partie):
        if (x_added, y_added) in self.liste_coups_legaux(grille):
            self.moved = True
            if grille[self.y + y_added][self.x + x_added]:
                self.capture(grille[self.y + y_added][self.x + x_added], partie)
            grille[self.y][self.x] = None
            self.x += x_added
            self.y += y_added
            grille[self.y][self.x] = self
            return grille
        else:
            print(f"Le coup ({x_added}, {y_added}) n'est pas valide pour la pièce de couleur {self.couleur}.")
            return None

    def capture(self, piece_capturee: Piece, partie):
        piece_capturee.capturee = True
        piece_capturee.x = -1
        piece_capturee.y = -1

        if self.couleur == "blanc":
            partie.points_blanc += piece_capturee.valeur
            print(f"Les blancs ont maintenant {partie.points_blanc} points")
        if self.couleur == "noir":
            partie.points_noir += piece_capturee.valeur
            print(f"Les noirs ont maintenant {partie.points_noir} points")


class Tour(Piece):
    def __init__(self, couleur: str, capturee: bool = False, x: int = 0, y: int = 0):
        super().__init__(couleur, capturee, "tour", x, y, 5)

    #Pour tour et fou, patterne n'est que 1 dans chaque direction possible
    def get_patterne_possible(self):
        patterne = [(+1, +0), (-1, +0), (+0, +1), (+0, -1)]
        for i in range(len(patterne) - 1, -1, -1):
            if self.x + patterne[i][0] < 0 or self.x + patterne[i][0] > 7 or self.y + patterne[i][1] < 0 or self.y + \
                    patterne[i][1] > 7:
                patterne.pop(i)
        return patterne

    def liste_coups_legaux(self, grille: list):
        patterne = self.get_patterne_possible()
        new_patterne = []
        for move in patterne:
            x = move[0]
            y = move[1]
            # Fait bouger la tour jusqu'à ce qu'elle atteigne une case non vide
            while True:
                if not chess_utils.get_piece(grille, self.x + x, self.y + y):
                    new_patterne.append((x, y))
                else:
                    if chess_utils.get_piece(grille, self.x + x, self.y + y).couleur != self.couleur:
                        new_patterne.append((x, y))
                        break
                    else:
                        break
                #ajoute 1 aux directions pour que si la pièce n'a pas atteint une case non vide, elle essaye la prochaine case
                if x > 0:
                    x += 1
                if x < 0:
                    x -= 1
                if y > 0:
                    y += 1
                if y < 0:
                    y -= 1
                #stop la boucle aussi si la pièce sortirait du plateau
                if x + self.x > 7 or x + self.x < 0 or y + self.y > 7 or y + self.y < 0:
                    break
        return new_patterne

    def move(self, x_added, y_added, grille: list, partie, forced=False):
        #forced permet de forcer le mouvement de la tour car ce n'est utilisé que pour le roc, et le roc lui même vérifie les condtions nécessaires pour le mouvement
        if (x_added, y_added) in self.liste_coups_legaux(grille) or forced:
            self.moved = True
            if not forced and grille[self.y + y_added][self.x + x_added]:
                self.capture(grille[self.y + y_added][self.x + x_added], partie)
            grille[self.y][self.x] = None
            self.x += x_added
            self.y += y_added
            grille[self.y][self.x] = self
            return grille
        else:
            print(f"Le coup ({x_added}, {y_added}) n'est pas valide pour la pièce de couleur {self.couleur}.")
            return None

    def capture(self, piece_capturee: Piece, partie):
        piece_capturee.capturee = True
        # met la pièce capturée en (1, 1) pour dire qu'elle n'est plus dans le plateau
        piece_capturee.x = -1
        piece_capturee.y = -1

        if self.couleur == "blanc":
            partie.points_blanc += piece_capturee.valeur
            print(f"Les blancs ont maintenant {partie.points_blanc} points")
        if self.couleur == "noir":
            partie.points_noir += piece_capturee.valeur
            print(f"Les noirs ont maintenant {partie.points_noir} points")


class Dame(Piece):
    def __init__(self, couleur: str, capturee: bool = False, x: int = 0, y: int = 0):
        super().__init__(couleur, capturee, "dame", x, y, 9)

    def get_patterne_possible(self):
        #2 patternes pour les mouvements dont ils sont nommés
        patterne_diagonale = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
        patterne_tour = [(+1, +0), (-1, +0), (+0, +1), (+0, -1)]
        for i in range(len(patterne_diagonale) - 1, -1, -1):
            if self.x + patterne_diagonale[i][0] < 0 or self.x + patterne_diagonale[i][0] > 7 or self.y + \
                    patterne_diagonale[i][1] < 0 or self.y + patterne_diagonale[i][1] > 7:
                patterne_diagonale.pop(i)
        for i in range(len(patterne_tour) - 1, -1, -1):
            if self.x + patterne_tour[i][0] < 0 or self.x + patterne_tour[i][0] > 7 or self.y + patterne_tour[i][
                1] < 0 or self.y + patterne_tour[i][1] > 7:
                patterne_tour.pop(i)
        return patterne_diagonale, patterne_tour

    def liste_coups_legaux(self, grille: list):
        patterne = self.get_patterne_possible()
        new_patterne = []
        #répète les boucles pour les mouvements légaux de la tour et du fou
        for move in patterne[0]:
            x = move[0]
            y = move[1]
            while True:
                if not chess_utils.get_piece(grille, self.x + x, self.y + y):
                    new_patterne.append((x, y))
                else:
                    if chess_utils.get_piece(grille, self.x + x, self.y + y).couleur != self.couleur:
                        new_patterne.append((x, y))
                        break
                    else:
                        break
                if x > 0:
                    x += 1
                if x < 0:
                    x -= 1
                if y > 0:
                    y += 1
                if y < 0:
                    y -= 1
                if x + self.x > 7 or x + self.x < 0 or y + self.y > 7 or y + self.y < 0:
                    break
        for move in patterne[1]:
            x = move[0]
            y = move[1]
            # make rook move in direction until it goes on a square that isn't None
            while True:
                if not chess_utils.get_piece(grille, self.x + x, self.y + y):
                    new_patterne.append((x, y))
                else:
                    if chess_utils.get_piece(grille, self.x + x, self.y + y).couleur != self.couleur:
                        new_patterne.append((x, y))
                        break
                    else:
                        break
                if x > 0:
                    x += 1
                if x < 0:
                    x -= 1
                if y > 0:
                    y += 1
                if y < 0:
                    y -= 1
                if x + self.x > 7 or x + self.x < 0 or y + self.y > 7 or y + self.y < 0:
                    break
        #supprime les coups duppliqués avec list(set(new_patterne))
        return list(set(new_patterne))

    def move(self, x_added, y_added, grille: list, partie):
        if (x_added, y_added) in self.liste_coups_legaux(grille):
            self.moved = True
            if grille[self.y + y_added][self.x + x_added]:
                self.capture(grille[self.y + y_added][self.x + x_added], partie)
            grille[self.y][self.x] = None
            self.x += x_added
            self.y += y_added
            grille[self.y][self.x] = self
            return grille
        else:
            print(f"Le coup ({x_added}, {y_added}) n'est pas valide pour la pièce de couleur {self.couleur}.")
            return None

    def capture(self, piece_capturee: Piece, partie):
        piece_capturee.capturee = True
        # met la pièce capturée en (1, 1) pour dire qu'elle n'est plus dans le plateau
        piece_capturee.x = -1
        piece_capturee.y = -1

        if self.couleur == "blanc":
            partie.points_blanc += piece_capturee.valeur
            print(f"Les blancs ont maintenant {partie.points_blanc} points")
        if self.couleur == "noir":
            partie.points_noir += piece_capturee.valeur
            print(f"Les noirs ont maintenant {partie.points_noir} points")


class Fou(Piece):
    def __init__(self, couleur: str, capturee: bool = False, x: int = 0, y: int = 0):
        super().__init__(couleur, capturee, "fou", x, y, 3)

    #pareil que tour presque
    def get_patterne_possible(self):
        patterne = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
        for i in range(len(patterne) - 1, -1, -1):
            if self.x + patterne[i][0] < 0 or self.x + patterne[i][0] > 7 or self.y + patterne[i][1] < 0 or self.y + \
                    patterne[i][1] > 7:
                patterne.pop(i)
        return patterne

    def liste_coups_legaux(self, grille: list):
        patterne = self.get_patterne_possible()
        new_patterne = []
        for move in patterne:
            x = move[0]
            y = move[1]
            while True:
                if not chess_utils.get_piece(grille, self.x + x, self.y + y):
                    new_patterne.append((x, y))
                else:
                    if chess_utils.get_piece(grille, self.x + x, self.y + y).couleur != self.couleur:
                        print(f"piece de couleur différente trouvée en x{x} et y{y}")
                        new_patterne.append((x, y))
                        break
                    else:
                        print(f"piece de même couleur trouvée en x{x} et y{y}")
                        break
                if x > 0:
                    x += 1
                if x < 0:
                    x -= 1
                if y > 0:
                    y += 1
                if y < 0:
                    y -= 1
                if x + self.x > 7 or x + self.x < 0 or y + self.y > 7 or y + self.y < 0:
                    break
        return new_patterne

    def move(self, x_added, y_added, grille: list, partie):
        if (x_added, y_added) in self.liste_coups_legaux(grille):
            self.moved = True
            if grille[self.y + y_added][self.x + x_added]:
                self.capture(grille[self.y + y_added][self.x + x_added], partie)
            grille[self.y][self.x] = None
            self.x += x_added
            self.y += y_added
            grille[self.y][self.x] = self
            return grille
        else:
            print(f"Le coup ({x_added}, {y_added}) n'est pas valide pour la pièce de couleur {self.couleur}.")
            return None

    def capture(self, piece_capturee: Piece, partie):
        piece_capturee.capturee = True
        # met la pièce capturée en (1, 1) pour dire qu'elle n'est plus dans le plateau
        piece_capturee.x = -1
        piece_capturee.y = -1

        if self.couleur == "blanc":
            partie.points_blanc += piece_capturee.valeur
            print(f"Les blancs ont maintenant {partie.points_blanc} points")
        if self.couleur == "noir":
            partie.points_noir += piece_capturee.valeur
            print(f"Les noirs ont maintenant {partie.points_noir} points")

