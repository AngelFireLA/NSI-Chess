import random

import chess_utils
from bots import negamax
from core_engine import endgame_and_opening_move_finder
from core_engine.partie import Partie
from core_engine.piece import Roi


def simulate_match(fen, bot1, bot2):
    partie = Partie()
    partie.mode = "auto"
    partie.setup_from_fen(fen)
    partie.temps_de_reflexion = None
    i = 0
    print("\n")
    while not partie.terminee:
        partie.compteur_de_tour+=1
        print(partie.compteur_de_tour, end=" ")
        if partie.tour == "blanc":
            couleur = 1
            depth = 3
            bot = bot1
        else:
            couleur = -1
            depth = 3
            bot = bot2

        if len(chess_utils.liste_pieces_bougeables(partie.grille, partie.tour)) + len(
                chess_utils.liste_pieces_bougeables(partie.grille, chess_utils.couleur_oppose(
                    partie.tour))) <= 7 and not chess_utils.check_si_roi_restant(partie.grille):
            meilleur_coup = endgame_and_opening_move_finder.get_best_endgame_move_from_tablebase(
                partie.grille, partie.tour)
            if meilleur_coup:
                piece, move = meilleur_coup
                best_score, best_combo = 69, (partie.grille[piece[1]][piece[0]], move)
            else:
                # best_score, best_combo = negamax.negascout(partie.grille, depth, color=couleur, alpha=-float('inf'), beta=float('inf'))
                best_score, best_combo = bot.iterative_deepening_negamax(partie.grille, couleur,
                                                                             depth, time_limit=partie.temps_de_reflexion, partie_original=partie)

        else:

            best_score, best_combo = bot.iterative_deepening_negamax(partie.grille, couleur, depth, time_limit=partie.temps_de_reflexion, partie_original=partie)

        best_piece, best_move = best_combo
        converted_coords = best_piece.x + best_move[0], best_piece.y + best_move[1]
        # print(best_score)
        # end_time = time.time()
        # total_time = end_time - start_time

        # print(f"Time taken: {total_time} seconds")

        #print(f"{best_piece.type_de_piece} {best_piece.couleur} en ({best_piece.x}, {best_piece.y}) a joué {best_move}")
        from core_engine.endgame_and_opening_move_finder import convert_custom_move
        if partie.compteur_de_tour % 2 == 1:
            if best_piece.type_de_piece == "pion":
                partie.pgn += f" {partie.compteur_de_tour // 2 + 1}. {convert_custom_move(best_piece, converted_coords)[1]}"
            else:
                partie.pgn += f" {partie.compteur_de_tour // 2 + 1}. {endgame_and_opening_move_finder.symbol_from_piece(best_piece).upper()}{convert_custom_move(best_piece, converted_coords)[1]}"
        else:
            if best_piece.type_de_piece == "pion":
                partie.pgn += f" {convert_custom_move(best_piece, converted_coords)[1]}"
            else:
                partie.pgn += f" {endgame_and_opening_move_finder.symbol_from_piece(best_piece).upper()}{convert_custom_move(best_piece, converted_coords)[1]}"
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
                f"Partie terminée! Les vainqueurs sont les {chess_utils.check_si_roi_restant(partie.grille)} par capture du roi en {partie.compteur_de_tour} coups.")
            partie.terminee = True
            #print(partie.pgn)
            return echec_et_mat

        if chess_utils.egalite(partie.grille, partie) or partie.compteur_de_tour == 100:
            print("Egalité !")
            partie.terminee = True
            #print(partie.pgn)
            return "draw"


def batch_simulate():
    bots = []
    winners = []
    # Parcourir chaque ligne
    for i in range(64):
        bot = negamax.Bot(f"{i}")
        bot.white_goku_table = [[], [], [], [],[], [], [], []]
        for j in range(8):
            for k in range(8):
                bot.white_goku_table[j].append(random.randint(-50, 50))
        bot.black_goku_table = [row[::-1] for row in bot.white_goku_table[::-1]]
        bot.piece_tables["blanc"]["goku"] = bot.white_goku_table
        bot.piece_tables["noir"]["goku"] = bot.black_goku_table
        bots.append(bot)
        # print(f"Partie numéro {i+1} débutée")
        # # Utiliser la ligne comme vous le souhaitez
        # result = simulate_match(ligne.split()[0])
        # if result:
        #     results[result]+=1
        # print(results)
    while not len(winners) == 1:
        print(len(bots))
        while len(bots) > 1:
            bot1 = random.choice(bots)
            bots.remove(bot1)
            bot2 = random.choice(bots)
            bots.remove(bot2)
            result = simulate_match("rnbqkbnr/ppgppgpp/8/8/8/8/PPGPPGPP/RNBQKBNR", bot1, bot2)
            if result == "blanc":
                print("win blanc")
                winners.append(bot1)
                print(bot1.name)
                for l in bot1.white_goku_table:
                    print(l)
                print()
            elif result == "noir":
                print("win noir")
                winners.append(bot2)
                print(bot2.name)
                for l in bot2.white_goku_table:
                    print(l)
                print()
            else:
                print("egalite")
                bots.append(bot1)
                bots.append(bot2)
        if winners:
            bots = winners
        else:
            print("no winners ?")
    print("gagnant")
    for l in winners[0].white_goku_table:
        print(l)
    partie = Partie()
    partie.setup_from_fen("rnbqkbnr/ppgppgpp/8/8/8/8/PPGPPGPP/RNBQKBNR")
    partie.depth = 4
    partie.mode = "semi-auto"
    partie.run("blanc")
    # print("Résultats finaux :", results)

batch_simulate()