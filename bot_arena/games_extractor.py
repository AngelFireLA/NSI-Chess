import chess.pgn, random, math

pgn = open("lichess_db_standard_rated_2013-01.pgn")
positions = []

for i in range(100000):
    print(i, flush=True, end=' ')
    game = chess.pgn.read_game(pgn)
    moves = game.mainline_moves()
    board = game.board()

    plyToPlay = math.floor(16 + 20 * random.random()) & ~1
    numPlyPlayed = 0
    for move in moves:
        board.push(move)
        numPlyPlayed += 1
        if numPlyPlayed == plyToPlay:
            fen = board.fen()

    numPiecesPoss = sum(fen.lower().count(piece) for piece in "nbrq")
    if numPlyPlayed > plyToPlay + 20 * 2 and numPiecesPoss >= 10:
        positions.append(fen)

with open("positions.txt", "w") as f:
    for string in positions:
        f.write(string + "\n")