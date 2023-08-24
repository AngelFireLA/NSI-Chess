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
    points_blanc, points_noir = chess_utils.points(grid)
    score_blanc+=points_blanc*10
    score_noir+=points_noir*10

    #todo is checkmate
    if chess_utils.check_si_roi_restant(grid) == "blanc":
        score_blanc+=1000
    elif chess_utils.check_si_roi_restant(grid) == "noir":
        score_noir+=1000

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

    score_blanc += cases_par_couleur["blanc"]*0.5
    score_noir +=  cases_par_couleur["noir"]*0.5

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
        king_safety += 10 * pions
        king_safety += 5 * pion_par_colonne[1]
        king_safety += 5 * pion_par_colonne[0]
        king_safety += 5 * pion_par_colonne[-1]
        king_safety += score_de_position
        king_safety -= 25 * len([elem for elem in chess_utils.liste_pieces_dans_rayon(grid, roi.x, roi.y, 3) if
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


