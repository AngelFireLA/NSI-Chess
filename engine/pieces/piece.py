
# classe de base qui sera héritée par toute les pièces
class Piece:
    def __init__(self, couleur: str, type_de_piece: str, x: int, y: int, valeur: int):
        self.couleur = couleur
        self.x, self.y = x, y
        self.type_de_piece = type_de_piece
        self.moved = False
        self.valeur = valeur


class Roi(Piece):
    def __init__(self, couleur: str, x: int = 0, y: int = 0):
        super().__init__(couleur, "roi", x, y, 30000)
    def copy(self):
        new_piece = Roi(self.couleur,  self.x, self.y)
        new_piece.moved = self.moved
        return new_piece
    #Pareil pour toutes les pièces : Récupère tout les mouvements possible s'il  avait 0 pièces autour de la pièce, et autres coups spéciaux
    #Vérifie aussi si la pièce ne vas pas en dehors du plateau
    def get_patterne_possible(self):
        #Mouvements possibles à partir de notre pièce en fonction de notre position actuelle, première valeur est x et la seconde est y
        patterne = [(2, 0), (-2, 0), (+1, +0), (+1, +1), (+0, +1), (-1, +1), (-1, +0), (-1, -1), (+0, -1), (+1, -1)]
        # Vérifie si la pièce ne va pas en dehors du plateau
        for i in range(len(patterne) - 1, -1, -1):
            if self.x + patterne[i][0] < 0 or self.x + patterne[i][0] > 7 or self.y + patterne[i][1] < 0 or self.y + \
                    patterne[i][1] > 7:
                patterne.pop(i)
        #Pour le roi, c'est les mouvements de roc s'il n'a pas encore bouger
        return patterne

    #Pareil pour toutes les pièces :  Vérifie si chaque coup est légal en prenant en comptes les autres pièces
    def liste_coups_legaux(self, grille: list, peut_capturer_allie=False):
        patterne = self.get_patterne_possible()
        move_legaux = []

        # Pour chaque coup, vérifie s'il est valide
        for move in patterne:
            # Le prochain if et elif sont les cas spéciaux du roc
            # petit roc
            if move == (2, 0):
                if self.x + 3 <= 7 and not self.moved:
                    if grille[self.y][self.x + 3]:
                        # Récupère la tour et si elle y est, la déplace où elle devrait
                        piece = grille[self.y][self.x + 3]
                        if piece.type_de_piece == "tour" and piece.couleur == self.couleur and not piece.moved:
                            if not grille[self.y][self.x + 2] and not grille[self.y][self.x + 1]:
                                move_legaux.append(move)

                            else:
                                continue
                        else:
                            continue
                    else:
                        continue
                else:
                    continue
            # grand roc
            elif move == (-2, 0):
                if self.x - 4 >= 0 and not self.moved:
                    # même commentaires que pour l'autre roc
                    if grille[self.y][self.x - 4]:
                        piece: Piece = grille[self.y][self.x - 4]
                        if piece.type_de_piece == "tour" and piece.couleur == self.couleur and not piece.moved:
                            if not grille[self.y][self.x - 3] and not grille[self.y][self.x - 2] and not grille[self.y][self.x - 1]:
                                move_legaux.append(move)
                            else:
                                continue
                        else:
                            continue
                    else:
                        continue
                else:
                    continue

            # Vérifie s'il n'y a pas une pièce de même couleur là où on veut aller
            if grille[self.y + move[1]][self.x + move[0]]:
                if peut_capturer_allie and grille[self.y + move[1]][self.x + move[0]].couleur == self.couleur:
                    move_legaux.append(move)
                elif not grille[self.y + move[1]][self.x + move[0]].couleur == self.couleur:
                    move_legaux.append(move)
            else:
                move_legaux.append(move)

        # Retourne la liste des coups légaux
        return move_legaux


    #Pareil pour toutes les pièces: bouge la pièce à l'endroit donnée, si le mouvement est valide
    def move(self, x_added, y_added, grille: list):
        #vérifie si le coup est légal
        if (x_added, y_added) in self.liste_coups_legaux(grille):
            self.moved = True
            #cas spéciaux pour les rocs
            if (x_added, y_added) == (2, 0):
                #récupère la tour
                tour: Tour = grille[self.y + y_added][self.x + x_added+1]
                #la bouge
                grille = tour.move(-2, 0,grille, True)
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
                grille = tour.move(3, 0, grille, True)
                grille[self.y][self.x] = None
                self.x += x_added
                self.y += y_added
                grille[self.y][self.x] = self
                return grille

            #coups qui ne sont pas le roc
            else:
                #Si une pièce est trouvée sur la nouvelle case, la capturée car grâce à liste_coups_legaux, une pièce trouvée ne peut que être de couleur opposée

                #voir commentaires des rocs
                grille[self.y][self.x] = None
                self.x += x_added
                self.y += y_added
                grille[self.y][self.x] = self
            return grille
        else:
            raise ValueError(f"Le coup({x_added}, {y_added}) n'est pas valide pour la pièce {self.type_de_piece} de couleur {self.couleur} au coordonnées {(self.x, self.y)}.")


class Pion(Piece):
    def __init__(self, couleur: str, x: int = 0, y: int = 0):
        super().__init__(couleur, "pion", x, y, 100)
    def copy(self):
        new_piece = Pion(self.couleur,  self.x, self.y)

        return new_piece
    def get_patterne_possible(self, grille: list):
        if self.couleur == "blanc":
            patterne = []
            # verifie si une piece is devant le pion:
            if not grille[self.y - 1][self.x]:
                patterne.append((0, -1))
            #si le pion est sur la bonne ligne et pas de pièces devant, lui laisse avancé de 2 cases
            if self.y == 6 and not grille[4][self.x] and not grille[5][self.x]:
                patterne.append((0, -2))
            return patterne
        else:
            #pareil mais si le pion est noir
            patterne = []
            if not grille[self.y + 1][self.x]:
                patterne.append((0, +1))
            if self.y == 1 and not grille[3][self.x] and not grille[2][self.x]:
                patterne.append((0, +2))
            return patterne

    def liste_coups_legaux(self, grille: list, peut_capturer_allie=False):
        patterne = self.get_patterne_possible(grille)
        #ajoute les coups de captures s'il y a une pièce de couleur opposée en diagonal
        if self.couleur == "blanc":
            if self.y - 1 >= 0 and self.x - 1 >= 0:
                if grille[self.y - 1][self.x - 1]:
                    if not grille[self.y - 1][self.x - 1].couleur == self.couleur:
                        patterne.append((-1, -1))
                    elif peut_capturer_allie:
                        patterne.append((-1, -1))
            if self.y - 1 >= 0 and self.x + 1 <= 7:
                if grille[self.y - 1][self.x + 1]:
                    if not grille[self.y - 1][self.x + 1].couleur == self.couleur:
                        patterne.append((1, -1))
                    elif peut_capturer_allie:
                        patterne.append((1, -1))
        else:
            if self.x - 1 >= 0 and self.y + 1 <= 7:
                if grille[self.y + 1][self.x - 1]:
                    if not grille[self.y + 1][self.x - 1].couleur == self.couleur:
                        patterne.append((-1, +1))
                    elif peut_capturer_allie:
                        patterne.append((-1, +1))
            if self.y + 1 <= 7 and self.x + 1 <= 7:
                if grille[self.y + 1][self.x + 1]:
                    if not grille[self.y + 1][self.x + 1].couleur == self.couleur:
                        patterne.append((1, +1))
                    elif peut_capturer_allie:
                        patterne.append((1, +1))
        return patterne

    def move(self, x_added, y_added, grille: list):
        if (x_added, y_added) in self.liste_coups_legaux(grille):
            #Code mouvement basique
            self.moved = True

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
            from engine import endgame_and_opening_move_finder
            print(endgame_and_opening_move_finder.board_to_fen(grille, self.couleur))
            raise ValueError(f"Le coup({x_added}, {y_added}) n'est pas valide pour la pièce {self.type_de_piece} de couleur {self.couleur} au coordonnées {(self.x, self.y)}.")



    #Fonction gérant la promotion du pion
    def promote(self, grille: list, new_piece: Piece):
        #Créer une nouvelle pièce (une dame) et remplace le pion par cette dame à qui on donne les bons attributs
        grille[self.y][self.x] = new_piece
        new_piece.x = self.x
        new_piece.y = self.y
        new_piece.moved = True
        return grille

class Cavalier(Piece):
    def __init__(self, couleur: str, x: int = 0, y: int = 0):
        super().__init__(couleur, "cavalier", x, y, 300)
    def copy(self):
        new_piece = Cavalier(self.couleur, self.x, self.y)

        return new_piece
    #Rien de spécial
    def get_patterne_possible(self):
        patterne = [(+2, +1), (+2, -1), (-2, +1), (-2, -1), (+1, +2), (+1, -2), (-1, +2), (-1, -2)]
        #vérifie si la pièce ne va pas en dehors du plateau
        for i in range(len(patterne) - 1, -1, -1):
            if self.x + patterne[i][0] < 0 or self.x + patterne[i][0] > 7 or self.y + patterne[i][1] < 0 or self.y + \
                    patterne[i][1] > 7:
                patterne.pop(i)
        return patterne

    def liste_coups_legaux(self, grille: list, peut_capturer_allie=False):
        coups = self.get_patterne_possible()
        move_illegaux = []
        for coup in coups:
            if grille[self.y+coup[1]][self.x+coup[0]]:
                if grille[self.y + coup[1]][self.x + coup[0]].couleur == self.couleur and not peut_capturer_allie:
                    move_illegaux.append(coup)
        for move in move_illegaux:
            coups.remove(move)
        return coups

    def move(self, x_added, y_added, grille: list):
        if (x_added, y_added) in self.liste_coups_legaux(grille):
            self.moved = True
            if grille[self.y + y_added][self.x + x_added]:
                if grille[self.y + y_added][self.x + x_added].couleur == self.couleur:
                    raise ValueError(f"Le coup({x_added}, {y_added}) n'est pas valide pour la piéce {self.type_de_piece} de couleur {self.couleur} au coordonnées {(self.x, self.y)}.")
            grille[self.y][self.x] = None
            self.x += x_added
            self.y += y_added
            grille[self.y][self.x] = self
            return grille
        else:

            raise ValueError(f"Le coup({x_added}, {y_added}) n'est pas valide pour la pièce {self.type_de_piece} de couleur {self.couleur} au coordonnées {(self.x, self.y)}.")



class Tour(Piece):
    def __init__(self, couleur: str, x: int = 0, y: int = 0):
        super().__init__(couleur, "tour", x, y, 500)
    def copy(self):
        new_piece = Tour(self.couleur,  self.x, self.y)

        return new_piece
    #Pour tour et fou, patterne n'est que 1 dans chaque direction possible
    def get_patterne_possible(self):
        patterne = [(+1, +0), (-1, +0), (+0, +1), (+0, -1)]
        for i in range(len(patterne) - 1, -1, -1):
            if self.x + patterne[i][0] < 0 or self.x + patterne[i][0] > 7 or self.y + patterne[i][1] < 0 or self.y + \
                    patterne[i][1] > 7:
                patterne.pop(i)
        return patterne

    def liste_coups_legaux(self, grille: list, peut_capturer_allie=False):
        patterne = self.get_patterne_possible()
        new_patterne = []
        for move in patterne:
            x = move[0]
            y = move[1]
            # Fait bouger la tour jusqu'à ce qu'elle atteigne une case non vide
            while True:
                if not grille[self.y+y][self.x+x]:
                    new_patterne.append((x, y))
                else:
                    if not grille[self.y+y][self.x+x].couleur == self.couleur:
                        new_patterne.append((x, y))
                        break
                    elif peut_capturer_allie:
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

    def move(self, x_added, y_added, grille: list, forced=False):
        #forced permet de forcer le mouvement de la tour car ce n'est utilisé que pour le roc, et le roc lui même vérifie les condtions nécessaires pour le mouvement
        if (x_added, y_added) in self.liste_coups_legaux(grille) or forced:
            self.moved = True

            grille[self.y][self.x] = None
            self.x += x_added
            self.y += y_added
            grille[self.y][self.x] = self
            return grille
        else:
            raise ValueError(f"Le coup({x_added}, {y_added}) n'est pas valide pour la pièce {self.type_de_piece} de couleur {self.couleur} au coordonnées {(self.x, self.y)}.")



class Dame(Piece):
    def __init__(self, couleur: str, x: int = 0, y: int = 0):
        super().__init__(couleur, "dame", x, y, 900)
    def copy(self):
        new_piece = Dame(self.couleur,  self.x, self.y)

        return new_piece
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

    def liste_coups_legaux(self, grille: list, peut_capturer_allie=False):
        patterne = self.get_patterne_possible()
        new_patterne = []
        #répète les boucles pour les mouvements légaux de la tour et du fou
        for move in patterne[0]:
            x = move[0]
            y = move[1]
            while True:
                if x + self.x > 7 or x + self.x < 0 or y + self.y > 7 or y + self.y < 0:
                    break
                if not grille[self.y+y][self.x+x]:
                    new_patterne.append((x, y))
                else:
                    if grille[self.y+y][self.x+x].couleur != self.couleur:
                        new_patterne.append((x, y))
                        break
                    elif peut_capturer_allie:
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
            if x + self.x > 7 or x + self.x < 0 or y + self.y > 7 or y + self.y < 0:
                break
            # make rook move in direction until it goes on a square that isn't None
            while True:
                if not grille[self.y+y][self.x+x]:
                    new_patterne.append((x, y))
                else:
                    if grille[self.y+y][self.x+x].couleur != self.couleur:
                        new_patterne.append((x, y))
                        break
                    elif peut_capturer_allie:
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

    def move(self, x_added, y_added, grille: list):
        if (x_added, y_added) in self.liste_coups_legaux(grille):
            self.moved = True

            grille[self.y][self.x] = None
            self.x += x_added
            self.y += y_added
            grille[self.y][self.x] = self
            return grille
        else:
            raise ValueError(f"Le coup({x_added}, {y_added}) n'est pas valide pour la pièce {self.type_de_piece} de couleur {self.couleur} au coordonnées {(self.x, self.y)}.")



class Fou(Piece):
    def __init__(self, couleur: str, x: int = 0, y: int = 0):
        super().__init__(couleur, "fou", x, y, 320)
    def copy(self):
        new_piece = Fou(self.couleur,  self.x, self.y)

        return new_piece
    #pareil que tour presque
    def get_patterne_possible(self):
        patterne = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
        for i in range(len(patterne) - 1, -1, -1):
            if self.x + patterne[i][0] < 0 or self.x + patterne[i][0] > 7 or self.y + patterne[i][1] < 0 or self.y + \
                    patterne[i][1] > 7:
                patterne.pop(i)
        return patterne

    def liste_coups_legaux(self, grille: list, peut_capturer_allie=False):
        patterne = self.get_patterne_possible()
        new_patterne = []
        for move in patterne:
            x = move[0]
            y = move[1]
            while True:
                if not grille[self.y+y][self.x+x]:
                    new_patterne.append((x, y))
                else:
                    if grille[self.y+y][self.x+x].couleur != self.couleur:
                        new_patterne.append((x, y))
                        break
                    elif peut_capturer_allie:
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
        return new_patterne

    def move(self, x_added, y_added, grille: list):
        if (x_added, y_added) in self.liste_coups_legaux(grille):
            self.moved = True

            grille[self.y][self.x] = None
            self.x += x_added
            self.y += y_added
            grille[self.y][self.x] = self
            return grille
        else:

            raise ValueError(f"Le coup({x_added}, {y_added}) n'est pas valide pour la pièce {self.type_de_piece} de couleur {self.couleur} au coordonnées {(self.x, self.y)}.")




