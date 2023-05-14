import copy
#Récupère la pièece, ou si la case vide, à une case donnée d'une grille donnée
def get_piece(grille: list, x:int, y:int):
    """
    @type piece: lysandre.pieces.piece.Piece
    """
    if grille[y][x]:
        piece = grille[y][x]
        return piece
    else:
        return None

#Pareille que celle d'en haut sauf que ça retourne le type de la pièce s'il y en a une
def get_piece_type(grille: list, x:int, y:int):
    """
    @type piece: lysandre.pieces.piece.Piece
    """
    if grille[y][x]:
        return grille[y][x].type_de_piece
    else:
        return None


def liste_pieces_bougeables(grille, couleur: str) -> list:
    return [
        j for i in grille for j in i if j and j.couleur == couleur
    ]


def liste_pieces_dans_rayon(grille, x: int, y: int, rayon: int) -> list:
    debut_ligne = max(y - rayon, 0)
    fin_ligne = min(y + rayon + 1, len(grille))
    debut_colonne = max(x - rayon, 0)
    fin_colonne = min(x + rayon + 1, len(grille[0]))

    sub_grille = [grille[i][debut_colonne:fin_colonne] for i in range(debut_ligne, fin_ligne)]
    liste = [
        j for i in sub_grille for j in i
    ]
    liste = [elem for elem in liste if elem and not (elem.x, elem.y) == (x, y)]
    return liste


def liste_coups_legaux(couleur, grille):
    pieces = liste_pieces_bougeables(grille, couleur)
    return [
        (piece, coup) for piece in pieces for coup in piece.liste_coups_legaux(grille)
    ]

def check_si_roi_restant(grille):
    compteur_de_roi = {"blanc":0, "noir":0}
    for i in grille:
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

def montrer_grille(grille):
    for i in grille:
        ligne = []
        for j in i:
            if j:
                ligne.append(j.type_de_piece)
            else:
                ligne.append(None)
        print(ligne)

def roi_contre_roi(grille) -> bool:
    pieces_restantes = []
    for i in grille:
        for j in i:
            if j:
                pieces_restantes.append(j)
    for piece in pieces_restantes:
        if not piece.type_de_piece == "roi":
            return False
    return True

def points(grille):
    points_blanc = sum([j.valeur for i in grille for j in i if j and j.type_de_piece != "roi" and j.couleur == "blanc"])
    points_noir = sum([j.valeur for i in grille for j in i if j and j.type_de_piece != "roi" and j.couleur == "noir"])
    return points_blanc, points_noir

def points_avec_roi(grille):
    points_blanc = sum([j.valeur for i in grille for j in i if j and j.couleur == "blanc"])
    points_noir = sum([j.valeur for i in grille for j in i if j and j.couleur == "noir"])
    return points_blanc, points_noir


def possible_captures_ou_promotions(couleur, grille):
    all_legal_moves = liste_coups_legaux(couleur, grille)
    return [
        (copy.deepcopy(piece), move) for piece, move in all_legal_moves
        if not points_avec_roi(grille) == points_avec_roi(
            copy.deepcopy(piece).move(move[0], move[1], copy.deepcopy(grille))
        )
    ]




