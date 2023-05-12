import chess_utils
from engine.pieces.piece import Roi, Tour, Fou, Cavalier, Dame, Pion, Piece
from engine.plateau import Plateau
import bots.negamax as negamax

class Partie():
    def __init__(self, type_de_partie: str = "normale", tour="blanc", points_blanc=0, points_noir=1):
        #setup pour voir si le plateau a été défini
        self.setup = False
        self.points_blanc = 0
        self.points_noir = 0
        self.terminee = False
        #tour dans "a qui le tour" et pas la pièce
        self.tour = tour
        self.type_de_partie = type_de_partie
        #type_de_partie au cas où qu'on fait des modes de jeux customs
        if self.type_de_partie == "normale":
            self.plateau = Plateau()

    #Met en place le tableau à partir d'un string FEN qui est un texte qui dit quel pièce va a quelle place,
    # on peut le générer pour n'importe quel position, facielement en ligne
    #même moi je me souviens plus comment le code marche car il est compliqué
    def setup_from_fen(self, fen: str):
        grille = []
        rank_strings = fen.split('/')
        for rank_index, rank_string in enumerate(rank_strings):
            ligne = []
            file_index = 0
            y = rank_index
            for symbol in rank_string:
                if symbol.isdigit():
                    empty_fields = int(symbol)
                    for _ in range(empty_fields):
                        ligne.append(None)
                    file_index += empty_fields
                else:
                    piece_class, couleur = self.piece_from_symbol(symbol)
                    piece = piece_class(x=file_index, y=y, couleur=couleur)
                    ligne.append(piece)
                    file_index += 1
            grille.append(ligne)
        self.plateau = Plateau(grille)
        self.setup = True

    #Dans un string fen, chaque lettre veut dire une pièce, ici on définit quelle lettre dans le string FEN correspond à quelle pièce, agrandissable pour des pièces customs
    def piece_from_symbol(self, symbol: str):
        symbol_piece_dict = {
            'K': (Roi, "blanc"), 'Q': (Dame, "blanc"), 'R': (Tour, "blanc"), 'B': (Fou, "blanc"),
            'N': (Cavalier, "blanc"), 'P': (Pion, "blanc"),
            'k': (Roi, "noir"), 'q': (Dame, "noir"), 'r': (Tour, "noir"), 'b': (Fou, "noir"),
            'n': (Cavalier, "noir"), 'p': (Pion, "noir")
        }
        return symbol_piece_dict[symbol]

    #Boucle qui gère le début jusqu'à la fin d'une partie
    def run(self):
        if self.setup:
            if self.type_de_partie == "normale":
                self.plateau.montrer_grille()
                #Boucle qui laisse les joueurs jouer tant que la partie n'est pas terminée
                while not self.terminee:
                    if self.tour == "blanc":
                        negamax.init(self.plateau, self.points_blanc, self.points_noir)
                        negamax.make_move(self.plateau, 1, self)
                        self.tour = "noir"
                    inp_piece = input("Sélectionner une pièce :")
                    #q pour "quitter"
                    if inp_piece == "q":
                        self.terminee = True
                        break
                    #p pour "points"
                    if inp_piece == "p":
                        print(self.points_blanc, self.points_noir)
                        continue
                    #Récupère le contenu de la case aux corrdonées données
                    piece_selectionner: Piece = chess_utils.get_piece(p.plateau.get_grille(),
                                                                      int(inp_piece.split(',')[0]),
                                                                      int(inp_piece.split(',')[1]))
                    #Si le joueur à sélectionner une case vide, ça recommence la boucle sans continuer pour que le joueur puisse entrer de nouvelles coordonnées
                    if not piece_selectionner:
                        print("Erreur, la case sélectionnée est vide.")
                        continue
                    #Si le joueur à sélectionner une pièce de son adversaire à jouer, ça recommence la boucle sans continuer pour que le joueur puisse entrer de nouvelles coordonnées
                    if piece_selectionner.couleur != self.tour:
                        print("Cette pièce n'est pas votre")
                        continue
                    print(f"Vous avez sélectionné {piece_selectionner.type_de_piece}")
                    print(
                        f"Voici la liste de coups possible : {piece_selectionner.liste_coups_legaux(p.plateau.get_grille())}")
                    inp_coup = input("Sélectionner le coup choisi :")
                    #r pour recommencer, si on ne veut plus jouer cette pièce
                    if inp_coup == "r":
                        continue
                    coup = piece_selectionner.move(int(inp_coup.split(',')[0]), int(inp_coup.split(',')[1]),
                                                   self.plateau.get_grille(), self)
                    #boucle qui s'active que si le coup envoyé par le joueur n'est pas dans la liste des coups possibles, et donc redemande un coup au joueur,
                    #jusqu'à ce qu'il envoie un coup valide
                    while not coup:
                        inp_coup = input("Sélectionner nouvelle coordonnées :")
                        coup = piece_selectionner.move(int(inp_coup.split(',')[0]), int(inp_coup.split(',')[1]),
                                                       self.plateau.get_grille(), self)
                        print(coup)
                    print(f"Vous avez jouer {inp_coup}")
                    #Met à jour le plateau après le mouvement
                    self.plateau.set_grille(coup)
                    self.plateau.montrer_grille()
                    #change le tour
                    if self.tour == "blanc":
                        self.tour = "noir"
                    else:
                        self.tour = "blanc"
                    #s'il ne reste pas au moins un roi de chaque couleur, ça termine la partie
                    #if self.plateau.check_si_roi_restant():
                    #    print(f"Partie terminée! Les vainqueurs sont les {self.plateau.check_si_roi_restant()}")
                    #    self.terminee = True+

                    if self.plateau.roi_contre_roi():
                        print("Egalité ! Il ne reste que des rois sur le plateau.")
                        self.terminee = True
        else:
            print("Erreur, vous n'avez pas setup la position initiale")

#Partie exemple
p = Partie()
p.setup_from_fen("k7/2q5/3P4/8/8/8/8/K7")
p.run()
