def get_piece(grille: list, x:int, y:int):
    """
    @type piece: lysandre.pieces.piece.Piece
    """
    if grille[y][x]:
        piece = grille[y][x]
        return piece
    else:
        return None

def get_piece_type(grille: list, x:int, y:int):
    """
    @type piece: lysandre.pieces.piece.Piece
    """
    if grille[y][x]:
        return grille[y][x].type_de_piece
    else:
        return None