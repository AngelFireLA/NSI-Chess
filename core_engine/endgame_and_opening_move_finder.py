from core_engine.piece import Roi, Tour, Fou, Cavalier, Dame, Pion, Piece, Goku, Vegeta, Voleur, Imposteur


import time
import requests
import json
import os
parent_directory = os.getcwd()+"/core_engine/"

#Utilise l'api de lichess pour récupérer le meilleur coup de fin de partie
#Api obligatoire car pour 7 pièces restantes, c'est plus d'un terraoctet de stockage
def get_best_endgame_move_from_tablebase(board, couleur, variant="standard"):
    url = f"http://tablebase.lichess.ovh/{variant}"
    fen = board_to_fen(board, couleur)
    params = {"fen": fen}
    i = 0
    while True:
        response = requests.get(url, params=params)

        if response.status_code == 200:  # Successful response
            break
        elif response.status_code == 429:  # Too Many Requests
            print("Trop de requêtes par le bot, attendre 60 secondes.")
            time.sleep(60)  # Wait for 60 seconds
            i+=1
        else:
            print("Error:", response.status_code)
            return None
        if i == 3:
            return None

    try:
        data = json.loads(response.text)
    except:
        print("Error parsing response:", response.text)
        return None

    if "moves" in data:
        moves = data["moves"]
        if moves:
            best_move = moves[0]["uci"]
            return convert_move(best_move)

    return None

import chess
import chess.polyglot

#Récupère si possible un coup en provenance d'un énorme variété d'ouverture selon le plateau
def get_best_move_from_opening_book(grille, couleur):
    return None
    board = chess.Board(fen = board_to_fen(grille, couleur, status="ouverture"))
    import random
    with chess.polyglot.open_reader(parent_directory+"opening_book/codekiddy.bin") as reader:
        entries = list(reader.find_all(board))
        entries = [entry for entry in entries if entry.move != chess.Move.from_uci("c7c5")]

        if entries:
            total_weight = sum(entry.weight for entry in entries)
            random_weight = random.randint(1, total_weight)
            cumulative_weight = 0
            for entry in entries:
                cumulative_weight += entry.weight
                if cumulative_weight >= random_weight:
                    best_move = entry.move
                    break
            else:
                # If no move was selected (shouldn't happen unless all weights are 0),
                # you can handle it here, such as selecting a default move.
                with chess.polyglot.open_reader(parent_directory+"opening_book/book.bin") as reader1:
                    entries = list(reader1.find_all(board))
                    entries = [entry for entry in entries if entry.move != chess.Move.from_uci("e7e5")]

                    if entries:
                        total_weight = sum(entry.weight for entry in entries)
                        random_weight = random.randint(1, total_weight)
                        cumulative_weight = 0
                        for entry in entries:
                            cumulative_weight += entry.weight
                            if cumulative_weight >= random_weight:
                                best_move = entry.move
                                break
                        else:
                            # If no move was selected (shouldn't happen unless all weights are 0),
                            # you can handle it here, such as selecting a default move.
                            return None
                    else:
                        # If no opening moves are available, you can handle it here,
                        # such as selecting a default move.
                        return None
        else:
            # If no opening moves are available, you can handle it here,
            # such as selecting a default move.
            with chess.polyglot.open_reader(parent_directory+"opening_book/book.bin") as reader2:
                entries = list(reader2.find_all(board))
                entries = [entry for entry in entries if entry.move != chess.Move.from_uci("e7e5")]

                if entries:
                    total_weight = sum(entry.weight for entry in entries)
                    random_weight = random.randint(1, total_weight)
                    cumulative_weight = 0
                    for entry in entries:
                        cumulative_weight += entry.weight
                        if cumulative_weight >= random_weight:
                            best_move = entry.move
                            break
                    else:
                        # If no move was selected (shouldn't happen unless all weights are 0),
                        # you can handle it here, such as selecting a default move.
                        return None
                else:
                    # If no opening moves are available, you can handle it here,
                    # such as selecting a default move.
                    return None
    print(f"best move is {best_move}")
    return convert_move(best_move)


#Transforme la liste plateau en string FEN pour les fonctions le nécessitant
def board_to_fen(board, couleur, status="endgame", complet=True):
    fen = ''
    for row in board:
        empty_count = 0
        for square in row:
            if square is None:
                empty_count += 1
            else:
                if empty_count > 0:
                    fen += str(empty_count)
                    empty_count = 0
                piece_symbol = symbol_from_piece(square)
                fen += piece_symbol
        if empty_count > 0:
            fen += str(empty_count)
        fen += '/'
    fen = fen[:-1]  # Remove the trailing '/'
    if not complet:
        return fen
    if status == "ouverture":
        roc =  " KQkq - 0 1"
    else:
        roc = " - - 0 1"
    if couleur == "blanc":
        fen += ' w'+roc  # Append the active color and other FEN fields
    else:
        fen += ' b'+roc  # Append the active color and other FEN fields
    return fen

#CUSTOM TODO
def symbol_from_piece(piece):
    piece_symbol_dict = {
        Roi: 'K', Dame: 'Q', Tour: 'R', Fou: 'B', Cavalier: 'N', Pion: 'P', Goku: 'G', Vegeta: 'V', Voleur: 'T', Imposteur: 'I',
    }
    if piece.couleur == "noir":
        return piece_symbol_dict[type(piece)].lower()
    else:
        return piece_symbol_dict[type(piece)]

#Convertit un coup en notation chess en notation custom
def convert_move(chess_move):
    chess_move = str(chess_move)
    # Extract source and destination squares
    source_square = chess_move[:2]
    dest_square = chess_move[2:]

    # Convert squares to custom format
    source_coords = (int(source_square[1]) - 1, ord(source_square[0]) - ord('a'))
    dest_coords = (int(dest_square[1]) - 1, ord(dest_square[0]) - ord('a'))
    source_coords = (source_coords[1], 7-source_coords[0])
    dest_coords = (dest_coords[1]-source_coords[0], 7-dest_coords[0]-source_coords[1])

    return source_coords, dest_coords

def convert_custom_move(piece_class_move):
    piece_class, coords_change = piece_class_move
    x_change, y_change = coords_change

    original_pos = (piece_class.x,  piece_class.y)  # assuming you store the current position in 'position'

    # Create original and destination squares in tuple (x_change, y_change)
    orig_square_tuple = (original_pos[0], original_pos[1])
    dest_square_tuple = (x_change, y_change)


    # Consider that the chess board coordinates start from the bottom left as (0,0) while python 2D array starts from top left.
    orig_square_chess_notation = chr(ord('a') + orig_square_tuple[0]) + str(8 - orig_square_tuple[1])
    dest_square_chess_notation = chr(ord('a') + dest_square_tuple[0]) + str(8 - dest_square_tuple[1])

    chess_move = (orig_square_chess_notation, dest_square_chess_notation)
    return chess_move




