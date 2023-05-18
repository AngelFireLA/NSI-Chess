import random

import chess_utils
from engine.pieces.piece import Roi, Piece, Pion
import copy

piece_values = {
    "pion": 100,
    "cavalier": 320,
    "fou": 330,
    "tour": 500,
    "dame": 900,
    "roi": 20000
}

multiplier = 1

white_knight_table = [
    [-50, -40, -30, -30, -30, -30, -40, -50],
    [-40, -20, 0, 0, 0, 0, -20, -40],
    [-30, 0, 10, 15, 15, 10, 0, -30],
    [-30, 5, 15, 20, 20, 15, 5, -30],
    [-30, 0, 15, 20, 20, 15, 0, -30],
    [-30, 5, 10, 15, 15, 10, 5, -30],
    [-40, -20, 0, 5, 5, 0, -20, -40],
    [-50, -40, -30, -30, -30, -30, -40, -50]
]

white_bishop_table = [
    [-20, -10, -10, -10, -10, -10, -10, -20],
    [-10, 0, 0, 0, 0, 0, 0, -10],
    [-10, 0, 5, 10, 10, 5, 0, -10],
    [-10, 5, 5, 10, 10, 5, 5, -10],
    [-10, 0, 10, 10, 10, 10, 0, -10],
    [-10, 10, 10, 10, 10, 10, 10, -10],
    [-10, 5, 0, 0, 0, 0, 5, -10],
    [-20, -10, -10, -10, -10, -10, -10, -20]
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
    [0, 0, 5, 5, 5, 5, 0, -5],
    [-10, 5, 5, 5, 5, 5, 0, -10],
    [-10, 0, 5, 0, 0, 0, 0, -10],
    [-20, -10, -10, -5, -5, -10, -10, -20]
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



black_knight_table = [row[::-1] for row in white_knight_table]
black_bishop_table = [row[::-1] for row in white_bishop_table]
black_rook_table = [row[::-1] for row in white_rook_table]
black_queen_table = [row[::-1] for row in white_queen_table]
black_king_table = [row[::-1] for row in white_king_table]
black_pawn_table = [row[::-1] for row in white_pawn_table]



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
        "cavalier": black_knight_table,
        "fou": black_bishop_table,
        "tour": black_rook_table,
        "dame": black_queen_table,
        "roi": black_king_table,
        "pion": black_pawn_table
    }
}


def evaluate_board(grid, couleur: int):
    score_blanc, score_noir = 0, 0


    #equilibre des points
    points_blanc, points_noir = chess_utils.points_avec_roi(grid)
    score_blanc+=points_blanc
    score_noir+=points_noir


    #position des pièces

    #
    # #cases controlees
    # coups = {"blanc": chess_utils.liste_coups_legaux("blanc", grid),
    #          "noir": chess_utils.liste_coups_legaux("noir", grid)}
    # cases_controlees = set()
    # cases_par_couleur = {"blanc": 0, "noir": 0}
    # for c in coups:
    #     for piece, coup in coups[c]:
    #         case = (piece.x + coup[0], piece.y + coup[1])
    #         if case not in cases_controlees:
    #             cases_controlees.add(case)
    #             cases_par_couleur[c] += 1
    #
    # score_blanc += cases_par_couleur["blanc"]*0.1
    # score_noir +=  cases_par_couleur["noir"]*0.1
    #
    # #sureté du roi*
    # for l in range(-1,2, 2):
    #     pieces = []
    #     for piece in chess_utils.liste_pieces_bougeables(grid, chess_utils.get_couleur_str(l)):
    #         if isinstance(piece, Roi):
    #             pieces.append(piece)
    #
    #     if len(pieces) <1:
    #         continue
    #     roi: Roi = pieces[0]
    #
    #     score_de_position = carte_suretee_du_roi[roi.y][roi.x]
    #     pions = 0
    #     pion_par_colonne = {-1: 0, 0: 0, 1: 0}
    #     if roi.couleur == "blanc":
    #         # count how many pion there is in the 3 squares in front of the king
    #
    #         for i in range(-1, 2):
    #             if roi.y - 1 < 0:
    #                 break
    #             if roi.x + i < 0 or roi.x + i > 7:
    #                 break
    #             if grid[roi.y - 1][roi.x + i]:
    #                 pions += 1
    #                 pion_par_colonne[i] += 1
    #             if roi.y - 2 < 0:
    #                 continue
    #             if grid[roi.y - 2][roi.x + i]:
    #                 pions += 1
    #                 pion_par_colonne[i] += 1
    #     else:
    #         # count how many pion there is in the 3 squares in front of the king
    #         for i in range(-1, 2):
    #             if roi.y + 1 > 7:
    #                 break
    #             if roi.x + i < 0 or roi.x + i > 7:
    #                 break
    #             if grid[roi.y + 1][roi.x + i]:
    #                 pions += 1
    #                 pion_par_colonne[i] += 1
    #             if roi.y + 2 > 7:
    #                 continue
    #             if grid[roi.y + 2][roi.x + i]:
    #                 pions += 1
    #                 pion_par_colonne[i] += 1
    #
    #     king_safety = 0
    #
    #
    #     valeur_pion_par_colonne = 0
    #     for k, v in pion_par_colonne.items():
    #         if v == 0:
    #             valeur_pion_par_colonne -= 5
    #         elif v == 1:
    #             valeur_pion_par_colonne += 10
    #         elif v == 2:
    #             valeur_pion_par_colonne += 15
    #         else:
    #             valeur_pion_par_colonne += 5 * v + 5
    #
    #     king_safety += valeur_pion_par_colonne
    #
    #     king_safety += 5 * pions
    #
    #     king_safety += score_de_position
    #     king_safety -= 15 * len([elem for elem in chess_utils.liste_pieces_dans_rayon(grid, roi.x, roi.y, 2) if
    #                              elem.couleur != roi.couleur])
    #     king_safety -= 10 * len([elem for elem in chess_utils.liste_pieces_dans_rayon(grid, roi.x, roi.y, 3) if
    #                              elem.type_de_piece == "dame"])
    #     if chess_utils.get_couleur_str(l) == "blanc":
    #         score_blanc+=king_safety
    #     else:
    #         score_noir+=king_safety
    #
    # #pion structure
    # pion_structure_score = 0
    # isolated_pions_score = 0
    # doubled_pions_score = 0
    # tripled_pions_score = 0
    # pion_chain_score = 0
    #
    # pion_structure = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0}
    # pions = [piece for piece in chess_utils.liste_pieces_bougeables(grid, "blanc") if isinstance(piece, Roi)]
    # for pion in pions:
    #     pion_structure[pion.x] += 1
    #
    #
    # # Calculate isolated pions
    # for column in range(8):
    #     if pion_structure[column] > 0:
    #         if column == 0:
    #             if pion_structure[column + 1] == 0:
    #                 isolated_pions_score -= 20
    #         elif column == 7:
    #             if pion_structure[column - 1] == 0:
    #                 isolated_pions_score -= 20
    #         else:
    #             if pion_structure[column - 1] == 0 and pion_structure[column + 1] == 0:
    #                 isolated_pions_score -= 20
    #
    # # Calculate doubled and tripled pions
    # for column in range(8):
    #     if pion_structure[column] > 1:
    #         doubled_pions_score -= 10 * (pion_structure[column] - 1)
    #     if pion_structure[column] > 2:
    #         tripled_pions_score -= 20 * (pion_structure[column] - 2)
    #
    # # Calculate pion chains
    # for column in range(8):
    #     if pion_structure[column] > 0:
    #         if column == 0:
    #             if pion_structure[column + 1] > 0:
    #                 pion_chain_score += 10
    #         elif column == 7:
    #             if pion_structure[column - 1] > 0:
    #                 pion_chain_score += 10
    #         else:
    #             if pion_structure[column - 1] > 0 and pion_structure[column + 1] > 0:
    #                 pion_chain_score += 10
    #
    #
    #
    # pion_structure_score = isolated_pions_score + doubled_pions_score + tripled_pions_score + pion_chain_score

    for i in range(-1,2, 2):
        for piece in chess_utils.liste_pieces_bougeables(grid, chess_utils.get_couleur_str(i)):
            if piece.couleur == "blanc":
                score_blanc+=(piece_tables["blanc"][piece.type_de_piece][piece.y][piece.x])/2
            else:
                score_noir += (piece_tables["noir"][piece.type_de_piece][piece.y][piece.x])/2

    return (score_blanc-score_noir)*couleur


# Initialize the move history structure
move_history = [[0] * 8 for _ in range(8)]  # Assuming an 8x8 chessboard size

max_depth = 10

killer_moves_history = [[] for _ in range(max_depth)]

def move_ordering(piece_moves, board, couleur, killer_moves):
    king_captures = []
    other_captures = []
    quiet_moves = set()

    capture_moves = set(chess_utils.possible_captures_ou_promotions(couleur, board))

    for piece, move in piece_moves:
        if (piece, move) in capture_moves:
            if piece.type_de_piece == "roi":
                king_captures.append((piece, move))
            else:
                # Calculate the value of the captured piece and the attacking piece
                target_square = (piece.x + move[0], piece.y + move[1])
                target_piece = board[target_square[1]][target_square[0]]
                captured_piece_value = target_piece.valeur if target_piece else 0
                attacking_piece_value = piece.valeur

                # Use MVV/LVA ordering by assigning a score to the move
                score = captured_piece_value - attacking_piece_value

                other_captures.append((piece, move, score))
        else:
            quiet_moves.add((piece, move))

    # Sort other_captures based on the scores in descending order
    other_captures.sort(key=lambda x: x[2], reverse=True)

    other_captures = [(piece, move) for piece, move, _ in other_captures]

    # Sort quiet_moves based on the move history values in descending order
    quiet_moves = sorted(quiet_moves, key=lambda x: move_history[x[1][1]][x[1][0]], reverse=True)

    # Order the moves based on the priorities
    ordered_moves = king_captures + killer_moves + other_captures + quiet_moves
    return ordered_moves

def negascout_original(board, depth, alpha=float('-inf'), beta=float('inf'), color=1):
    if depth == 0 or chess_utils.check_si_roi_restant(board):
        return evaluate_board(board, color), None

    best_move = None
    b = beta
    if color == 1:
        couleur = "blanc"
    else:
        couleur = "noir"

    all_moves = chess_utils.liste_coups_legaux(couleur, board)

    killer_moves = killer_moves_history[depth]  # Retrieve killer moves

    # Order the moves using move ordering
    ordered_moves = move_ordering(all_moves, board, couleur, killer_moves)


    for piece, move in ordered_moves:
        new_board = copy.deepcopy(board)
        new_piece = copy.deepcopy(piece)
        new_board = new_piece.move(move[0], move[1], new_board)

        # Update move history
        target_square = (piece.x + move[0], piece.y + move[1])
        target_piece = new_board[target_square[1]][target_square[0]]
        move_history[target_square[1]][target_square[0]] += 1

        if b == beta or b == alpha + 1:
            score, _ = negascout(new_board, depth - 1, -b, -alpha, -color)
        else:
            score, _ = negascout(new_board, depth - 1, -b, -alpha - 1, -color)
            if alpha < score < beta:
                score, _ = negascout(new_board, depth - 1, -beta, -score, -color)

        if alpha >= beta:
            # Add the current move to the killer move history
            killer_moves.append((piece, move))
            break

        value = -score
        if value > alpha:
            alpha = value
            best_move = (piece, move)

        if alpha >= beta:
            break
        b = alpha + 1

    # Reduce the move history for unplayed moves
    for piece, move in ordered_moves:
        target_square = (piece.x + move[0], piece.y + move[1])
        move_history[target_square[1]][target_square[0]] -= 1

    # Update the killer moves history
    killer_moves_history[depth] = killer_moves


    if not ordered_moves:
        return evaluate_board(board, color), None

    return alpha, best_move


zobrist = []
transposition_table = {}


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


def zobrist_hash(board):
    """
    Generate a unique hash for a board position using Zobrist hashing

    Hashing algorithm from Zobrist (1970)
    """
    hash_value = 0
    for y in range(8):
        for x in range(8):
            piece = board[y][x]  # Replace this with your own method to get the piece at a specific position
            if piece is not None:
                piece_type = piece.type_de_piece
                piece_color = piece.couleur

                # Map piece types and colors to corresponding integer values
                piece_type_mapping = {"roi": 0, "dame": 1, "tour": 2, "fou": 3, "cavalier": 4, "pion": 5}
                piece_color_mapping = {"blanc": 0, "noir": 1}

                piece_type_value = piece_type_mapping[piece_type]
                piece_color_value = piece_color_mapping[piece_color]
                square_index = y * 8 + x

                hash_value ^= zobrist[square_index][piece_type_value][piece_color_value]

    return hash_value


def get_transposition_entry(hash_value, color):
    if hash_value in transposition_table:
        return transposition_table[hash_value].get(color)
    return None


def store_transposition(hash_value, color, score):
    if hash_value not in transposition_table:
        transposition_table[hash_value] = {}
    transposition_table[hash_value][color] = score


def negascout(board, depth, alpha=float('-inf'), beta=float('inf'), color=1):
    if color == 1:
        couleur = "blanc"
    else:
        couleur = "noir"
    hash_value = zobrist_hash(board)
    cached_score = get_transposition_entry(hash_value, color)
    if cached_score is not None:
        return cached_score, None

    if depth == 0 or chess_utils.check_si_roi_restant(board) or chess_utils.check_si_echec_et_mat(board) == couleur:
        score = evaluate_board(board, color)
        store_transposition(hash_value, color, score)
        return score, None

    best_move = None
    b = beta


    all_moves = chess_utils.liste_coups_legaux(couleur, board)
    killer_moves = killer_moves_history[depth]  # Retrieve killer moves
    ordered_moves = move_ordering(all_moves, board, couleur, killer_moves)

    for piece, move in ordered_moves:
        new_board = copy.deepcopy(board)
        new_piece = copy.deepcopy(piece)
        new_board = new_piece.move(move[0], move[1], new_board)
        target_square = (piece.x + move[0], piece.y + move[1])
        target_piece = new_board[target_square[1]][target_square[0]]
        move_history[target_square[1]][target_square[0]] += 1

        if b == beta or b == alpha + 1:
            score, _ = negascout(new_board, depth - 1, -b, -alpha, -color)
        else:
            score, _ = negascout(new_board, depth - 1, -b, -alpha - 1, -color)
            if alpha < score < beta:
                score, _ = negascout(new_board, depth - 1, -beta, -score, -color)

        if alpha >= beta:
            killer_moves.append((piece, move))
            break

        value = -score
        if value > alpha:
            alpha = value
            best_move = (piece, move)

        if alpha >= beta:
            break
        b = alpha + 1

    for piece, move in ordered_moves:
        target_square = (piece.x + move[0], piece.y + move[1])
        move_history[target_square[1]][target_square[0]] -= 1

    killer_moves_history[depth] = killer_moves

    if not ordered_moves:
        score = evaluate_board(board, color)
        store_transposition(hash_value, color, score)
        return score, None

    store_transposition(hash_value, color, alpha)
    return alpha, best_move





















