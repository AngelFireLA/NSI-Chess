#classe de base qui sera héritée par toute les pièces
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

    def est_capturee(self) -> bool:
        return self.capturee

    #def move(self, x, y):
