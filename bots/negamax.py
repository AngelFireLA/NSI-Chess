# Define the evaluation function
import random

import chess_utils
from engine.pieces.piece import Roi, Piece, Pion
import copy

piece_values = {
    "pion": 1,
    "cavalier": 3,
    "fou": 3,
    "tour": 5,
    "dame": 9,
    "roi": 1000
}

multiplier = 1

carte_suretee_du_roi = [    [20*multiplier, 10*multiplier, 5*multiplier, 5*multiplier, 5*multiplier, 5*multiplier, 10*multiplier, 20*multiplier],
    [10*multiplier,  0*multiplier,  0*multiplier,  0*multiplier,  0*multiplier,  0*multiplier,  0*multiplier, 10*multiplier],
    [ 5*multiplier,  0*multiplier,  0*multiplier,  0*multiplier,  0*multiplier,  0*multiplier,  0*multiplier,  5*multiplier],
    [ 5*multiplier,  0*multiplier,  0*multiplier,  0*multiplier,  0*multiplier,  0*multiplier,  0*multiplier,  5*multiplier],
    [ 5*multiplier,  0*multiplier,  0*multiplier,  0*multiplier,  0*multiplier,  0*multiplier,  0*multiplier,  5*multiplier],
    [ 5*multiplier,  0*multiplier,  0*multiplier,  0*multiplier,  0*multiplier,  0*multiplier,  0*multiplier,  5*multiplier],
    [10*multiplier,  0*multiplier,  0*multiplier,  0*multiplier,  0*multiplier,  0*multiplier,  0*multiplier, 10*multiplier],
    [20*multiplier, 10*multiplier,  5*multiplier,  5*multiplier,  5*multiplier,  5*multiplier, 10*multiplier, 20*multiplier],
]

def get_couleur_str(couleur:int):
    couleur_str = None
    if couleur == 1:
        couleur_str = "blanc"
    elif couleur ==-1:
        couleur_str = "noir"
    return couleur_str

def evaluate_board(grid, couleur: int):

    score_blanc, score_noir = 0, 0
    #equilibre des points
    points_blanc, points_noir = chess_utils.points_avec_roi(grid)
    score_blanc+=points_blanc*10
    score_noir+=points_noir*10


    #cases controlees
    coups = {"blanc": chess_utils.liste_coups_legaux("blanc", grid),
             "noir": chess_utils.liste_coups_legaux("noir", grid)}
    cases_controlees = set()
    cases_par_couleur = {"blanc": 0, "noir": 0}
    for c in coups:
        for piece, coup in coups[c]:
            case = (piece.x + coup[0], piece.y + coup[1])
            if case not in cases_controlees:
                cases_controlees.add(case)
                cases_par_couleur[c] += 1

    score_blanc += cases_par_couleur["blanc"]*0.1
    score_noir +=  cases_par_couleur["noir"]*0.1

    #sureté du roi*
    for l in range(-1,2, 2):
        pieces = []
        for piece in chess_utils.liste_pieces_bougeables(grid, get_couleur_str(l)):
            if isinstance(piece, Roi):
                pieces.append(piece)

        if len(pieces) <1:
            continue
        roi: Roi = pieces[0]

        score_de_position = carte_suretee_du_roi[roi.y][roi.x]
        pions = 0
        pion_par_colonne = {-1: 0, 0: 0, 1: 0}
        if roi.couleur == "blanc":
            # count how many pion there is in the 3 squares in front of the king

            for i in range(-1, 2):
                if roi.y - 1 < 0:
                    break
                if roi.x + i < 0 or roi.x + i > 7:
                    break
                if grid[roi.y - 1][roi.x + i]:
                    pions += 1
                    pion_par_colonne[i] += 1
                if roi.y - 2 < 0:
                    continue
                if grid[roi.y - 2][roi.x + i]:
                    pions += 1
                    pion_par_colonne[i] += 1
        else:
            # count how many pion there is in the 3 squares in front of the king
            for i in range(-1, 2):
                if roi.y + 1 > 7:
                    break
                if roi.x + i < 0 or roi.x + i > 7:
                    break
                if grid[roi.y + 1][roi.x + i]:
                    pions += 1
                    pion_par_colonne[i] += 1
                if roi.y + 2 > 7:
                    continue
                if grid[roi.y + 2][roi.x + i]:
                    pions += 1
                    pion_par_colonne[i] += 1

        king_safety = 0


        valeur_pion_par_colonne = 0
        for k, v in pion_par_colonne.items():
            if v == 0:
                valeur_pion_par_colonne -= 5
            elif v == 1:
                valeur_pion_par_colonne += 10
            elif v == 2:
                valeur_pion_par_colonne += 20
            else:
                valeur_pion_par_colonne += 10 * v

        king_safety += valeur_pion_par_colonne

        king_safety += 10 * pions

        king_safety += score_de_position
        king_safety -= 25 * len([elem for elem in chess_utils.liste_pieces_dans_rayon(grid, roi.x, roi.y, 2) if
                                 elem.couleur != roi.couleur])
        king_safety -= 15 * len([elem for elem in chess_utils.liste_pieces_dans_rayon(grid, roi.x, roi.y, 3) if
                                 elem.type_de_piece == "dame"])
        if get_couleur_str(l) == "blanc":
            score_blanc+=king_safety
        else:
            score_noir+=king_safety

    #pion structure
    pion_structure_score = 0
    isolated_pions_score = 0
    doubled_pions_score = 0
    tripled_pions_score = 0
    pion_chain_score = 0

    pion_structure = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0}
    pions = [piece for piece in chess_utils.liste_pieces_bougeables(grid, "blanc") if isinstance(piece, Roi)]
    for pion in pions:
        pion_structure[pion.x] += 1


    # Calculate isolated pions
    for column in range(8):
        if pion_structure[column] > 0:
            if column == 0:
                if pion_structure[column + 1] == 0:
                    isolated_pions_score -= 20
            elif column == 7:
                if pion_structure[column - 1] == 0:
                    isolated_pions_score -= 20
            else:
                if pion_structure[column - 1] == 0 and pion_structure[column + 1] == 0:
                    isolated_pions_score -= 20

    # Calculate doubled and tripled pions
    for column in range(8):
        if pion_structure[column] > 1:
            doubled_pions_score -= 10 * (pion_structure[column] - 1)
        if pion_structure[column] > 2:
            tripled_pions_score -= 20 * (pion_structure[column] - 2)

    # Calculate pion chains
    for column in range(8):
        if pion_structure[column] > 0:
            if column == 0:
                if pion_structure[column + 1] > 0:
                    pion_chain_score += 10
            elif column == 7:
                if pion_structure[column - 1] > 0:
                    pion_chain_score += 10
            else:
                if pion_structure[column - 1] > 0 and pion_structure[column + 1] > 0:
                    pion_chain_score += 10



    pion_structure_score = isolated_pions_score + doubled_pions_score + tripled_pions_score + pion_chain_score

    return (score_blanc-score_noir)*couleur


def alpha_beta_pruning(board, depth, alpha=float('-inf'), beta=float('inf'), color=1):
    if depth == 0:
        return evaluate_board(board, color), None

    best_move = None
    best_value = float('-inf')
    if color == 1:
        couleur = "blanc"
    else:
        couleur = "noir"

    # Generate capturing and promotion moves
    capture_promotion_moves = [
        move for move in chess_utils.possible_captures_ou_promotions(couleur, board)
    ]

    # Sort the capturing/promotion moves in descending order based on captured piece value
    capture_promotion_moves.sort(
        key=lambda x: piece_values[chess_utils.get_piece_type(board, x[1][1], x[1][0])] - piece_values[
            x[0].type_de_piece]
        if chess_utils.get_piece_type(board, x[1][1], x[1][0]) is not None else 0,
        reverse=True,
    )

    # Generate all other legal moves
    other_moves = [
        (piece, move) for piece, move in chess_utils.liste_coups_legaux(couleur, board)
        if (piece, move) not in capture_promotion_moves
    ]

    random.shuffle(other_moves)  # shuffle the list of other_moves
    # Combine the capturing/promotion moves and other moves
    all_moves = capture_promotion_moves + other_moves

    for piece, move in all_moves:
        new_board = copy.deepcopy(board)
        new_piece = copy.deepcopy(piece)
        # create a new copy of the board
        new_board = new_piece.move(move[0], move[1], new_board)  # make the move on the new board
        score, _ = alpha_beta_pruning(new_board, depth - 1, -beta, -alpha, -color)
        value = -score
        if value > best_value:
            best_value = value
            best_move = (piece, move)

        alpha = max(alpha, value)

        if alpha >= beta:
            break

    if not all_moves:
        return evaluate_board(board, color), None

    return best_value, best_move

def negascout_original(board, depth, alpha=float('-inf'), beta=float('inf'), color=1):
    if depth == 0:
        return evaluate_board(board, color), None

    best_move = None
    b = beta
    if color == 1:
        couleur = "blanc"
    else:
        couleur = "noir"

    capture_promotion_moves = [
        move for move in chess_utils.possible_captures_ou_promotions(couleur, board)
    ]
    capture_promotion_moves.sort(
        key=lambda x: piece_values[chess_utils.get_piece_type(board, x[1][1], x[1][0])] - piece_values[
            x[0].type_de_piece]
        if chess_utils.get_piece_type(board, x[1][1], x[1][0]) is not None else 0,
        reverse=True,
    )

    other_moves = [
        (piece, move) for piece, move in chess_utils.liste_coups_legaux(couleur, board)
        if (piece, move) not in capture_promotion_moves
    ]
    random.shuffle(other_moves)
    all_moves = capture_promotion_moves + other_moves

    for piece, move in all_moves:
        new_board = copy.deepcopy(board)
        new_piece = copy.deepcopy(piece)
        new_board = new_piece.move(move[0], move[1], new_board)
        if b == beta or b == alpha + 1:
            score, _ = negascout(new_board, depth - 1, -b, -alpha, -color)
        else:
            score, _ = negascout(new_board, depth - 1, -b, -alpha - 1, -color)
            if alpha < score < beta:
                score, _ = negascout(new_board, depth - 1, -beta, -score, -color)

        value = -score
        if value > alpha:
            alpha = value
            best_move = (piece, move)

        if alpha >= beta:
            break
        b = alpha + 1

    if not all_moves:
        return evaluate_board(board, color), None

    return alpha, best_move


import random

def generate_zobrist_table():
    return [[random.randint(1, 2**64 - 1) for _ in range(64)] for _ in range(12)] # Assuming 12 unique pieces including both colors

zobrist_table = generate_zobrist_table()

piece_to_index = {
    'pion_blanc': 0,
    'pion_noir': 1,
    'tour_blanc': 2,
    'tour_noir': 3,
    'cavalier_blanc': 4,
    'cavalier_noir': 5,
    'fou_blanc': 6,
    'fou_noir': 7,
    'roi_blanc': 8,
    'roi_noir': 9,
    'dame_blanc': 10,
    'dame_noir': 11
}


def compute_zobrist_hash(board):
    zobrist_hash = 0
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece:
                index = piece_to_index[piece.type_de_piece+"_"+piece.couleur] # You must map each unique piece in your custom library to an index between 0 and 11 (inclusive)
                zobrist_hash ^= zobrist_table[index][row * 8 + col]
    return zobrist_hash

transposition_table = {}

def negascout(board, depth, alpha=float('-inf'), beta=float('inf'), color=1, zobrist_hash=None):
    if color == 1:
        couleur = "blanc"
    else:
        couleur = "noir"
    if depth == 0:
        return evaluate_board(board, color), None

    if zobrist_hash is None:
        zobrist_hash = compute_zobrist_hash(board)

    if zobrist_hash in transposition_table:
        entry = transposition_table[zobrist_hash]
        if entry[0] >= depth:
            return entry[1], entry[2]

    best_move = None
    b = beta

    capture_promotion_moves = [
        move for move in chess_utils.possible_captures_ou_promotions(couleur, board)
    ]
    capture_promotion_moves.sort(
        key=lambda x: piece_values[chess_utils.get_piece_type(board, x[1][1], x[1][0])] - piece_values[
            x[0].type_de_piece]
        if chess_utils.get_piece_type(board, x[1][1], x[1][0]) is not None else 0,
        reverse=True,
    )

    other_moves = [
        (piece, move) for piece, move in chess_utils.liste_coups_legaux(couleur, board)
        if (piece, move) not in capture_promotion_moves
    ]
    random.shuffle(other_moves)
    all_moves = capture_promotion_moves + other_moves

    first_child = True
    for piece, move in all_moves:
        new_board = copy.deepcopy(board)
        new_piece = copy.deepcopy(piece)
        new_board = new_piece.move(move[0], move[1], new_board)
        new_zobrist_hash = zobrist_hash ^ zobrist_table[piece_to_index[piece.type_de_piece+"_"+piece.couleur]][move[0] * 8 + move[1]] ^ zobrist_table[piece_to_index[piece.type_de_piece+"_"+piece.couleur]][move[0] * 8 + move[1]]
        if first_child:
            score, _ = negascout(new_board, depth - 1, -beta, -alpha, -color, new_zobrist_hash)
            first_child = False
        else:
            score, _ = negascout(new_board, depth - 1, -alpha - 1, -alpha, -color, new_zobrist_hash)
            if alpha < score < beta:
                score, _ = negascout(new_board, depth - 1, -beta, -score, -color, new_zobrist_hash)

        value = -score
        if value > alpha:
            alpha = value
            best_move = (piece, move)

        if alpha >= beta:
            break
        alpha = b + 1

    transposition_table[zobrist_hash] = (depth, alpha, best_move)

    if not all_moves:
        return evaluate_board(board, color), None

    return alpha, best_move





