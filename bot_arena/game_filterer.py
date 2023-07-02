from stockfish import Stockfish

EQUAL_THRESHOLD = 20  # Adjust this value. Unit is in centipawns.
INPUT_FILE = 'positions.txt'  # Adjust path to your input file here.
OUTPUT_FILE = 'equal_positions.txt'  # Adjust path to your output file here.
STOCKFISH_PATH = 'stockfish-windows-x86-64-avx2.exe'  # Adjust path to your Stockfish binary here.
SEARCH_DEPTH = 16  # Adjust this value based on how deeply you want Stockfish to analyze.

stockfish = Stockfish(STOCKFISH_PATH, parameters={"Threads": 4, "Hash": 4096, "Minimum Thinking Time": 0}, depth=SEARCH_DEPTH)

with open(INPUT_FILE, 'r') as input_file, open(OUTPUT_FILE, 'a') as output_file:
    for fen in input_file:
        fen = fen.strip()  # Remove trailing newlines and any extra white space.
        if stockfish.is_fen_valid(fen):
            stockfish.set_fen_position(fen)
            evaluation = stockfish.get_evaluation()

            # Check if evaluation is in centipawns, otherwise probably a mating sequence.
            if evaluation['type'] == 'cp' and abs(evaluation['value']) <= EQUAL_THRESHOLD:
                print(fen)