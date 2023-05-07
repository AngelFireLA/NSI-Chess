from lysandre import plateau
from lysandre.pieces.piece import Piece

pion1 = Piece("blanc", False, "pion", 1, 3)

plateau = plateau.Plateau()
plateau.init_grille([])
print('[')
plateau.montrer_grille()
print(']', end='')




