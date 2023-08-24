import time

import chess_utils
from bots import negascout_last, negascout_v1, negascout_v2, negascout_v3, negascout_v4, negascout_v5, negascout_v6, negascout_v7, negascout_v8, negamax_v1, negamax_v2
from engine import endgame_and_opening_move_finder
from engine.partie import Partie
from engine.pieces.piece import Roi



def simulate_match(fen):
    partie = Partie()
    partie.mode = "auto"
    partie.setup_from_fen(fen)
    partie.temps_de_reflexion = 5
    i = 0
    print("\n")
    while not partie.terminee:
        i+=1
        print(i, end=" ")
        if partie.tour == "blanc":
            couleur = 1
            depth = partie.depth
        else:
            couleur = -1
            depth = partie.second_depth
        # Vérifie si la position est dans le livre d'ouverture, et si oui jouer le coup recommandé
        # start_time = time.time()
        # S'il y a 7 pièces au moins restantes sur le plateau, utiliser le solveur de fin de partie
        if len(chess_utils.liste_pieces_bougeables(partie.grille, partie.tour)) + len(
                chess_utils.liste_pieces_bougeables(partie.grille, chess_utils.couleur_oppose(
                    partie.tour))) <= 7 and not chess_utils.check_si_roi_restant(partie.grille):
            meilleur_coup = endgame_and_opening_move_finder.get_best_endgame_move_from_tablebase(
                partie.grille, partie.tour)
            if meilleur_coup:
                piece, move = meilleur_coup
                best_score, best_combo = 69, (partie.grille[piece[1]][piece[0]], move)
            else:
                print("pas de meilleur coup même avec 7 pièces")
                if partie.tour == "blanc":
                    negascout_last.init_transposition()
                    # best_score, best_combo = negamax.negascout(partie.grille, depth, color=couleur, alpha=-float('inf'), beta=float('inf'))
                    best_score, best_combo = None, None
                    while not best_score and not best_combo:
                        best_score, best_combo = negascout_last.iterative_deepening_negamax(partie.grille, couleur, depth, time_limite=partie.temps_de_reflexion)
                else:
                    best_score, best_combo = None, None
                    while not best_score and not best_combo:
                        best_score, best_combo = negamax_v1.iterative_deepening_negamax(partie.grille, couleur, depth, time_limite=partie.temps_de_reflexion)

        # utilise l'algorithme de recherche du meilleur coup de negascout_last.py de manière normale
        else:
            if partie.tour == "blanc":
                negascout_last.init_transposition()
                # best_score, best_combo = negamax.negascout(partie.grille, depth, color=couleur, alpha=-float('inf'), beta=float('inf'))
                best_score, best_combo = None, None
                while not best_score and not best_combo:
                    best_score, best_combo = negascout_last.iterative_deepening_negamax(partie.grille, couleur, depth,
                                                                                    time_limite=partie.temps_de_reflexion)
            else:
                best_score, best_combo = None, None
                while not best_score and not best_combo:
                    best_score, best_combo = negamax_v1.iterative_deepening_negamax(partie.grille, couleur, depth,
                                                                                time_limite=partie.temps_de_reflexion)
        echec_et_mat = chess_utils.check_si_roi_restant(partie.grille)
        if echec_et_mat:
            print(
                f"Partie terminée! Les vainqueurs sont les {chess_utils.check_si_roi_restant(partie.grille)} par capture du roi en {i} coups.")
            partie.terminee = True
            return echec_et_mat

        if chess_utils.roi_contre_roi(partie.grille) or i == 100:
            print("Egalité !")
            partie.terminee = True
            return "draw"
        # Récupère meilleur pièce, coup et score
        best_piece, best_move = best_combo
        # print(best_score)
        # end_time = time.time()
        # total_time = end_time - start_time

        # print(f"Time taken: {total_time} seconds")

        # print(f"{best_piece.type_de_piece} {best_piece.couleur} en ({best_piece.x}, {best_piece.y}) a joué {best_move}")
        best_piece: Roi
        # Effectue le meilleur coup trouvé
        partie.grille = best_piece.move(best_move[0], best_move[1], partie.grille)
        # chess_utils.montrer_grille(partie.grille)

        # change le tour
        if partie.tour == "blanc":
            partie.tour = "noir"
        else:
            partie.tour = "blanc"
        partie.points_blanc, partie.points_noir = chess_utils.points(partie.grille)
        # s'il ne reste pas au moins un roi de chaque couleur, ça termine la partie
        echec_et_mat = chess_utils.check_si_roi_restant(partie.grille)
        if echec_et_mat:
            print(
                f"Partie terminée! Les vainqueurs sont les {chess_utils.check_si_roi_restant(partie.grille)} par capture du roi en {i} coups.")
            partie.terminee = True
            return echec_et_mat

        if chess_utils.roi_contre_roi(partie.grille) or i == 100:
            print("Egalité !")
            partie.terminee = True
            return "draw"


def batch_simulate():
    with open('100_equal_positions.txt', 'r') as fichier:
        # Lire chaque ligne du fichier
        lignes = fichier.readlines()
    results = {"blanc": 0, "noir": 0, "draw": 0}
    # Parcourir chaque ligne
    for i in range(len(lignes)):
        print(f"Partie numéro {i+1} débutée")
        ligne = lignes[i]
        # Supprimer les caractères de nouvelle ligne (\n)
        ligne = ligne.strip()
        # Utiliser la ligne comme vous le souhaitez
        result = simulate_match(ligne.split()[0])
        if result:
            results[result]+=1
        print(results)
    print("Résultats finaux :", results)

batch_simulate()