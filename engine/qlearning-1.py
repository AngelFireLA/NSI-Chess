import chess_utils
from lysandre.partie import Partie
from lysandre.pieces.piece import Roi

partie: Partie = None

def get_partie(p: Partie):
    global partie
    partie = p

def get_reward() -> int:



import numpy as np
import random

class QLearner:
    def __init__(self, alpha, gamma, epsilon, num_pieces, num_moves):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.num_pieces = num_pieces
        self.num_moves = num_moves
        self.q_table = np.zeros((num_pieces, num_moves))

    def get_action(self, state, legal_moves):
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(legal_moves)
        q_values = self.q_table[state]
        legal_q_values = [(i, q_values[i]) for i in legal_moves]
        print(legal_q_values)
        max_move = max(legal_q_values, key=lambda x: x[1])[0]
        return max_move

    def update(self, state, action, reward, next_state, next_legal_moves):
        max_next_q = max([self.q_table[next_state][a] for a in next_legal_moves])
        old_q_value = self.q_table[state][action]
        self.q_table[state][action] = old_q_value + self.alpha * (reward + self.gamma * max_next_q - old_q_value)

def main():
    num_pieces = 8
    num_moves = 8
    alpha = 0.1
    gamma = 0.99
    epsilon = 0.1
    num_episodes = 1000

    q_learner = QLearner(alpha, gamma, epsilon, num_pieces, num_moves)
    board = partie.plateau

    for episode in range(num_episodes):
        state_idx = None
        movable_pieces = board.liste_pieces_bougeables("noir")  # Get the list of movable pieces
        if movable_pieces:
            state_idx = random.randint(0, len(movable_pieces) - 1)
            state = movable_pieces[state_idx]
            legal_moves = state.liste_coups_legaux(board.grille)  # Get the legal moves for the selected piece
            while not legal_moves:
                movable_pieces = board.liste_pieces_bougeables("noir")
                if movable_pieces:
                    state_idx = random.randint(0, len(movable_pieces) - 1)
                    state = movable_pieces[state_idx]
                    legal_moves = state.liste_coups_legaux(board.grille)
        game_ended = False
        while not game_ended and state_idx is not None:
            action = q_learner.get_action(state_idx, legal_moves)
            piece = board.get_piece(state)
            piece.move(action)
            reward = get_reward(board)

            # Decide if the game has ended
            game_ended = partie.terminee

            if not game_ended:
                movable_pieces = board.liste_pieces_bougeables()  # Get the list of movable pieces
                if movable_pieces:
                    next_state_idx = random.randint(0, len(movable_pieces) - 1)
                    next_state = movable_pieces[next_state_idx]
                    next_legal_moves = next_state.liste_coups_legaux()  # Get the legal moves for the selected piece
                    q_learner.update(state_idx, action, reward, next_state_idx, next_legal_moves)
                    state_idx = next_state_idx
                    state = next_state
                    legal_moves = next_legal_moves
                else:
                    state_idx = None  # No movable pieces, exit the loop

#Partie exemple
partie = Partie()
partie.setup_from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")
main()






