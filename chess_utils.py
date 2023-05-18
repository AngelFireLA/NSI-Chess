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

def get_couleur_str(couleur:int):
    couleur_str = None
    if couleur == 1:
        couleur_str = "blanc"
    elif couleur ==-1:
        couleur_str = "noir"
    return couleur_str

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


def liste_coups_legaux(couleur, grille, peux_capturer_allier=False):
    pieces = liste_pieces_bougeables(grille, couleur)
    if peux_capturer_allier:
        coups = [
            (piece, coup) for piece in pieces for coup in piece.liste_coups_legaux(grille, peut_capturer_allie=True)
        ]
    else:
        coups = [
            (piece, coup) for piece in pieces for coup in piece.liste_coups_legaux(grille)
        ]
    return coups

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

def check_si_echec_et_mat(grille):
    for i in range(-1,2,2):

        couleur_str = get_couleur_str(i)
        oppose_str = get_couleur_str(-i)
        coups_rois = [(piece, move) for piece, move in liste_coups_legaux(couleur_str, grille) if piece.type_de_piece == "roi"]
        coups_rois = list(set(coups_rois))
        coups_legaux_opposes = liste_coups_legaux(oppose_str, grille)
        for piece, move in coups_legaux_opposes:  # Iterate over a copy of capturable list to safely remove elements
            attacked_pos = (piece.x + move[0], piece.y + move[1])
            for ally_piece, ally_move in coups_rois[:]:
                if attacked_pos == (ally_piece.x + ally_move[0], ally_piece.y + ally_move[1]):
                    coups_rois.remove((ally_piece, ally_move))
                    break
        if len(coups_rois) == 0:
            return oppose_str
    return None

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


def possible_captures_ou_promotions(couleur:str, grille):
    all_legal_moves = liste_coups_legaux(couleur, grille)
    return [
        (piece, move) for piece, move in all_legal_moves
        if not points_avec_roi(grille) == points_avec_roi(
            copy.deepcopy(piece).move(move[0], move[1], copy.deepcopy(grille))
        )
    ]

def liste_pieces_en_capture(grille, couleur:int):
    couleur_str = get_couleur_str(-couleur)
    nos_coups = liste_coups_legaux(couleur_str, grille, peux_capturer_allier=True)
    capturable = [(piece,move) for piece, move in possible_captures_ou_promotions(couleur_str, grille)]
    for piece, move in capturable[:]:  # Iterate over a copy of capturable list to safely remove elements
        if piece.type_de_piece != 'pion':
            attacked_pos = (piece.x + move[0], piece.y + move[1])
            for ally_piece, ally_move in nos_coups:
                if attacked_pos in (ally_piece.x + ally_move[0], ally_piece.y + ally_move[1]):
                    capturable.remove((piece, move))
                    break
    return capturable





