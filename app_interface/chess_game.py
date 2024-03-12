import time

import pygame

import app_interface.button as button_library
import bots.negamax as negamax
import chess_utils as c_u
import core_engine.endgame_and_opening_move_finder as endgame_and_opening_move_finder
from core_engine.endgame_and_opening_move_finder import convert_custom_move
from core_engine.piece import Roi

DEPTH = 4
# Position d'une pièces sur la case (0, 0)
initial_x = 50
initial_y = 50

# Calcule les coordonnées associées en pixels à chaque case sur le plateau
grille = []
for i in range(8):
    ligne = []
    for j in range(8):
        ligne.append((initial_x + 100 * j, initial_y + 100 * i))
    grille.append(ligne)


# Récupère toutes les pièces du plateau et leur coordonnées en pixels où elles devraient être
def afficher(grid):
    combo = []
    for i in range(8):
        for j in range(8):
            if grid[i][j]:
                coordinates = grille[i][j]
                combo.append((grid[i][j], coordinates))
    return combo


# Transforme les coordonnées x y allant de 0 à 7 en coordonées pixels
def coords_from_pixel(x, y):
    return (x - 50) / 100, (y - 50) / 100


# Vérifie si l'une des surfaces de la liste donnée à reçue un click gauche
def check_click(surfaces, event):
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button clicked
        mouse_pos = pygame.mouse.get_pos()  # Get current mouse position
        for surface, pos in surfaces:
            if pos.collidepoint(mouse_pos):
                # Check if mouse position is within the surface
                return surface, pos  # Store the selected surface
    return None  # Return None if no surface is clicked


plateau = []


# récupère le coup du bot, similaire à la fonction run() de Partie
def get_bot_move(grid, tour, depth, partie, bot):
    # call negamax to find the best move
    if tour == "blanc":
        couleur = 1
    else:
        couleur = -1
    start_time = time.time()
    opening = endgame_and_opening_move_finder.get_best_move_from_opening_book(grid, tour)

    if opening:
        piece, move = opening
        best_score, best_combo = 69, (grid[piece[1]][piece[0]], move)
    else:
        if len(c_u.liste_pieces_bougeables(grid, tour)) + len(
                c_u.liste_pieces_bougeables(grid, c_u.couleur_oppose(
                    tour))) <= 7 and not c_u.check_si_roi_restant(grid):
            meilleur_coup = endgame_and_opening_move_finder.get_best_endgame_move_from_tablebase(
                grid, tour)
            if meilleur_coup:
                piece, move = meilleur_coup
                best_score, best_combo = 69, (grid[piece[1]][piece[0]], move)
            else:

                best_score, best_combo = bot.iterative_deepening_negamax(grid, couleur,
                                                                             depth, partie.temps_de_reflexion,
                                                                             partie_original=partie)

        else:

            best_score, best_combo = bot.iterative_deepening_negamax(grid, couleur, depth,
                                                                         partie.temps_de_reflexion,
                                                                         partie_original=partie)
    if not best_combo:
        return None
    best_piece, best_move = best_combo
    end_time = time.time()
    total_time = end_time - start_time

    print(f"Bot played in {total_time} seconds thinking the current eval is {best_score}.")
    print()
    best_piece: Roi
    print(best_combo, (best_piece.x, best_piece.y))
    from core_engine.endgame_and_opening_move_finder import convert_custom_move
    if best_piece.type_de_piece == "pion":
        partie.pgn += f" {convert_custom_move(best_piece, (best_move[0]+best_piece.x,best_piece.y + best_move[1]))[1]}"
    else:
        partie.pgn += f" {endgame_and_opening_move_finder.symbol_from_piece(best_piece).upper()}{convert_custom_move(best_piece, (best_move[0]+best_piece.x,best_piece.y + best_move[1]))[1]}"
    print(partie.pgn)
    grid = best_piece.move(best_move[0], best_move[1], grid)
    partie.grilles.append(c_u.copy_grille(grid))
    if len(partie.grilles) > 1 and len(
            c_u.liste_pieces_restantes(partie.grilles[-1])) < len(
        c_u.liste_pieces_restantes(partie.grilles[-2])):
        # play audio/capture.mp3
        print("played")
        pygame.mixer.music.load("audio/capture.mp3")
        pygame.mixer.music.play()
    else:
        # play audio/move.mp3
        pygame.mixer.music.load("audio/move-self.mp3")
        pygame.mixer.music.play()
    surface = pygame.image.load(f"images/{best_piece.type_de_piece} {best_piece.couleur}.png")
    coords = grille[best_piece.y][best_piece.x]
    piece_rect = pygame.Rect(coords[0], coords[0], surface.get_width(), surface.get_height())
    return (surface, piece_rect), grid


# Affiche un texte selon des paramètres
def afficher_text(fenetre, texte: str, x: int, y: int, taille, font_choisi: str, couleur=(0, 0, 0), center=False):
    fontt = pygame.font.SysFont(font_choisi, taille)
    text_surface = fontt.render(texte, True, couleur)
    if center:
        text_x = (fenetre.get_width() - text_surface.get_width()) // 2
        text_y = (fenetre.get_height() - text_surface.get_height()) // 2
    else:
        text_x = x
        text_y = y

    return text_surface, (text_x, text_y)


def start_partie(partie, start_tour: str = "blanc", bot=None):
    global DEPTH
    DEPTH = partie.depth
    from core_engine.partie import Partie
    partie: Partie
    global plateau
    plateau = partie.grille
    pygame.init()
    pygame.mixer.init()
    selected_piece = None
    fenetre = pygame.display.set_mode((1200, 800))

    bg = pygame.image.load("images/plateau jeu d'echec.png").convert_alpha()
    selected_square = pygame.image.load("images/selected.png")
    position_bg = bg.get_rect()
    selected_squares = []
    selected = None
    partie.tour = "blanc"
    bot_answer = None
    partie_finie = False

    button = pygame.image.load("images/button.png").convert_alpha()
    pressed_button = pygame.image.load("images/button_pressed.png").convert_alpha()
    left_arrow_button = pygame.image.load("images/left_arrow.png").convert_alpha()
    right_arrow_button = pygame.image.load("images/right_arrow.png").convert_alpha()

    cross_button = pygame.image.load("images/button_cross.svg").convert_alpha()
    button_library.set_button_images(button, pressed_button, cross_button, left_arrow_button, right_arrow_button)

    fen_button = button_library.Button(920, 750, 1, "Print FEN", fenetre, button, montrer=True, taille_texte=25,
                                       temps_animation=50)
    new_game_button = button_library.Button(920, 150, 1.1, "Nouvelle Partie", fenetre, button, montrer=True,
                                            taille_texte=25, temps_animation=50)
    save_game_button = button_library.Button(950, 650, 1.4, "Sauvegarder le plateau", fenetre, button, montrer=True,
                                             taille_texte=23, temps_animation=50)
    previous_board_button = button_library.Button(950, 550, 0.25, "", fenetre, button_type=left_arrow_button,
                                                  montrer=False)
    next_board_button = button_library.Button(1050, 550, 0.25, "", fenetre, button_type=right_arrow_button,
                                              montrer=False)
    partie.grilles.append(c_u.copy_grille(partie.grille))
    if not bot:
        bot = negamax.Bot("negamax")
    # Boucle principale du jeu
    while not partie.terminee:
        selected_squares.clear()
        pieces = []
        fenetre.fill((0, 0, 0))
        fenetre.blit(bg, position_bg)

        # Affiche à qui c'est le tour
        texte_combo = afficher_text(fenetre, f"Tour {partie.compteur_de_tour} : {partie.tour}", 810, 20, 50, "arial",
                                    couleur=(255, 255, 255))
        fenetre.blit(texte_combo[0], texte_combo[1])

        if selected:
            x, y = coords_from_pixel(selected[1].x, selected[1].y)
            x, y = int(x), int(y)
            if plateau[y][x]:
                selected_piece: Roi = plateau[y][x]
                if selected_piece.couleur == partie.tour:
                    for move in selected_piece.liste_coups_legaux(plateau):
                        square_position = grille[selected_piece.y + move[1]][selected_piece.x + move[0]]
                        square_rect = selected_square.get_rect(center=square_position)
                        selected_squares.append(square_rect)
            else:
                print("Erreur, la pièce cliquée n'a pas d'équivalent sur le plateau")

        if selected_squares:
            for square_rect in selected_squares:
                fenetre.blit(selected_square, square_rect)

        for piece, pos in afficher(plateau):
            if piece:
                surface = pygame.image.load(f"images/{piece.type_de_piece} {piece.couleur}.png")
                position = surface.get_rect(center=(pos[0], pos[1]))
                fenetre.blit(surface, position)
                coords = pygame.Rect(pos[0], pos[1], surface.get_width(), surface.get_height())
                pieces.append((surface, coords))  # Store the surface in the surfaces list

        if new_game_button.draw():
            new_game_text = afficher_text(fenetre,
                                          f"Partie terminée!",
                                          fenetre.get_width(),
                                          fenetre.get_height(), 60, "Impact", center=True, couleur=(255, 255, 255))
            fenetre.blit(new_game_text[0], new_game_text[1])
            pygame.display.flip()
            pygame.time.delay(3000)
            partie = None
            break

        if fen_button.draw():
            print(endgame_and_opening_move_finder.board_to_fen(partie.grille, partie.tour))

        if save_game_button.draw():
            with open("dernière position.txt", "w") as f:
                f.write(endgame_and_opening_move_finder.board_to_fen(partie.grille, partie.tour, complet=False))

                print("Plateau sauvegardé")
                board_saved_text = afficher_text(fenetre,
                                                 f"Plateau sauvegardé",
                                                 820,
                                                 690, 25, "Impact", center=False, couleur=(255, 255, 255))
                fenetre.blit(board_saved_text[0], board_saved_text[1])
                pygame.display.flip()
                pygame.time.delay(1000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                for square_rect in selected_squares:
                    if square_rect.collidepoint(mouse_pos):
                        converted_coords = tuple(map(int, coords_from_pixel(square_rect.centerx, square_rect.centery)))
                        if partie.compteur_de_tour%2 == 0:
                            if selected_piece.type_de_piece == "pion":
                                partie.pgn += f" {partie.compteur_de_tour//2+1}. {convert_custom_move(selected_piece, converted_coords)[1]}"
                            else:
                                partie.pgn += f" {partie.compteur_de_tour//2+1}. {endgame_and_opening_move_finder.symbol_from_piece(selected_piece).upper()}{convert_custom_move(selected_piece, converted_coords)[1]}"
                        else:
                            if selected_piece.type_de_piece == "pion":
                                partie.pgn += f" {convert_custom_move(selected_piece, converted_coords)[1]}"
                            else:
                                partie.pgn += f" {endgame_and_opening_move_finder.symbol_from_piece(selected_piece).upper()}{convert_custom_move(selected_piece, converted_coords)[1]}"
                        partie.compteur_de_tour += 1
                        resulting_grille = selected_piece.move(converted_coords[0] - selected_piece.x,
                                                               converted_coords[1] - selected_piece.y,
                                                               partie.grille)
                        partie.grilles.append(c_u.copy_grille(resulting_grille))

                        if len(partie.grilles) > 1 and len(
                                c_u.liste_pieces_restantes(partie.grilles[-1])) < len(
                            c_u.liste_pieces_restantes(partie.grilles[-2])):
                            # play audio/capture.mp3
                            print("played")
                            pygame.mixer.music.load("audio/capture.mp3")
                            pygame.mixer.music.play()
                        else:
                            # play audio/move.mp3
                            pygame.mixer.music.load("audio/move-self.mp3")
                            pygame.mixer.music.play()

                        partie.repetitions.append(bot.zobrist_hash(partie.grille, partie.compteur_de_tour))
                        score = int(bot.evaluate_board(partie.grille, c_u.get_couleur_int(partie.tour)))
                        if score == 0:
                            print(f"Tour numéro {partie.compteur_de_tour}. Le score est égal.")
                        elif score > 0:
                            print(
                                f"Tour numéro {partie.compteur_de_tour}. Le score est avantage {partie.tour} +{score}.")
                        else:
                            print(
                                f"Tour numéro {partie.compteur_de_tour}. Le score est avantage {c_u.couleur_oppose(partie.tour)} +{abs(score)}.")
                        selected_piece = None
                        selected = None
                        selected_squares.clear()
                        partie.tour = c_u.couleur_oppose(partie.tour)
                        print(partie.pgn)
                        break

            if check_click(pieces, event) and (partie.tour == start_tour or partie.mode == "manuel"):
                selected = check_click(pieces, event)
            # Si pas de pièces sont séléctionnée et que c'est aux noirs donc au bot
            elif not selected and partie.tour == c_u.couleur_oppose(start_tour) and partie.mode == "semi-auto":
                # Affiche le emssage d'attente pendant que le bot choisi le coup
                fenetre_originale = fenetre.copy()
                bot_reflechit = afficher_text(fenetre, "Le bot réfléchit au meilleur coup...",
                                              fenetre.get_width(), fenetre.get_height(), 50,
                                              "Impact", center=True)
                fenetre.blit(bot_reflechit[0], bot_reflechit[1])

                pygame.display.flip()

                bot_answer = get_bot_move(partie.grille, partie.tour, DEPTH, partie, bot)
                # Si le bot retourne None c'est que la partie est finie
                if not bot_answer:
                    if c_u.check_si_roi_restant(partie.grille):
                        print(
                            f"Partie terminée! Les vainqueurs sont les {c_u.check_si_roi_restant(partie.grille)} par capture du roi")
                        # partie.terminee = True
                        pygame.quit()
                        exit()

                    if c_u.egalite(partie.grille, partie):
                        print("Egalité ! Il ne reste que des rois sur le plateau.")
                        # partie.terminee = True
                        pygame.quit()
                        exit()

                    raise ValueError("Le bot n'a pas trouvé de coup ?")

                # Restaure la fenêtre pygame
                fenetre.blit(fenetre_originale, (0, 0))
                pygame.display.update()
                partie.compteur_de_tour += 1
                partie.repetitions.append(bot.zobrist_hash(partie.grille, partie.compteur_de_tour))
                partie.tour = c_u.couleur_oppose(partie.tour)

        partie.points_blanc, partie.points_noir = c_u.points(partie.grille)
        if c_u.check_si_roi_restant(partie.grille) and partie_finie:
            bot_reflechit = afficher_text(fenetre,
                                          f"Partie terminée! Les vainqueurs sont les {c_u.check_si_roi_restant(partie.grille)} par capture du roi",
                                          fenetre.get_width(),
                                          fenetre.get_height(), 30, "Impact", center=True, couleur=(255, 255, 255))
            fenetre.blit(bot_reflechit[0], bot_reflechit[1])
            pygame.display.flip()
            partie.terminee = True

            # print(partie.pgn)
            time.sleep(10)
        if c_u.check_si_roi_restant(partie.grille):
          partie_finie = True
        # print(partie.pgn)

        if c_u.egalite(partie.grille, partie):
            print("Egalité ! Il ne reste que des rois sur le plateau.")
            bot_reflechit = afficher_text(fenetre, "Egalité ! Il ne reste que des rois sur le plateau.",
                                          fenetre.get_width(),
                                          fenetre.get_height(), 35, "Impact", center=True, couleur=(255, 255, 255))
            fenetre.blit(bot_reflechit[0], bot_reflechit[1])
            pygame.display.flip()
            # partie.terminee = True
            # print(partie.pgn)
            time.sleep(10)
        if c_u.egalite(partie.grille, partie):
            partie_finie = True
            # print(partie.pgn)

        pygame.display.flip()
