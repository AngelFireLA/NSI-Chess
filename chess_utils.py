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



