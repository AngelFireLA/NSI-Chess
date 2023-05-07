#classe de base qui sera héritée par toute les pièces
import chess_utils


def type_valide(type_de_piece) -> bool:
    if not (type == "pion", type == "tour", type == "cavalier", type == "fou", type == "dame", type == "roi"):
        return False
    else:
        return True

p_id = 0
def get_last_piece_id():
    return p_id


def set_last_piece_id(new_p_id):
    p_id = new_p_id


class Piece():
    def __init__(self, couleur: str, capturee: bool==False, type_de_piece:str, x:int, y:int):
        self.id = get_last_piece_id()+1
        set_last_piece_id(get_last_piece_id()+1)
        #couleur de la pièce
        if couleur.lower() == "blanc" or couleur.lower() == "noir":
            self.couleur = couleur
        else:
            print("Une pièce a été définie avec une couleur invalide.")

        #position de la pièce sur la grille de 8x8
        self.x, self.y = x, y

        #Piece est capturée ou pas
        self.capturee = capturee

        #le type de la pièce
        if not type_valide(type_de_piece):
            print("Une pièce a été définie avec un type invalide.")
        else:
            self.type_de_piece = type_de_piece

        #vérifie si la pièce a déja bougée
        self.moved = False

    def set_type(self, type_de_piece):
        self.type_de_piece = type_de_piece

    def set_color(self, couleur):
        self.couleur = couleur

    #todo: enlever si inutile
    def est_capturee(self) -> bool:
        return self.capturee


class Roi(Piece):
    def __init__(self, couleur: str, capturee: bool=False, x:int=0, y:int=0):
        super().__init__(couleur, capturee, "roi", x, y)

    def get_patterne_possible(self, x, y):
        patterne = [(+1, +0), (+1, +1), (+0, +1), (-1, +1), (-1, +0), (-1, -1), (+0, -1), (+1, -1)]
        #check if piece doesn't go outside the grid
        for i in range(len(patterne) - 1, -1, -1):
            if x + patterne[i][0] < 0 or x + patterne[i][0] > 7 or y + patterne[i][1] < 0 or y + \
                    patterne[i][1] > 7:
                patterne.pop(i)
        return patterne

    def liste_coups_legaux(self, grille: list):
        #vérifie s'il y a le roi ennemi autour de chaque case possible,
        # si oui enlever cette case de la liste des cases possible:
        patterne = self.get_patterne_possible(self.x, self.y)
        print()
        move_illegaux = []
        for move in patterne:
            test_x, test_y = self.x+ move[0], self.y+ move[1]
            for intra_move in self.get_patterne_possible(test_x, test_y):
                piece_trouvee = chess_utils.get_piece_type(grille, test_x + intra_move[0], test_y + intra_move[1])
                if piece_trouvee:
                    if  chess_utils.get_piece_type(grille, test_x + intra_move[0], test_y + intra_move[1]) == "roi" and chess_utils.get_piece(grille, test_x + intra_move[0], test_y + intra_move[1]).couleur != self.couleur:
                        move_illegaux.append(move)
        for move in move_illegaux:
            patterne.remove(move)
        print(patterne)

    def move(self):
        pass

class Pion(Piece):
    def __init__(self, couleur: str, capturee: bool=False, x:int=0, y:int=0):
        super().__init__(couleur, capturee, "pion", x, y)
        if self.y == 7 or self.y == 0:
            self.promotable = True

    def get_patterne_possible(self, grille: list):
        if self.couleur == "blanc":
            patterne = []
            #verifie si une piece is devant le pion:
            if grille[self.y-1][self.x]:
                #todo : vérifier s'il peut pas en passant
                return patterne
            if self.y == 1:
                 patterne.append((+2, +0))
            # todo : vérifier s'il peut pas en passant
            patterne.append((+1, +0))
            return patterne
        else:
            patterne = []
            #vérifie s'il y a une pièce devant le pion:
            if grille[self.y+1][self.x]:
                #todo : vérifier s'il peut pas en passant
                return patterne
            if self.y == 6:
                 patterne.append((-2, +0))
            # todo : vérifier s'il peut pas en passant
            patterne.append((-1, +0))
            return patterne

    def liste_coups_legaux(self, grille: list):
        patterne = self.get_patterne_possible(grille)
        if self.couleur == "blanc":
            if grille[self.y-1][self.x-1]:
                patterne.append(-1, -1)
            if grille[self.y-1][self.x+1]:
                patterne.append(1, -1)
        else:
            if grille[self.y + 1][self.x - 1]:
                patterne.append(-1, +1)
            if grille[self.y + 1][self.x + 1]:
                patterne.append(1, +1)
        return patterne

    def move(self):
        pass

class Cavalier(Piece):
    def __init__(self, couleur: str, capturee: bool=False, x:int=0, y:int=0):
        super().__init__(couleur, capturee, "cavalier", x, y)

    def get_patterne_possible(self):
        patterne = [(+2, +1), (+2, -1), (-2, +1), (-2, -1), (+1, +2), (+1, -2), (-1, +2), (-1, -2)]
        # check if piece doesn't go outside the grid
        for i in range(len(patterne) - 1, -1, -1):
            if self.x + patterne[i][0] < 0 or self.x + patterne[i][0] > 7 or self.y + patterne[i][1] < 0 or self.y + \
                    patterne[i][1] > 7:
                patterne.pop(i)
        return patterne

    def liste_coups_legaux(self, grille: list):
        return self.get_patterne_possible()

    def move(self):
        pass

class Tour(Piece):
    def __init__(self, couleur: str, capturee: bool=False, x:int=0, y:int=0):
        super().__init__(couleur, capturee, "tour", x, y)

    def get_patterne_possible(self):
        patterne = [(+1, +0), (-1, +0), (+0, +1), (+0, -1)]
        # check if piece doesn't go outside the grid
        for i in range(len(patterne) - 1, -1, -1):
            if self.x + patterne[i][0] < 0 or self.x + patterne[i][0] > 7 or self.y + patterne[i][1] < 0 or self.y + \
                    patterne[i][1] > 7:
                patterne.pop(i)
        return patterne

    def liste_coups_legaux(self, grille: list):
        patterne = self.get_patterne_possible()
        n_patterne = []
        for move in patterne:
            x=move[0]
            y=move[1]
            #make rook move in direction until it goes on a square that isn't None
            while True:
                if not chess_utils.get_piece(grille, self.x + x, self.y + y):
                    n_patterne.append((x, y))
                else:
                    if chess_utils.get_piece(grille, self.x+x, self.y+y).couleur != self.couleur:
                        n_patterne.append((x, y))
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
                if x+self.x > 7 or x+self.x < 0 or y+self.y > 7 or y+self.y < 0:
                    break
        return n_patterne



    def move(self):
        pass

class Dame(Piece):
    def __init__(self, couleur: str, capturee: bool=False, x:int=0, y:int=0):
        super().__init__(couleur, capturee, "dame", x, y)

    def get_patterne_possible(self):
        patterne_diagonale = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (1, -1), (2, -2), (3, -3), (4, -4), (5, -5), (6, -6), (7, -7), (-1, -1), (-2, -2), (-3, -3), (-4, -4), (-5, -5), (-6, -6), (-7, -7), (-1, 1), (-2, 2), (-3, 3), (-4, 4), (-5, 5), (-6, 6), (-7, 7)]
        patterne_tour = [(+1, +0), (-1, +0), (+0, +1), (+0, -1)]
        for i in range(len(patterne_diagonale) - 1, -1, -1):
            if self.x + patterne_diagonale[i][0] < 0 or self.x + patterne_diagonale[i][0] > 7 or self.y + patterne_diagonale[i][1] < 0 or self.y + patterne_diagonale[i][1] > 7:
                patterne_diagonale.pop(i)
        for i in range(len(patterne_tour) - 1, -1, -1):
            if self.x + patterne_tour[i][0] < 0 or self.x + patterne_tour[i][0] > 7 or self.y + patterne_tour[i][1] < 0 or self.y + patterne_tour[i][1] > 7:
                patterne_tour.pop(i)
        return patterne_diagonale, patterne_tour

    def liste_coups_legaux(self, grille: list):
        patterne = self.get_patterne_possible()
        n_patterne = []
        for move in patterne[0]:
            x = move[0]
            y = move[1]
            while True:
                if not chess_utils.get_piece(grille, self.x + x, self.y + y):
                    n_patterne.append((x, y))
                else:
                    if chess_utils.get_piece(grille, self.x + x, self.y + y).couleur != self.couleur:
                        n_patterne.append((x, y))
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
                    n_patterne.append((x, y))
                else:
                    if chess_utils.get_piece(grille, self.x + x, self.y + y).couleur != self.couleur:
                        n_patterne.append((x, y))
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
        return list(set(n_patterne))

    def move(self):
        pass

class Fou(Piece):
    def __init__(self, couleur: str, capturee: bool=False, x:int=0, y:int=0):
        super().__init__(couleur, capturee, "fou", x, y)

    def get_patterne_possible(self):
        patterne = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (1, -1), (2, -2), (3, -3), (4, -4), (5, -5), (6, -6), (7, -7), (-1, -1), (-2, -2), (-3, -3), (-4, -4), (-5, -5), (-6, -6), (-7, -7), (-1, 1), (-2, 2), (-3, 3), (-4, 4), (-5, 5), (-6, 6), (-7, 7)]
        # check if piece doesn't go outside the grid
        for i in range(len(patterne) - 1, -1, -1):
            if self.x + patterne[i][0] < 0 or self.x + patterne[i][0] > 7 or self.y + patterne[i][1] < 0 or self.y + \
                    patterne[i][1] > 7:
                patterne.pop(i)
        return patterne

    def liste_coups_legaux(self, grille: list):
        pass

    def move(self):
        pass