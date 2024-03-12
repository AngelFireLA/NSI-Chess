import json
import random

import chess_utils


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
        new_piece = Roi(self.couleur, self.x, self.y)
        new_piece.moved = self.moved
        return new_piece

    # Pareil pour toutes les pièces :  Vérifie si chaque coup est légal en prenant en comptes les autres pièces
    def liste_coups_legaux(self, grille: list, peut_capturer_allie=False):
        patterne = [(2, 0), (-2, 0), (+1, +0), (+1, +1), (+0, +1), (-1, +1), (-1, +0), (-1, -1), (+0, -1), (+1, -1)]
        move_legaux = []
        for i in range(len(patterne) - 1, -1, -1):
            if self.x + patterne[i][0] < 0 or self.x + patterne[i][0] > 7 or self.y + patterne[i][1] < 0 or self.y + \
                    patterne[i][1] > 7:
                patterne.pop(i)
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
                            if not grille[self.y][self.x - 3] and not grille[self.y][self.x - 2] and not grille[self.y][
                                self.x - 1]:
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

    # Pareil pour toutes les pièces: bouge la pièce à l'endroit donnée, si le mouvement est valide
    def move(self, x_added, y_added, grille: list):
        # vérifie si le coup est légal
        if (x_added, y_added) in self.liste_coups_legaux(grille):
            self.moved = True
            # cas spéciaux pour les rocs
            if (x_added, y_added) == (2, 0):
                # récupère la tour
                tour: Tour = grille[self.y + y_added][self.x + x_added + 1]
                # la bouge
                grille = tour.move(-2, 0, grille, True)
                # vide la case où nle roi était
                grille[self.y][self.x] = None
                self.x += x_added
                self.y += y_added
                # met à jour le plateau avec le roi à la nouvelle position
                grille[self.y][self.x] = self
                return grille
            if (x_added, y_added) == (-2, 0):
                # même commentaire que autre roc
                tour: Tour = grille[self.y + y_added][self.x + x_added - 2]
                grille = tour.move(3, 0, grille, True)
                grille[self.y][self.x] = None
                self.x += x_added
                self.y += y_added
                grille[self.y][self.x] = self
                return grille

            # coups qui ne sont pas le roc
            else:
                # Si une pièce est trouvée sur la nouvelle case, la capturée car grâce à liste_coups_legaux, une pièce trouvée ne peut que être de couleur opposée

                # voir commentaires des rocs
                grille[self.y][self.x] = None
                self.x += x_added
                self.y += y_added
                grille[self.y][self.x] = self
            return grille
        else:
            raise ValueError(
                f"Le coup({x_added}, {y_added}) n'est pas valide pour la pièce {self.type_de_piece} de couleur {self.couleur} au coordonnées {(self.x, self.y)}.")


class Pion(Piece):
    def __init__(self, couleur: str, x: int = 0, y: int = 0):
        super().__init__(couleur, "pion", x, y, 100)

    def copy(self):
        return Pion(self.couleur, self.x, self.y)

    def liste_coups_legaux(self, grille: list, peut_capturer_allie=False):
        if self.couleur == "blanc":
            patterne = []
            # verifie si une piece is devant le pion:
            if not grille[self.y - 1][self.x]:
                patterne.append((0, -1))
            # si le pion est sur la bonne ligne et pas de pièces devant, lui laisse avancé de 2 cases
            if self.y == 6 and not grille[4][self.x] and not grille[5][self.x]:
                patterne.append((0, -2))
        else:
            # pareil mais si le pion est noir
            patterne = []
            if not grille[self.y + 1][self.x]:
                patterne.append((0, +1))
            if self.y == 1 and not grille[3][self.x] and not grille[2][self.x]:
                patterne.append((0, +2))

        # ajoute les coups de captures s'il y a une pièce de couleur opposée en diagonal
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
            # Code mouvement basique
            self.moved = True

            grille[self.y][self.x] = None
            self.x += x_added
            self.y += y_added
            grille[self.y][self.x] = self
            # Code gérant la promotion en dame
            if (self.couleur == "blanc" and self.y == 0) or (self.couleur == "noir" and self.y == 7):
                return self.promote(grille)
            else:
                return grille
        else:
            raise ValueError(
                f"Le coup({x_added}, {y_added}) n'est pas valide pour la pièce {self.type_de_piece} de couleur {self.couleur} au coordonnées {(self.x, self.y)}.")

    # Fonction gérant la promotion du pion
    def promote(self, grille: list):
        new_piece = Dame(self.couleur)
        # Créer une nouvelle pièce (une dame) et remplace le pion par cette dame à qui on donne les bons attributs
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

    def liste_coups_legaux(self, grille: list, peut_capturer_allie=False):
        patterne = [(+2, +1), (+2, -1), (-2, +1), (-2, -1), (+1, +2), (+1, -2), (-1, +2), (-1, -2)]
        move_illegaux = []
        for coup in patterne:
            if self.x + coup[0] < 0 or self.x + coup[0] > 7 or self.y + coup[1] < 0 or self.y + coup[1] > 7:
                move_illegaux.append(coup)
                continue
            if grille[self.y + coup[1]][self.x + coup[0]]:
                if grille[self.y + coup[1]][self.x + coup[0]].couleur == self.couleur and not peut_capturer_allie:
                    move_illegaux.append(coup)
        for move in move_illegaux:
            patterne.remove(move)
        return patterne

    def move(self, x_added, y_added, grille: list):
        if (x_added, y_added) in self.liste_coups_legaux(grille):
            self.moved = True
            if grille[self.y + y_added][self.x + x_added]:
                if grille[self.y + y_added][self.x + x_added].couleur == self.couleur:
                    raise ValueError(
                        f"Le coup({x_added}, {y_added}) n'est pas valide pour la piéce {self.type_de_piece} de couleur {self.couleur} au coordonnées {(self.x, self.y)}.")
            grille[self.y][self.x] = None
            self.x += x_added
            self.y += y_added
            grille[self.y][self.x] = self
            return grille
        else:

            raise ValueError(
                f"Le coup({x_added}, {y_added}) n'est pas valide pour la pièce {self.type_de_piece} de couleur {self.couleur} au coordonnées {(self.x, self.y)}.")


class Tour(Piece):
    def __init__(self, couleur: str, x: int = 0, y: int = 0):
        super().__init__(couleur, "tour", x, y, 500)

    def copy(self):
        new_piece = Tour(self.couleur, self.x, self.y)

        return new_piece

    def liste_coups_legaux(self, grille: list, peut_capturer_allie=False):
        patterne = [(+1, +0), (-1, +0), (+0, +1), (+0, -1)]
        new_patterne = []
        for move in patterne:
            x = move[0]
            y = move[1]
            # Fait bouger la tour jusqu'à ce qu'elle atteigne une case non vide
            while True:
                # stop la boucle aussi si la pièce sortirait du plateau
                if x + self.x > 7 or x + self.x < 0 or y + self.y > 7 or y + self.y < 0:
                    break
                if not grille[self.y + y][self.x + x]:
                    new_patterne.append((x, y))
                else:
                    if not grille[self.y + y][self.x + x].couleur == self.couleur:
                        new_patterne.append((x, y))
                        break
                    elif peut_capturer_allie:
                        new_patterne.append((x, y))
                        break
                    else:
                        break
                # ajoute 1 aux directions pour que si la pièce n'a pas atteint une case non vide, elle essaye la prochaine case
                if x > 0:
                    x += 1
                if x < 0:
                    x -= 1
                if y > 0:
                    y += 1
                if y < 0:
                    y -= 1

        return new_patterne

    def move(self, x_added, y_added, grille: list, forced=False):
        # forced permet de forcer le mouvement de la tour car ce n'est utilisé que pour le roc, et le roc lui même vérifie les condtions nécessaires pour le mouvement
        if (x_added, y_added) in self.liste_coups_legaux(grille) or forced:
            self.moved = True

            grille[self.y][self.x] = None
            self.x += x_added
            self.y += y_added
            grille[self.y][self.x] = self
            return grille
        else:
            raise ValueError(
                f"Le coup({x_added}, {y_added}) n'est pas valide pour la pièce {self.type_de_piece} de couleur {self.couleur} au coordonnées {(self.x, self.y)}.")


class Dame(Piece):
    def __init__(self, couleur: str, x: int = 0, y: int = 0):
        super().__init__(couleur, "dame", x, y, 900)

    def copy(self):
        new_piece = Dame(self.couleur, self.x, self.y)
        return new_piece

    def liste_coups_legaux(self, grille: list, peut_capturer_allie=False):
        patterne = ((1, 1), (1, -1), (-1, -1), (-1, 1), (+1, +0), (-1, +0), (+0, +1), (+0, -1))
        new_patterne = []
        # répète les boucles pour les mouvements légaux de la tour et du fou
        for move in patterne:
            x = move[0]
            y = move[1]
            while True:
                if x + self.x > 7 or x + self.x < 0 or y + self.y > 7 or y + self.y < 0:
                    break
                if not grille[self.y + y][self.x + x]:
                    new_patterne.append((x, y))
                else:
                    if grille[self.y + y][self.x + x].couleur != self.couleur:
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

        # supprime les coups duppliqués avec list(set(new_patterne))
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
            raise ValueError(
                f"Le coup({x_added}, {y_added}) n'est pas valide pour la pièce {self.type_de_piece} de couleur {self.couleur} au coordonnées {(self.x, self.y)}.")


class Fou(Piece):
    def __init__(self, couleur: str, x: int = 0, y: int = 0):
        super().__init__(couleur, "fou", x, y, 320)

    def copy(self):
        new_piece = self.__class__(self.couleur, self.x, self.y)
        return new_piece

    def liste_coups_legaux(self, grille: list, peut_capturer_allie=False):
        patterne = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
        new_patterne = []
        for move in patterne:
            x = move[0]
            y = move[1]
            while True:
                if x + self.x > 7 or x + self.x < 0 or y + self.y > 7 or y + self.y < 0:
                    break
                if not grille[self.y + y][self.x + x]:
                    new_patterne.append((x, y))
                else:
                    if grille[self.y + y][self.x + x].couleur != self.couleur:
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

            raise ValueError(
                f"Le coup({x_added}, {y_added}) n'est pas valide pour la pièce {self.type_de_piece} de couleur {self.couleur} au coordonnées {(self.x, self.y)}.")


class Vegeta(Piece):
    def __init__(self, couleur: str, x: int = 0, y: int = 0):
        super().__init__(couleur, "vegeta", x, y, 900)
        self.promoted = False
        self.promoting = False

    def copy(self):
        new_piece = self.__class__(self.couleur, self.x, self.y)
        return new_piece

    def liste_coups_legaux(self, grille: list, peut_capturer_allie=False):
        if self.promoting:
            new_patterne = []
            for piece in chess_utils.liste_pieces_restantes(grille):
                if piece.type_de_piece != "roi":
                    new_patterne.append((piece.x, piece.y))
            return list(set(new_patterne))
        patterne = ((1, 1), (1, -1), (-1, -1), (-1, 1), (+1, +0), (-1, +0), (+0, +1), (+0, -1))
        new_patterne = []
        for move in patterne:
            x = move[0]
            y = move[1]
            while True:
                if x + self.x > 7 or x + self.x < 0 or y + self.y > 7 or y + self.y < 0:
                    break
                if not grille[self.y + y][self.x + x]:
                    new_patterne.append((x, y))
                else:
                    if grille[self.y + y][self.x + x].couleur != self.couleur:
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
        return new_patterne

    def move(self, x_added, y_added, grille: list):
        if (x_added, y_added) in self.liste_coups_legaux(grille) or self.promoting:
            self.moved = True
            if self.promoting:
                self.promoting = True

            grille[self.y][self.x] = None
            self.x += x_added
            self.y += y_added
            grille[self.y][self.x] = self
            if (self.couleur == "blanc" and self.y == 0) or (
                    self.couleur == "noir" and self.y == 7) and not self.promoted:
                self.promoted = True
                self.promoting = True
            return grille
        else:
            raise ValueError(
                f"Le coup({x_added}, {y_added}) n'est pas valide pour la pièce {self.type_de_piece} de couleur {self.couleur} au coordonnées {(self.x, self.y)}.")


def setup_custom_pieces():
    with open('custom_pieces.json', 'r') as config_file:
        config = json.load(config_file)
        for piece_info in config['pieces']:
            create_piece_class(piece_info)


def create_piece_class(piece_info):
    if len(piece_info["promotion"]) == 0:
        def init(self, couleur, x=0, y=0):
            super(self.__class__, self).__init__(couleur, piece_info['type_de_piece'], x, y, piece_info['valeur'])
            self.patterne = piece_info['patterne']
            self.promotable = False
    else:
        def init(self, couleur, x=0, y=0, promotable=False):
            super(self.__class__, self).__init__(couleur, piece_info['type_de_piece'], x, y, piece_info['valeur'])
            self.patterne = piece_info['patterne']
            self.promoted = False
            self.promotable = promotable

    mouvements = piece_info["mouvements"]
    if len(mouvements) == 1 and mouvements[0] == "etendu":
        liste_coups_legaux = coups_legaux_etendus
    elif len(mouvements) == 1 and mouvements[0] == "precis":
        liste_coups_legaux = coups_legaux_precis
    elif len(mouvements) == 2:
        if mouvements[0] == "etendu" and mouvements[1] == "precis":
            liste_coups_legaux = coups_legaux_etendu_precis
        elif mouvements[0] == "precis" and mouvements[1] == "etendu":
            liste_coups_legaux = coups_legaux_precis_etendu
        else:
            raise ValueError(f"Invalid double mouvements list for {piece_info['class_name']}, {mouvements}")
    else:
        raise ValueError(f"Invalid mouvements list for {piece_info['class_name']}")


    move = move_default
    if len(piece_info["abilite"]):
        if piece_info["abilite"][0] == "imposteur":
            move = move_imposteur
        if piece_info["abilite"][0] == "voleur":
            move = move_voleur
    else:
        print(piece_info["abilite"])
    if len(piece_info["promotion"]) > 0:
        promote = promote_to_queen
        if piece_info["promotion"][0] == "random_delete":
            promote = promote_random_delete
    if len(piece_info["promotion"]) == 0:
        def copy(self):
            new_piece = self.__class__(self.couleur, self.x, self.y)
            return new_piece
    else:
        def copy(self):
            new_piece = self.__class__(self.couleur, self.x, self.y, True)
            new_piece.promoted = self.promoted
            return new_piece

    if len(piece_info["promotion"]) == 0:
        new_class = type(
            piece_info['class_name'],
            (Piece,),
            {
                '__init__': init,
                'copy': copy,
                'liste_coups_legaux': liste_coups_legaux,
                'move': move,
            }
        )
    else:
        new_class = type(
            piece_info['class_name'],
            (Piece,),
            {
                '__init__': init,
                'copy': copy,
                'liste_coups_legaux': liste_coups_legaux,
                'move': move,
                'promote': promote,
            }
        )
    globals()[piece_info['class_name']] = new_class  # Make the class globally accessible


def coups_legaux_etendu_precis(self, grille: list, peut_capturer_allie=False):
    patterne = self.patterne
    new_patterne = []
    for move in patterne[0]:
        x = move[0]
        y = move[1]
        while True:
            if x + self.x > 7 or x + self.x < 0 or y + self.y > 7 or y + self.y < 0:
                break
            if not grille[self.y + y][self.x + x]:
                new_patterne.append((x, y))
            else:
                if grille[self.y + y][self.x + x].couleur != self.couleur:
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

    move_illegaux = []
    for coup in patterne[1]:
        if self.x + coup[0] < 0 or self.x + coup[0] > 7 or self.y + coup[1] < 0 or self.y + coup[1] > 7:
            move_illegaux.append(coup)
            continue
        if grille[self.y + coup[1]][self.x + coup[0]]:
            if grille[self.y + coup[1]][self.x + coup[0]].couleur == self.couleur and not peut_capturer_allie:
                move_illegaux.append(coup)
    new_patterne.extend([coup for coup in patterne[1] if coup not in move_illegaux])
    new_patterne = [tuple(item) if isinstance(item, list) else item for item in new_patterne]
    return new_patterne


def coups_legaux_precis_etendu(self, grille: list, peut_capturer_allie=False):
    patterne = self.patterne
    new_patterne = []
    for move in patterne[1]:
        x = move[0]
        y = move[1]
        while True:
            if x + self.x > 7 or x + self.x < 0 or y + self.y > 7 or y + self.y < 0:

                break
            if not grille[self.y + y][self.x + x]:
                new_patterne.append((x, y))
            else:
                if grille[self.y + y][self.x + x].couleur != self.couleur:
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

    move_illegaux = []
    for coup in patterne[0]:
        if self.x + coup[0] < 0 or self.x + coup[0] > 7 or self.y + coup[1] < 0 or self.y + coup[1] > 7:
            move_illegaux.append(coup)
            continue
        if grille[self.y + coup[1]][self.x + coup[0]]:
            if grille[self.y + coup[1]][self.x + coup[0]].couleur == self.couleur and not peut_capturer_allie:
                move_illegaux.append(coup)
    new_patterne.extend([coup for coup in patterne[0] if coup not in move_illegaux])
    new_patterne = [tuple(item) if isinstance(item, list) else item for item in new_patterne]

    return new_patterne


def coups_legaux_precis(self, grille: list, peut_capturer_allie=False):
    patterne = self.patterne[0]
    move_illegaux = []
    for coup in patterne:
        if self.x + coup[0] < 0 or self.x + coup[0] > 7 or self.y + coup[1] < 0 or self.y + coup[1] > 7:
            move_illegaux.append(coup)
            continue
        if grille[self.y + coup[1]][self.x + coup[0]]:
            if grille[self.y + coup[1]][self.x + coup[0]].couleur == self.couleur and not peut_capturer_allie:
                move_illegaux.append(coup)
    new_patterne = [coup for coup in patterne if coup not in move_illegaux]
    new_patterne = [tuple(item) if isinstance(item, list) else item for item in new_patterne]

    return new_patterne


def coups_legaux_etendus(self, grille: list, peut_capturer_allie=False):
    # add all the lists of self.patterne into one big list
    patterne = []
    for pattern in self.patterne:
        patterne.extend(pattern)
    new_patterne = []
    # répète les boucles pour les mouvements légaux de la tour et du fou
    for move in patterne:
        x = move[0]
        y = move[1]
        while True:
            if x + self.x > 7 or x + self.x < 0 or y + self.y > 7 or y + self.y < 0:
                break
            if not grille[self.y + y][self.x + x]:
                new_patterne.append((x, y))
            else:
                if grille[self.y + y][self.x + x].couleur != self.couleur:
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
    new_patterne = [tuple(item) if isinstance(item, list) else item for item in new_patterne]

    # supprime les coups duppliqués avec list(set(new_patterne))
    return new_patterne
def move_default(self, x_added, y_added, grille: list):
    if (x_added, y_added) in self.liste_coups_legaux(grille):
        self.moved = True
        grille[self.y][self.x] = None
        self.x += x_added
        self.y += y_added
        grille[self.y][self.x] = self
        if self.promotable and ((self.couleur == "blanc" and self.y == 0) or (
                self.couleur == "noir" and self.y == 7) and not self.promoted):
            self.promoted = True
            return self.promote(grille)
        else:
            return grille
    else:
        raise ValueError(
            f"Le coup({x_added}, {y_added}) n'est pas valide pour la pièce {self.type_de_piece} de couleur {self.couleur} au coordonnées {(self.x, self.y)}.")

def move_imposteur(self, x_added, y_added, grille: list):
    if (x_added, y_added) in self.liste_coups_legaux(grille) or self.promoting:
        # Code mouvement basique
        self.moved = True

        grille[self.y][self.x] = None
        self.x += x_added
        self.y += y_added
        is_imposteur = random.randint(1, 100)
        if is_imposteur <= 25:
            print("changed color")
            self.couleur = chess_utils.couleur_oppose(self.couleur)
        grille[self.y][self.x] = self
        if self.promotable and ((self.couleur == "blanc" and self.y == 0) or (
                self.couleur == "noir" and self.y == 7) and not self.promoted):
            self.promoted = True
            return self.promote(grille)
        else:
            return grille
    else:
        raise ValueError(
            f"Le coup({x_added}, {y_added}) n'est pas valide pour la pièce {self.type_de_piece} de couleur {self.couleur} au coordonnées {(self.x, self.y)}.")

def move_voleur(self, x_added, y_added, grille: list):
    if (x_added, y_added) in self.liste_coups_legaux(grille):
        self.moved = True
        if grille[self.y + y_added][self.x + x_added]:
            enemi_piece: Roi = grille[self.y + y_added][self.x + x_added]
            enemi_piece.couleur = self.couleur
            grille[self.y + y_added][self.x + x_added] = enemi_piece
        else:
            grille[self.y][self.x] = None
            self.x += x_added
            self.y += y_added
            grille[self.y][self.x] = self

        if self.promotable and ((self.couleur == "blanc" and self.y == 0) or (
                self.couleur == "noir" and self.y == 7) and not self.promoted):
            self.promoted = True
            return self.promote(grille)
        else:
            return grille
    else:
        raise ValueError(
            f"Le coup({x_added}, {y_added}) n'est pas valide pour la pièce {self.type_de_piece} de couleur {self.couleur} au coordonnées {(self.x, self.y)}.")
def promote_to_queen(self, grille: list):
    new_piece = Dame(self.couleur)
    # Créer une nouvelle pièce (une dame) et remplace le pion par cette dame à qui on donne les bons attributs
    grille[self.y][self.x] = new_piece
    new_piece.x = self.x
    new_piece.y = self.y
    new_piece.moved = True
    return grille


def promote_random_delete(self, n_grille: list):
    pieces_enemies = chess_utils.liste_pieces_bougeables(n_grille, chess_utils.couleur_oppose(self.couleur))
    piece_a_capturer = random.choice(pieces_enemies)
    n_grille[piece_a_capturer.y][piece_a_capturer.x] = None
    return n_grille




setup_custom_pieces()