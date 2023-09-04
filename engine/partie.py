from interface import chess_game
import chess_utils
from engine.pieces.piece import Roi, Tour, Fou, Cavalier, Dame, Pion, Piece, Goku, Vegeta, Voleur, Imposteur
import bots.negamax as negamax

import engine.endgame_and_opening_move_finder as endgame_and_opening_move_finder
import time


class Partie:
    def __init__(self, type_de_partie: str = "normale", tour="blanc", mode="manuel"):
        # setup pour voir si le plateau a été défini
        self.setup = False
        self.terminee = False
        # tour dans "a qui le tour" et pas la pièce
        self.tour = tour
        self.type_de_partie = type_de_partie
        self.grille = None
        self.mode = mode
        self.depth = 4
        self.second_depth = 4
        self.temps_de_reflexion = None
        self.compteur_de_tour = 0
        self.pgn = """[Event "Game"]
[Site "Somewhere"]
[Date "Sometime"]
[Round "1"]
[White "White"]
[Black "Black"]
[Result "*"]\n
        """
        self.repetitions = []

    # Met en place le tableau à partir d'un string FEN qui est un texte qui dit quel pièce va a quelle place,
    # on peut le générer pour n'importe quel position
    def setup_from_fen(self, fen: str):
        if fen == "default":
            fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
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

    #CUSTOM TODO
    # Dans un string fen, chaque lettre veut dire une pièce, ici on définit quelle lettre dans le string FEN correspond à quelle pièce, agrandissable pour des pièces customs
    def piece_from_symbol(self, symbol: str):
        symbol_piece_dict = {
            'K': (Roi, "blanc"), 'Q': (Dame, "blanc"), 'R': (Tour, "blanc"), 'B': (Fou, "blanc"),
            'N': (Cavalier, "blanc"), 'P': (Pion, "blanc"), 'G': (Goku, "blanc"), 'V': (Vegeta, 'blanc'), 'T': (Voleur, 'blanc'), 'I': (Imposteur, 'blanc'),
            'k': (Roi, "noir"), 'q': (Dame, "noir"), 'r': (Tour, "noir"), 'b': (Fou, "noir"),
            'n': (Cavalier, "noir"), 'p': (Pion, "noir"), 'g': (Goku, "noir"), 'v': (Vegeta, 'noir'), 't': (Voleur, 'noir'), 'i': (Imposteur, 'noir'),
        }
        return symbol_piece_dict[symbol]

    # Boucle qui gère le début jusqu'à la fin d'une partie
    def run(self, couleur="blanc", menu=False):

        if self.setup:
            import bots.negamax as negamax
            if self.type_de_partie == "normale":
                if menu:
                    import interface.chess_menu as chess_menu
                    chess_menu.start_menu(self)
                    return
                # Boucle qui laisse les joueurs jouer tant que la partie n'est pas terminée

                if self.mode == "auto":
                    chess_utils.montrer_grille(self.grille)
                    negamax.init_transposition()
                    self.repetitions.append(negamax.zobrist_hash(self.grille, self.compteur_de_tour))
                    while not self.terminee:
                        # manuel = joueur contre joueur, semi-auto = joueur contre bot, auto = bot contre bot
                        if self.tour == "blanc":
                            couleur = 1
                            depth = self.depth
                        else:
                            couleur = -1
                            depth = self.second_depth
                        # Vérifie si la position est dans le livre d'ouverture, et si oui jouer le coup recommandé
                        start_time = time.time()
                        opening = endgame_and_opening_move_finder.get_best_move_from_opening_book(self.grille,
                                                                                                  self.tour)
                        if opening:
                            piece, move = opening
                            best_score, best_combo = 69, (self.grille[piece[1]][piece[0]], move)

                        else:
                            # S'il y a 7 pièces au moins restantes sur le plateau, utiliser le solveur de fin de partie
                            if len(chess_utils.liste_pieces_bougeables(self.grille, self.tour)) + len(
                                    chess_utils.liste_pieces_bougeables(self.grille, chess_utils.couleur_oppose(
                                        self.tour))) <= 7 and not chess_utils.check_si_roi_restant(self.grille):
                                meilleur_coup = endgame_and_opening_move_finder.get_best_endgame_move_from_tablebase(
                                    self.grille, self.tour)
                                if meilleur_coup:
                                    piece, move = meilleur_coup
                                    best_score, best_combo = 69, (self.grille[piece[1]][piece[0]], move)
                                else:

                                    # best_score, best_combo = negamax.negascout(self.grille, depth, color=couleur, alpha=-float('inf'), beta=float('inf'))
                                    best_score, best_combo = negamax.iterative_deepening_negamax(self.grille, couleur,
                                                                                                 depth, partie_original=self)

                            # utilise l'algorithme de recherche du meilleur coup de negamax.py de manière normale
                            else:
                                best_score, best_combo = negamax.iterative_deepening_negamax(self.grille, couleur,
                                                                                             depth, partie_original=self)
                        # Récupère meilleur pièce, coup et score
                        best_piece, best_move = best_combo
                        print(best_score)
                        end_time = time.time()
                        total_time = end_time - start_time

                        print(f"Time taken: {total_time} seconds")

                        print(
                            f"{best_piece.type_de_piece} {best_piece.couleur} en ({best_piece.x}, {best_piece.y}) a joué {best_move}")
                        best_piece: Roi
                        # Effectue le meilleur coup trouvé
                        self.grille = best_piece.move(best_move[0], best_move[1], self.grille)
                        chess_utils.montrer_grille(self.grille)
                        self.repetitions.append(negamax.zobrist_hash(self.grille, self.compteur_de_tour))
                        # change le tour
                        if self.tour == "blanc":
                            self.tour = "noir"
                        else:
                            self.tour = "blanc"
                        self.compteur_de_tour+=1
                        # s'il ne reste pas au moins un roi de chaque couleur, ça termine la partie
                        echec_et_mat = chess_utils.check_si_roi_restant(self.grille)
                        if echec_et_mat:
                            print(
                                f"Partie terminée! Les vainqueurs sont les {chess_utils.check_si_roi_restant(self.grille)} par capture du roi")
                            self.terminee = True

                        if chess_utils.egalite(self.grille, self):
                            print("Egalité ! Il ne reste que des rois sur le plateau.")
                            self.terminee = True
                if self.mode == "semi-auto":
                    chess_game.start_semiauto(self, couleur)
                if self.mode == "manuel":
                    chess_game.start_manuel(self)
        else:
            print("Erreur, vous n'avez pas setup la position initiale")





