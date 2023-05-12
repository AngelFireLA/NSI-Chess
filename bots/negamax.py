# Define the evaluation function
from engine.pieces.piece import Roi
from engine.plateau import Plateau

points_noir = 0
points_blanc = 0
def evaluate_board(plateau: Plateau):
    return (points_noir - points_blanc) * 10

# Define the negamax algorithm
def negamax(board, depth, alpha, beta, color):
    if depth == 0:
        return color * evaluate_board(board)
    max_score = float('-inf')
    for move in board.legal_moves:
        board.push(move)
        score = -negamax(board, depth - 1, -beta, -alpha, -color)
        board.pop()
        max_score = max(max_score, score)
        alpha = max(alpha, score)
        if alpha >= beta:
            break
    return max_score

# Define the function to make a move using the negamax algorithm
def make_move(board: Plateau, depth, partie):
    best_score = float('-inf')
    best_move = None
    for move in board.liste_coups_legaux("noir"):
        print(move)
        board.grille = move[0].move(move[1][0][0], move[1][0][1], board.grille, partie)
        score = -negamax(board, depth - 1, float('-inf'), float('inf'), -1)
        board.pop()
        if score > best_score:
            best_score = score
            best_move = move
    return best_move

# Play the game
board = None

def init(plateau: Plateau, p_blancs, p_noir):
    global board, points_noir, points_blanc
    board = plateau
    points_noir = p_noir
    points_blanc = p_blancs