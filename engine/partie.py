import chess_utils
from engine.pieces.piece import Roi, Tour, Fou, Cavalier, Dame, Pion, Piece
import bots.negamax as negamax
import time

class Partie():
    def __init__(self, type_de_partie: str = "normale", tour="blanc", points_blanc=0, points_noir=1, mode="manuel"):
        #setup pour voir si le plateau a été défini
        self.setup = False
        self.points_blanc = 0
        self.points_noir = 0
        self.terminee = False
        #tour dans "a qui le tour" et pas la pièce
        self.tour = tour
        self.type_de_partie = type_de_partie
        self.grille = None
        self.mode = mode

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
        self.grille = grille
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
                chess_utils.montrer_grille(self.grille)
                #Boucle qui laisse les joueurs jouer tant que la partie n'est pas terminée
                i = 0
                while not self.terminee:
                    if self.mode == "manuel":
                        inp_piece = input("Sélectionner une pièce :")
                        # q pour "quitter"
                        if inp_piece == "q":
                            self.terminee = True
                            break
                        # p pour "points"
                        if inp_piece == "p":
                            print(self.points_blanc, self.points_noir)
                            continue
                        # Récupère le contenu de la case aux corrdonées données
                        piece_selectionner: Piece = chess_utils.get_piece(self.grille,
                                                                          int(inp_piece.split(',')[0]),
                                                                          int(inp_piece.split(',')[1]))
                        # Si le joueur à sélectionner une case vide, ça recommence la boucle sans continuer pour que le joueur puisse entrer de nouvelles coordonnées
                        if not piece_selectionner:
                            print("Erreur, la case sélectionnée est vide.")
                            continue
                        # Si le joueur à sélectionner une pièce de son adversaire à jouer, ça recommence la boucle sans continuer pour que le joueur puisse entrer de nouvelles coordonnées
                        if piece_selectionner.couleur != self.tour:
                            print("Cette pièce n'est pas votre")
                            continue
                        print(f"Vous avez sélectionné {piece_selectionner.type_de_piece}")
                        print(
                            f"Voici la liste de coups possible : {piece_selectionner.liste_coups_legaux(self.grille)}")
                        inp_coup = input("Sélectionner le coup choisi :")
                        # r pour recommencer, si on ne veut plus jouer cette pièce
                        if inp_coup == "r":
                            continue
                        coup = piece_selectionner.move(int(inp_coup.split(',')[0]), int(inp_coup.split(',')[1]),
                                                       self.grille)
                        # boucle qui s'active que si le coup envoyé par le joueur n'est pas dans la liste des coups possibles, et donc redemande un coup au joueur,
                        # jusqu'à ce qu'il envoie un coup valide
                        while not coup:
                            inp_coup = input("Sélectionner nouvelle coordonnées :")
                            coup = piece_selectionner.move(int(inp_coup.split(',')[0]), int(inp_coup.split(',')[1]),
                                                           self.get_grille())
                            print(coup)
                        print(f"Vous avez jouer {inp_coup}")
                        # Met à jour le plateau après le mouvement
                        self.grille = coup
                        chess_utils.montrer_grille(self.grille)
                    if self.mode == "auto":
                        print(i)
                        i+=1
                        alpha = -float('inf')
                        beta = float('inf')
                        depth = 6  # choose a suitable search depth
                        # call negamax to find the best move
                        if self.tour == "blanc":
                            couleur = 1
                        else:
                            couleur = -1
                        start_time = time.time()
                        best_score, best_combo = negamax.negascout(self.grille, depth, color=couleur,
                                                                            alpha=-100000,
                                                                            beta=+100000)
                        print(best_score)
                        end_time = time.time()
                        total_time = end_time - start_time

                        print(f"Time taken: {total_time} seconds")
                        best_piece, best_move = best_combo
                        print(best_combo)
                        best_piece: Roi
                        self.grille = best_piece.move(best_move[0], best_move[1], self.grille)
                        chess_utils.montrer_grille(self.grille)
                    #change le tour
                    if self.tour == "blanc":
                        self.tour = "noir"
                    else:
                        self.tour = "blanc"
                    self.points_blanc, self.points_noir = chess_utils.points(self.grille)
                    #s'il ne reste pas au moins un roi de chaque couleur, ça termine la partie
                    echec_et_mat = chess_utils.check_si_echec_et_mat(p.grille)
                    if echec_et_mat:
                        print(f"Partie terminée! Les vainqueurs sont les {echec_et_mat} par échec et mat")
                        self.terminee = True
                    else:
                        echec_et_mat = chess_utils.check_si_roi_restant(self.grille)
                        if echec_et_mat:
                            print(
                                f"Partie terminée! Les vainqueurs sont les {chess_utils.check_si_roi_restant(self.grille)} par capture du roi")
                            self.terminee = True

                    if chess_utils.roi_contre_roi(self.grille):
                        print("Egalité ! Il ne reste que des rois sur le plateau.")
                        self.terminee = True
                print(i)
        else:
            print("Erreur, vous n'avez pas setup la position initiale")

#Partie exemple
p = Partie()
p.setup_from_fen("4r3/8/k7/7n/8/5qP1/5P1P/5K2")
#print(negamax.evaluate_board(p.grille, 1))
p.mode = "auto"
p.run()
