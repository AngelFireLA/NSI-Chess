#Material tables
piece_values = {
    "queen": 9,
    "rook": 5,
    "bishop": 3,
    "knight": 3,
}

material_table = {}

# Enumerate possible material constellations
for white_queen_count in range(3):
    for black_queen_count in range(3):
        for white_rook_count in range(3):
            for black_rook_count in range(3):
                for white_bishop_count in range(3):
                    for black_bishop_count in range(3):
                        for white_knight_count in range(3):
                            for black_knight_count in range(3):
                                # Calculate material value based on piece counts
                                material_value = (
                                    white_queen_count * piece_values["queen"]
                                    + black_queen_count * piece_values["queen"]
                                    + white_rook_count * piece_values["rook"]
                                    + black_rook_count * piece_values["rook"]
                                    + white_bishop_count * piece_values["bishop"]
                                    + black_bishop_count * piece_values["bishop"]
                                    + white_knight_count * piece_values["knight"]
                                    + black_knight_count * piece_values["knight"]
                                )
                                # Store the material value in the material table
                                material_table[
                                    (
                                        white_queen_count,
                                        black_queen_count,
                                        white_rook_count,
                                        black_rook_count,
                                        white_bishop_count,
                                        black_bishop_count,
                                        white_knight_count,
                                        black_knight_count,
                                    )
                                ] = material_value

# Example usage to access the score for a specific piece combination
queen_counts = (1, 0)  # Example: White has 1 queen, Black has 0 queens
rook_counts = (2, 1)   # Example: White has 2 rooks, Black has 1 rook

# Exclude kings from indexing
material_score = material_table[
    (
        queen_counts[0],
        queen_counts[1],
        rook_counts[0],
        rook_counts[1],
        0, 0, 0, 0
    )
]
print(f"Material Score for {queen_counts} and {rook_counts}: {material_score}")
