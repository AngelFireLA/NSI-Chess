import random
import time

import chess_utils
import copy


white_knight_table = [
    [-50, -40, -30, -30, -30, -30, -40, -50],
    [-40, -20, 0, 0, 0, 0, -20, -40],
    [-30, 5, 10, 15, 15, 10, 5, -30],
    [-30, 0, 15, 20, 20, 15, 0, -30],
    [-30, 0, 15, 20, 20, 15, 0, -30],
    [-30, 5, 10, 15, 15, 10, 5, -30],
    [-40, -20, 0, 0, 0, 0, -20, -40],
    [-50, -40, -30, -30, -30, -30, -40, -50]
]

white_bishop_table = [
    [10, -10, -10, -10, -10, -10, -10, 10],
    [-10, 0, 0, 0, 0, 0, 0, -10],
    [-10, 0, 5, 10, 10, 5, 0, -10],
    [-10, 5, 5, 10, 10, 5, 5, -10],
    [-10, 0, 10, 10, 10, 10, 0, -10],
    [-10, 10, 10, 10, 10, 10, 10, -10],
    [-10, 5, 0, 0, 0, 0, 5, -10],
    [10, -10, -10, -10, -10, -10, -10, 10]
]

white_rook_table = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [5, 10, 10, 10, 10, 10, 10, 5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [0, 0, 0, 5, 5, 0, 0, 0]
]

white_queen_table = [
    [-20, -10, -10, -5, -5, -10, -10, -20],
    [-10, 0, 0, 0, 0, 0, 0, -10],
    [-10, 0, 5, 5, 5, 5, 0, -10],
    [-5, 0, 5, 5, 5, 5, 0, -5],
    [-5, 0, 5, 5, 5, 5, 0, -5],
    [-10, 0, 5, 5, 5, 5, 0, -10],
    [-10, 0, 0, 0, 0, 0, 0, -10],
    [-20, -10, -10, -5, -5, -10, -10, -20]
]

white_pawn_table = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [50, 50, 50, 50, 50, 50, 50, 50],
    [10, 10, 20, 30, 30, 20, 10, 10],
    [5, 5, 10, 25, 25, 10, 5, 5],
    [0, 0, 0, 20, 20, 0, 0, 0],
    [5, -5, -10, 0, 0, -10, -5, 5],
    [5, 10, 10, -20, -20, 10, 10, 5],
    [0, 0, 0, 0, 0, 0, 0, 0]
]

white_king_table = [
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-20, -30, -30, -40, -40, -30, -30, -20],
    [-10, -20, -20, -20, -20, -20, -20, -10],
    [20, 20, 0, 0, 0, 0, 20, 20],
    [20, 30, 10, 0, 0, 10, 30, 20]
]


#Inverse les tables pour les noirs
black_knight_table = [row[::-1] for row in white_knight_table[::-1]]
black_bishop_table = [row[::-1] for row in white_bishop_table[::-1]]
black_rook_table = [row[::-1] for row in white_rook_table[::-1]]
black_queen_table = [row[::-1] for row in white_queen_table[::-1]]
black_king_table = [row[::-1] for row in white_king_table[::-1]]
black_pawn_table = [row[::-1] for row in white_pawn_table[::-1]]



piece_tables = {
    "blanc": {
        "cavalier": white_knight_table,
        "fou": white_bishop_table,
        "tour": white_rook_table,
        "dame": white_queen_table,
        "roi": white_king_table,
        "pion": white_pawn_table
    },
    "noir": {
        "cavalier": white_knight_table,
        "fou": black_bishop_table,
        "tour": black_rook_table,
        "dame": white_queen_table,
        "roi": black_king_table,
        "pion": black_pawn_table
    }
}


#Fonction pour évaluer le plateau, très importante car c'est grâce à elle que le bot sait si il gagne ou pas

#pip install functools
#@cache
def evaluate_board(grid, couleur: int, partie):



    score_blanc, score_noir = chess_utils.points_avec_roi(grid)

    # Donne les points selon la position de chaque pièce selon le tableau
    for piece in chess_utils.liste_pieces_restantes(grid):
        if piece.couleur == "blanc":
            try:
                score_blanc+=(piece_tables["blanc"][piece.type_de_piece][piece.y][piece.x])
            except KeyError:
                continue
        else:
            try:
                score_noir += (piece_tables["noir"][piece.type_de_piece][piece.y][piece.x])
            except KeyError:
                continue
    #Retourne le score finale multiplier par la valeur de la couleur car un score négatif est bon pour noir
    return (score_blanc - score_noir) * couleur


# Initialize divers variables utilisées dans l'algorithme pour réduire le temps de recherche
#move_history = [[0] * 8 for _ in range(8)]  # Assuming an 8x8 chessboard size

max_depth = 10


best_moves_from_inferior_depth = []


#Tables de transpositions, store le score d'un plateau selon la couleur, évite de devoir recalculé évaluation à chaque fois et sauve beaucoup de temps
#On utilise une table de zobrist pour générer des valeurs uniques pour chaque position
zobrist = []
transposition_table = {}

#CUSTOM TODO
piece_type_mapping = {"roi": 0, "dame": 1, "tour": 2, "fou": 3, "cavalier": 4, "pion": 5, "goku":6, "vegeta":7, "voleur":8}
piece_color_mapping = {"blanc": 0, "noir": 1}
                
def init_transposition():
    global zobrist, transposition_table

    for _ in range(64):
        square = []
        for _ in range(12):
            piece = []
            for _ in range(2):
                piece.append(random.getrandbits(64))
            square.append(piece)
        zobrist.append(square)

    transposition_table = {}
def zobrist_hash(board, ply_count):
    """
    Generate a unique hash for a board position using Zobrist hashing.

    Hashing algorithm from Zobrist (1970).

    Args:
        board (list): The current state of the chessboard.
        ply_count (int): The number of moves since the start of the game.

    Returns:
        int: The hash value for the given board position and depth.
    """
    hash_value = 0
    for y in range(8):
        for x in range(8):
            piece = board[y][x]  # Replace this with your own method to get the piece at a specific position
            if piece:
                # Map piece types and colors to corresponding integer values

                square_index = y * 8 + x

                hash_value ^= zobrist[square_index][piece_type_mapping[piece.type_de_piece]][piece_color_mapping[piece.couleur]]

    hash_value ^= ply_count  # XOR the hash value with the depth parameter

    return hash_value

def get_transposition_entry(hash_value, ply_count):
    if hash_value in transposition_table:
        entry:dict = transposition_table[hash_value]
        if entry and entry.get('ply_count', 0) >= ply_count:
            return entry.get('score')
    return None

def store_transposition(hash_value, score, ply_count):

    transposition_table[hash_value] = {'score': score, 'ply_count': ply_count}



#Fonction qui ordonne les mouvements selon leur probabilité d'être bon puisque si l'algorithme regarde d'abord les coups bons, il s'arrêtera plus vite.
def move_ordering(piece_moves, board, couleur, is_initial_depth:bool=False):
    #captures de roi (donc echec et mat)
    captures = []
    capture_moves = chess_utils.possible_captures(couleur, board)
    for i in range(len(capture_moves)):
        score = capture_moves[i][0][0].valeur - capture_moves[i][1].valeur
        captures.append((capture_moves[i][0][0], capture_moves[i][0][1], score))

    captures.sort(key=lambda x: x[2], reverse=True)

    captures = [(piece, move) for piece, move, _ in captures]

    # Trie les "quiet_moves" en fonction des valeurs d'historique de mouvement dans l'ordre décroissant.
    #quiet_moves = sorted(quiet_moves, key=lambda x: move_history[x[1][1]][x[1][0]], reverse=True)
    piece_moves = [movement for movement in piece_moves if movement not in captures]

    # Ajoute le mouvement de variation principale au début de la liste des mouvements s'il existe.
    if is_initial_depth:
        ordered_moves = best_moves_from_inferior_depth + captures + piece_moves
    else:
        ordered_moves = captures + piece_moves
    return ordered_moves


best_move_global = None
BIG_VALUE = 9999999
#Fonction principale du bot qui recherche le meilleur coup
def negamax(board, depth, alpha=-BIG_VALUE, beta=BIG_VALUE, color=1, initial_depth=4, partie=None):
    global  best_move_global, best_moves_from_inferior_depth
    if color == 1:
        couleur = "blanc"
    else:
        couleur = "noir"
    if chess_utils.egalite(board, partie):
        return 0
    #Récupère si possible le score de la table de transposition
    hash_value = zobrist_hash(board, partie.compteur_de_tour)

    checkmate = chess_utils.check_si_roi_restant(board)

    #Si la partie est fini ou si la recherche a atteint son maximum
    if depth == 0 or checkmate:

        if checkmate == chess_utils.couleur_oppose(couleur):

            return -30000+(initial_depth-depth)*10
        cached_score = get_transposition_entry(hash_value, partie.compteur_de_tour)
        if cached_score:
            evalu = cached_score
        else:
            # Call q_search instead of evaluate_board
            evalu = q_search(alpha, beta, depth, board, color, partie)

        return evalu

    best_value = -BIG_VALUE
    #trie les mouvements
    all_moves = chess_utils.liste_coups_legaux(couleur, board)
    is_root = False
    if initial_depth == depth:
        is_root = True
    ordered_moves = move_ordering(all_moves, board, couleur, is_root)
    #Boucle principale qui itère sur les coups
    for piece, move in ordered_moves:
        if time.time() - start_time > time_limit_global:
            break
        #On duplique les pièces et le plateau pour ne pas les modifier eux directement
        new_board = [[piece.copy() if piece is not None else None for piece in row] for row in board]

        new_piece = piece.copy()

        #On modifie le plateau avec le coup à tester
        new_board = new_piece.move(move[0], move[1], new_board)
        partie.compteur_de_tour+=1
        partie.repetitions.append(zobrist_hash(partie.grille, partie.compteur_de_tour))
        #On va en récursivité pour tester les prochains coups, les conditions sont de l'optimization avec divers techniques trouvées
        score= negamax(new_board, depth - 1, -beta, -alpha, -color, initial_depth, partie=partie)
        partie.compteur_de_tour -= 1
        partie.repetitions.pop()
        value = -score

        if value > best_value:
            best_value = value
            if is_root:
                best_move_global = (piece, move)

        alpha = max(alpha, value)

        if alpha >= beta:
            break

    store_transposition(hash_value, best_value, partie.compteur_de_tour)
    return best_value

def q_search(alpha, beta, depth, board, color, partie):


    stand_pat = evaluate_board(board, color, partie)
    if stand_pat >= beta:
        return beta
    if alpha < stand_pat:
        alpha = stand_pat
    captures = chess_utils.possible_captures(color, board)

    if not captures:  # Return the stand-pat score if there are no captures
        return stand_pat

    for piece, move in captures:
        new_board = [[piece.copy() if piece is not None else None for piece in row] for row in board]
        new_piece = piece.copy()
        new_board = new_piece.move(move[0], move[1], new_board)
        value = -q_search(-beta, -alpha, depth - 1, new_board, -color)
        if value >= beta:
            return beta
        alpha = max(alpha, value)
    return alpha



start_time = None
time_limit_global = None
compteur_tour = 0

#Technique d'optimization qui consiste à d'abord trouver le meilleur coup pour un recherche moins poussée, car il y a des chances que ça soit un bon coup
def iterative_deepening_negamax(board, couleur, final_depth, time_limit=None, p_compteur_tour=0, partie_original=None):
    from engine.partie import Partie
    global  start_time, time_limit_global, best_move_global, best_moves_from_inferior_depth
    if not partie_original:
        raise ValueError
    partie: Partie = copy.deepcopy(partie_original)
    p_compteur_tour = partie.compteur_de_tour
    j=0
    entries_to_remove = []
    for hash in transposition_table:
        entry = transposition_table[hash]
        if abs(int(entry.get('ply_count', 0)) - p_compteur_tour) > partie.depth:
            # remove entry the dict transposition table
            entries_to_remove.append(hash)
            j += 1

    for entry in entries_to_remove:
        del transposition_table[entry]

    #print("removed",j," entries")

    if not time_limit:
        time_limit_global = 10000
        start_time = time.time()
        print("depth : ", final_depth)
        # best_score = negamax(board, final_depth, color=couleur, alpha=-float("inf"), beta=float("inf"), initial_depth=final_depth)
        best_moves_from_inferior_depth = []
        for i in range(1, final_depth + 1):
            best_move_global = None
            best_score = negamax(board, i, color=couleur, alpha=-float("inf"), beta=float("inf"), initial_depth=i, partie=partie)
            best_moves_from_inferior_depth.insert(0, best_move_global)
    else:
        time_limit_global = time_limit
        start_time = time.time()
        print("depth : Unlimited")
        # best_score = negamax(board, final_depth, color=couleur, alpha=-float("inf"), beta=float("inf"), initial_depth=final_depth)
        best_moves_from_inferior_depth = []
        for i in range(1, 100):
            best_move_global = None
            best_score = negamax(board, i, color=couleur, alpha=-float("inf"), beta=float("inf"), initial_depth=i, partie=partie)
            best_moves_from_inferior_depth.insert(0, best_move_global)
            print("Achieved depth : ", i)
            if time.time() - start_time > time_limit_global:
                print("Time limit reached", time.time() - start_time)
                break
            if time.time() - start_time > time_limit_global-1 and i >4:
                print("Time limit reached", time.time() - start_time)
                break


    return best_score, best_move_global

