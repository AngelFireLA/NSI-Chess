
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

#Pareille mais retourne le type de la pièce à la place s'il y en a une
def get_piece_type(grille: list, x:int, y:int):
    """
    @type piece: lysandre.pieces.piece.Piece
    """
    if grille[y][x]:
        return grille[y][x].type_de_piece
    else:
        return None

def get_couleur_str(couleur: int) -> str:
    return {1: "blanc", -1: "noir"}.get(couleur)

def get_couleur_int(couleur: str) -> int:
    return {"blanc": 1, "noir": -1}.get(couleur)

#Récupérer la liste de pièces bougeables pour un camp dans une position
def liste_pieces_bougeables(grille, couleur: str) -> list:
    return [
        j for i in grille for j in i if j and j.couleur == couleur
    ]

def liste_pieces_restantes(grille) -> list:
    return [
        j for i in grille for j in i if j
    ]

def nb_pieces_restantes(grille) -> int:
    return len([
        j for i in grille for j in i if j
    ])

#Récupère toutes les pièces autour d'une piéce donnée dans un rayon donné
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

#Récupère toutes les pièces et récupèrent chacun tous les coups possibles
def liste_coups_legaux(couleur, grille):
    pieces = liste_pieces_bougeables(grille, couleur)
    return [
            (piece, coup) for piece in pieces for coup in piece.liste_coups_legaux(grille)
        ]

#Fonction qui détermine si un camp n'a plus de roi
def check_si_roi_restant(grille):
    is_king = {"blanc": False, "noir": False}
    for row in grille:
        for piece in row:
            if piece and piece.type_de_piece == "roi":
                is_king[piece.couleur] = True

    if not is_king["blanc"]:
        return "noir"
    elif not is_king["noir"]:
        return "blanc"

    return False

#Montre la grille visuellement plus jolie mais toujours textuelle
def montrer_grille(grille):
    grid = [[],[],[],[],[],[],[],[]]
    for i in grille:
        ligne = []
        for j in i:
            if j:
                ligne.append(f"{j.couleur[0]}_{j.type_de_piece}")
                grid[grille.index(i)].append(f"{j.couleur[0]}_{j.type_de_piece}")
            else:
                ligne.append(None)
                grid[grille.index(i)].append(None)
        print(ligne)
    return grid

#Vérifie s'il ne reste que des rois sur le plateau, donc si c'est égalité
def roi_contre_roi(grille) -> bool:
    type_de_pieces_restantes = {"blanc":{"fou": 0, "cavalier": 0, "roi": 0, "dame": 0, "pion": 0, "tour": 0}, "noir":{"fou": 0, "cavalier": 0, "roi":0, "dame": 0, "pion": 0, "tour": 0}}
    for i in grille:
        for j in i:
            if j:
                type_de_pieces_restantes[j.couleur][j.type_de_piece]+=1

    if insufficient_material(type_de_pieces_restantes):
        return True


def insufficient_material(type_de_pieces_restantes):
    blanc = type_de_pieces_restantes["blanc"]
    noir = type_de_pieces_restantes["noir"]

    # Check if there are any pawns, queens, or rooks on the board
    for color in [blanc, noir]:
        if color["pion"] > 0 or color["dame"] > 0 or color["tour"] > 0:
            return False

    # Check for lone king
    if (blanc["roi"] == 1 and sum(blanc.values()) == 1) and (noir["roi"] == 1 and sum(noir.values()) == 1):
        return True

    # Check for king and bishop, or king and knight
    if (blanc["roi"] == 1 and blanc["fou"] == 1 and sum(blanc.values()) == 2) and (
            noir["roi"] == 1 and sum(noir.values()) == 1):
        return True
    if (blanc["roi"] == 1 and blanc["cavalier"] == 1 and sum(blanc.values()) == 2) and (
            noir["roi"] == 1 and sum(noir.values()) == 1):
        return True

    # swap colors and repeat checks
    if (noir["roi"] == 1 and noir["fou"] == 1 and sum(noir.values()) == 2) and (
            blanc["roi"] == 1 and sum(blanc.values()) == 1):
        return True
    if (noir["roi"] == 1 and noir["cavalier"] == 1 and sum(noir.values()) == 2) and (
            blanc["roi"] == 1 and sum(blanc.values()) == 1):
        return True

    # Check for king and two knights
    if (blanc["roi"] == 1 and blanc["cavalier"] == 2 and sum(blanc.values()) == 3) and (
            noir["roi"] == 1 and sum(noir.values()) == 1):
        return True
    if (noir["roi"] == 1 and noir["cavalier"] == 2 and sum(noir.values()) == 3) and (
            blanc["roi"] == 1 and sum(blanc.values()) == 1):
        return True

    return False

#Fonctions qui comptent les points de chaque camp sans compter les rois
def points(grille):
    points_blanc = sum([j.valeur for i in grille for j in i if j and j.type_de_piece != "roi" and j.couleur == "blanc"])
    points_noir = sum([j.valeur for i in grille for j in i if j and j.type_de_piece != "roi" and j.couleur == "noir"])
    return points_blanc, points_noir

#Fonctions qui comptent les points de chaque camp en comptant les rois
def points_avec_roi(grille):
    pointss = {'blanc': 0, 'noir': 0}

    for row in grille:
        for cell in row:
            if cell:
                pointss[cell.couleur] += cell.valeur

    return pointss['blanc'], pointss['noir']

#Récupère toutes les captures ou promotions possibles pour un camp dans une position donnée
def possible_captures_ou_promotions(couleur: str, grille):
    all_legal_moves = liste_coups_legaux(couleur, grille)
    captures = []
    for (piece, move) in all_legal_moves:
        j = grille[piece.y + move[1]][piece.x + move[0]]
        if j and j.couleur != piece.couleur:
            captures.append((piece, move))
    return captures




#Récupérer toutes les pièces qui sont menacée d'un camp spécifique
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

def couleur_oppose(couleur:str):
    if  couleur == "blanc":
        return "noir"
    elif couleur == "noir":
        return "blanc"
    elif couleur == 1:
        return -1
    elif couleur == -1:
        return 1
    else:
        return None





