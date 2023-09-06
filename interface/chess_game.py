import chess_utils
import pygame
import time
import engine.endgame_and_opening_move_finder as endgame_and_opening_move_finder
import bots.negamax as negamax
import os
import interface.button as button_library

from engine.pieces.piece import Roi

DEPTH = 4
#Position d'une pièces sur la case (0, 0)
initial_x = 50
initial_y = 50

#Calcule les coordonnées associées en pixels à chaque case sur le plateau
grille = []
for i in range (8):
  ligne = []
  for j in range(8):
    ligne.append((initial_x+100*j, initial_y+100*i))
  grille.append(ligne)

#Récupère toutes les pièces du plateau et leur coordonnées en pixels où elles devraient être
def afficher(grid):
  combo = []
  for i in range(8):
    for j in range(8):
      if grid[i][j]:
        coordinates = grille[i][j]
        combo.append((grid[i][j], coordinates))
  return combo

#Transforme les coordonnées x y allant de 0 à 7 en coordonées pixels
def coords_from_pixel(x, y):
  return(x-50)/100, (y-50)/100

#Vérifie si l'une des surfaces de la liste donnée à reçue un click gauche
def check_click(surfaces, event):
  if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button clicked
    mouse_pos = pygame.mouse.get_pos()  # Get current mouse position
    for surface, pos in surfaces:
      if pos.collidepoint(mouse_pos):
        # Check if mouse position is within the surface
        return surface, pos  # Store the selected surface
  return None  # Return None if no surface is clicked

plateau = []
#récupère le coup du bot, similaire à la fonction run() de Partie
def get_bot_move(grid, tour, depth, partie):

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
    if len(chess_utils.liste_pieces_bougeables(grid, tour)) + len(
            chess_utils.liste_pieces_bougeables(grid, chess_utils.couleur_oppose(
              tour))) <= 7 and not chess_utils.check_si_roi_restant(grid):
      meilleur_coup = endgame_and_opening_move_finder.get_best_endgame_move_from_tablebase(
        grid, tour)
      if meilleur_coup:
        piece, move = meilleur_coup
        best_score, best_combo = 69, (grid[piece[1]][piece[0]], move)
      else:

        # best_score, best_combo = negamax.negascout(grid, depth, color=couleur, alpha=-float('inf'), beta=float('inf'))
        best_score, best_combo = negamax.iterative_deepening_negamax(grid, couleur,
                                                                     depth, partie.temps_de_reflexion, partie_original=partie)

    else:

      # best_score, best_combo = negamax.negascout(grid, depth, color=couleur, alpha=-float('inf'), beta=float('inf'))
      best_score, best_combo = negamax.iterative_deepening_negamax(grid, couleur, depth, partie.temps_de_reflexion, partie_original=partie)
  if not best_combo:
    return None
  best_piece, best_move = best_combo
  end_time = time.time()
  total_time = end_time - start_time

  print(f"Bot played in {total_time} seconds thinking the current eval is {best_score}.")
  print()
  best_piece: Roi
  grid = best_piece.move(best_move[0], best_move[1], grid)
  partie.repetitions.append(negamax.zobrist_hash(partie.grille, partie.compteur_de_tour))

  surface = pygame.image.load(f"images/{best_piece.type_de_piece} {best_piece.couleur}.png")
  coords = grille[best_piece.y][best_piece.x]
  piece_rect = pygame.Rect(coords[0], coords[0], surface.get_width(), surface.get_height())
  from engine.endgame_and_opening_move_finder import convert_custom_move
  if best_piece.type_de_piece == "pion":
    partie.pgn+=f" {convert_custom_move((best_piece, best_move))[1]}"
  else:
    partie.pgn += f" {endgame_and_opening_move_finder.symbol_from_piece(best_piece)}{convert_custom_move((best_piece, best_move))[1]}"
  partie.compteur_de_tour+=1
  return (surface, piece_rect), grid

#Affiche un texte selon des paramètres
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


def start_partie(partie, start_tour:str="blanc"):
  global DEPTH
  DEPTH = partie.depth
  from engine.partie import Partie
  partie: Partie
  global plateau
  plateau = partie.grille
  pygame.init()
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
  negamax.init_transposition()

  button = pygame.image.load("images/button.png").convert_alpha()
  pressed_button = pygame.image.load("images/button_pressed.png").convert_alpha()
  cross_button = pygame.image.load("images/button_cross.svg").convert_alpha()
  button_library.set_button_images(button, pressed_button, cross_button)

  fen_button = button_library.Button(920, 750, 1, "Print FEN", fenetre, button, montrer=True, taille_texte=25, temps_animation=50)
  new_game_button = button_library.Button(920, 150, 1.1, "Nouvelle Partie", fenetre, button, montrer=True, taille_texte=25, temps_animation=50)
  save_game_button = button_library.Button(950, 650, 1.4, "Sauvegarder le plateau", fenetre, button, montrer=True, taille_texte=23, temps_animation=50)


  # Boucle principale du jeu
  while not partie.terminee:
    selected_squares.clear()
    pieces = []
    fenetre.fill((0, 0, 0))
    fenetre.blit(bg, position_bg)


    #Affiche à qui c'est le tour
    texte_combo = afficher_text(fenetre, f"Tour {partie.compteur_de_tour} : {partie.tour}", 810, 20, 50, "arial", couleur=(255, 255, 255))
    fenetre.blit(texte_combo[0], texte_combo[1])



    if selected:
      x, y = coords_from_pixel(selected[1].x, selected[1].y)
      x, y = int(x), int(y)
      if plateau[y][x]:
        selected_piece: Roi = plateau[y][x]
        if selected_piece.couleur ==partie.tour:
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
      # print(partie.pgn)

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
            # Send the message here
            converted_coords = tuple(map(int, coords_from_pixel(square_rect.centerx, square_rect.centery)))
            from engine.endgame_and_opening_move_finder import convert_custom_move
            if selected_piece.type_de_piece == "pion":
              partie.pgn+=f" {partie.compteur_de_tour}. {convert_custom_move((selected_piece, converted_coords))[1]}"
            else:
              partie.pgn+=f" {partie.compteur_de_tour}. {endgame_and_opening_move_finder.symbol_from_piece(selected_piece)}{convert_custom_move((selected_piece, converted_coords))[1]}"
            partie.grille = selected_piece.move(converted_coords[0] - selected_piece.x,
                                                converted_coords[1] - selected_piece.y, partie.grille)
            partie.repetitions.append(negamax.zobrist_hash(partie.grille, partie.compteur_de_tour))
            partie.compteur_de_tour+=1
            scores = chess_utils.points_avec_roi(partie.grille)
            if scores[0] == scores[1]:
              print(f"Tour numéro {partie.compteur_de_tour}. Le score est égal.")
            elif scores[0] > scores[1]:
                print(f"Tour numéro {partie.compteur_de_tour}. Le score est avantage blanc +{scores[0]-scores[1]}.")
            else:
                print(f"Tour numéro {partie.compteur_de_tour}. Le score est avantage noir +{scores[1]-scores[0]}.")
            selected_piece = None
            selected = None
            selected_squares.clear()
            partie.tour = chess_utils.couleur_oppose(partie.tour)
            break

      if check_click(pieces, event) and (partie.tour == start_tour or partie.mode == "manuel"):
        selected = check_click(pieces, event)
      #Si pas de pièces sont séléctionnée et que c'est aux noirs donc au bot
      elif not selected and partie.tour == chess_utils.couleur_oppose(start_tour) and partie.mode == "semi-auto":
        #Affiche le emssage d'attente pendant que le bot choisi le coup
        fenetre_originale = fenetre.copy()
        bot_reflechit = afficher_text(fenetre, "Le bot réfléchit au meilleur coup...",
                                      fenetre.get_width(), fenetre.get_height(), 50,
                                      "Impact", center=True)
        fenetre.blit(bot_reflechit[0], bot_reflechit[1])

        pygame.display.flip()

        bot_answer = get_bot_move(partie.grille, partie.tour, DEPTH, partie)
        #Si le bot retourne None c'est que la partie est finie
        if not bot_answer:
          if chess_utils.check_si_roi_restant(partie.grille):
            print(
              f"Partie terminée! Les vainqueurs sont les {chess_utils.check_si_roi_restant(partie.grille)} par capture du roi")
            partie.terminee = True
            pygame.quit()
            exit()

          if chess_utils.egalite(partie.grille, partie):
            print("Egalité ! Il ne reste que des rois sur le plateau.")
            partie.terminee = True
            pygame.quit()
            exit()

          raise ValueError("Le bot n'a pas trouvé de coup ?")

        # Restaure la fenêtre pygame
        fenetre.blit(fenetre_originale, (0, 0))
        pygame.display.update()
        partie.grille = bot_answer[1]
        partie.tour = chess_utils.couleur_oppose(partie.tour)

    partie.points_blanc, partie.points_noir = chess_utils.points(partie.grille)
    if chess_utils.check_si_roi_restant(partie.grille) and partie_finie:
      bot_reflechit = afficher_text(fenetre,
                                    f"Partie terminée! Les vainqueurs sont les {chess_utils.check_si_roi_restant(partie.grille)} par capture du roi",
                                    fenetre.get_width(),
                                    fenetre.get_height(), 30, "Impact", center=True, couleur=(255, 255, 255))
      fenetre.blit(bot_reflechit[0], bot_reflechit[1])
      pygame.display.flip()
      partie.terminee = True
      #print(partie.pgn)
      time.sleep(10)
    if chess_utils.check_si_roi_restant(partie.grille):
      partie_finie = True
      #print(partie.pgn)

    if chess_utils.egalite(partie.grille, partie):
      print("Egalité ! Il ne reste que des rois sur le plateau.")
      bot_reflechit = afficher_text(fenetre, "Egalité ! Il ne reste que des rois sur le plateau.", fenetre.get_width(),
                                    fenetre.get_height(), 35, "Impact", center=True, couleur=(255, 255, 255))
      fenetre.blit(bot_reflechit[0], bot_reflechit[1])
      pygame.display.flip()
      partie.terminee = True
      #print(partie.pgn)
      time.sleep(10)
    if chess_utils.egalite(partie.grille, partie):
      partie_finie = True
      #print(partie.pgn)


    pygame.display.flip()







