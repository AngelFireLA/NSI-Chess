from pygame import font

import chess_utils
import pygame
import time
import engine.endgame_and_opening_move_finder as endgame_and_opening_move_finder
import bots.negamax as negamax


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
tour_num = 0
#récupère le coup du bot, similaire à la fonction run() de Partie
def get_bot_move(grid, tour, depth, partie):
  global tour_num
  alpha = -float('inf')
  beta = float('inf')

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
        negamax.init_transposition()
        # best_score, best_combo = negamax.negascout(grid, depth, color=couleur, alpha=-float('inf'), beta=float('inf'))
        best_score, best_combo = negamax.iterative_deepening_negamax(grid, couleur,
                                                                     depth, partie.temps_de_reflexion)

    else:
      negamax.init_transposition()
      # best_score, best_combo = negamax.negascout(grid, depth, color=couleur, alpha=-float('inf'), beta=float('inf'))
      best_score, best_combo = negamax.iterative_deepening_negamax(grid, couleur, depth, partie.temps_de_reflexion)
  if not best_combo:
    return None
  best_piece, best_move = best_combo
  print(best_score)
  end_time = time.time()
  total_time = end_time - start_time

  print(f"Time taken: {total_time} seconds")

  print(best_combo)
  best_piece: Roi
  chess_utils.montrer_grille(grid)
  grid = best_piece.move(best_move[0], best_move[1], grid)
  partie.compteur_de_tour+=1

  surface = pygame.image.load(f"images/{best_piece.type_de_piece} {best_piece.couleur}.png")
  coords = grille[best_piece.y][best_piece.x]
  piece_rect = pygame.Rect(coords[0], coords[0], surface.get_width(), surface.get_height())
  from engine.endgame_and_opening_move_finder import convert_custom_move
  if best_piece.type_de_piece == "pion":
    partie.pgn+=f" {convert_custom_move((best_piece, best_move))[1]}"
  else:
    partie.pgn += f" {endgame_and_opening_move_finder.symbol_from_piece(best_piece)}{convert_custom_move((best_piece, best_move))[1]}"
  tour_num+=1
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


#Fonctions pour jouer en 1 contre 1 manuellement
def start_manuel(partie):
  #Juste aide pour l'autocomplétion de pycharm
  from engine.partie import Partie
  partie:Partie

  global plateau
  plateau = partie.grille
  pygame.init()
  selected_piece = None
  fenetre = pygame.display.set_mode((1000, 800))

  bg = pygame.image.load("images/plateau jeu d'echec.png").convert_alpha()
  #Image qui va être superposée sur les cases sélectionnées
  selected_square = pygame.image.load("images/selected.png")
  position_bg = bg.get_rect()
  selected_squares = []
  selected = None
  partie.tour = "blanc"
  partie_finie = False

  while not partie.terminee:
    selected_squares.clear()
    pieces = []
    fenetre.fill((0, 0, 0))
    fenetre.blit(bg, position_bg)

    #Affiche à qui c'est le tour
    texte_combo = afficher_text(fenetre, f"Tour : {partie.tour} ", 810, 50, 40, "arial", couleur=(255, 255, 255))
    fenetre.blit(texte_combo[0], texte_combo[1])

    #Si une pièce à été clickée dessus
    if selected:
      x, y = coords_from_pixel(selected[1].x, selected[1].y)
      x, y = int(x), int(y)
      #Récupère la pièce sur le plateau
      if plateau[y][x]:
        selected_piece: Roi = plateau[y][x]
        #Empêche de jouer une pièce quand c'est pas notre tour
        if selected_piece.couleur ==partie.tour:
          for move in selected_piece.liste_coups_legaux(plateau):
            #Récupère toutes les cases sur lesquelles on pourrait se déplacer
            square_position = grille[selected_piece.y + move[1]][selected_piece.x + move[0]]
            square_rect = selected_square.get_rect(center=square_position)
            selected_squares.append(square_rect)
      else:
        print("Erreur, la pièce cliquée n'a pas d'équivalent sur le plateau")


    #Si il y a des cases où se déplacer (donc une pièce séléctionner), affiché ces cases
    if selected_squares:
      for square_rect in selected_squares:
        fenetre.blit(selected_square, square_rect)

    #Affiche toutes les pièces à leurs coordonnées
    for piece, pos in afficher(plateau):
      if piece:
        surface = pygame.image.load(f"images/{piece.type_de_piece} {piece.couleur}.png")
        position = surface.get_rect(center=(pos[0], pos[1]))
        fenetre.blit(surface, position)
        coords = pygame.Rect(pos[0], pos[1], surface.get_width(), surface.get_height())
        pieces.append((surface, coords))  # Store the surface in the surfaces list


    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        exit()

      #Vérifie si une pièce est cliquée
      if check_click(pieces, event):
        selected = check_click(pieces, event)

      if event.type == pygame.MOUSEBUTTONUP:
        mouse_pos = pygame.mouse.get_pos()
        for square_rect in selected_squares:
          #Vérifie si une des cases de mouvement possibles a été cliquée et déplace la pièce dans le plateau
          if square_rect.collidepoint(mouse_pos):
            # Send the message here
            converted_coords = tuple(map(int, coords_from_pixel(square_rect.centerx, square_rect.centery)))

            partie.grille = selected_piece.move(converted_coords[0]-selected_piece.x, converted_coords[1]-selected_piece.y, partie.grille)
            partie.compteur_de_tour+=1
            chess_utils.montrer_grille(partie.grille)
            #Reset les variables pour attendre la prochaine pièce à sélectionner
            selected_piece = None
            selected = None
            selected_squares.clear()
            partie.tour = chess_utils.couleur_oppose(partie.tour)
            moved = True
            break


    partie.points_blanc, partie.points_noir = chess_utils.points(partie.grille)
    # s'il ne reste pas au moins un roi de chaque couleur, ça termine la partie
    if chess_utils.check_si_roi_restant(partie.grille):
      partie_finie = True
    if chess_utils.check_si_roi_restant(partie.grille) and partie_finie:
      bot_reflechit = afficher_text(fenetre, f"Partie terminée! Les vainqueurs sont les {chess_utils.check_si_roi_restant(partie.grille)} par capture du roi", fenetre.get_width(),
                                    fenetre.get_height(), 36, "Impact", center=True, couleur=(255, 255, 255))
      fenetre.blit(bot_reflechit[0], bot_reflechit[1])
      pygame.display.flip()
      partie.terminee = True
      time.sleep(10)

    # s'il ne reste que des rois, ça termine la partie
    if chess_utils.roi_contre_roi(partie.grille):
      partie_finie = True
    if chess_utils.roi_contre_roi(partie.grille) and partie_finie:
      print("Egalité ! Il ne reste que des rois sur le plateau.")
      bot_reflechit = afficher_text(fenetre, "Egalité ! Il ne reste que des rois sur le plateau.", fenetre.get_width(),
                                    fenetre.get_height(), 40, "Impact", center=True, couleur=(255, 255, 255))
      fenetre.blit(bot_reflechit[0], bot_reflechit[1])
      pygame.display.flip()
      partie.terminee = True
      time.sleep(10)

    pygame.display.flip()


#Fonction qui lance le jeu en mode joueur contre bot
def start_semiauto(partie, start_tour:str):
  global DEPTH
  DEPTH = partie.depth
  from engine.partie import Partie
  partie: Partie
  global plateau
  global tour_num
  plateau = partie.grille
  pygame.init()
  selected_piece = None
  fenetre = pygame.display.set_mode((800, 800))

  bg = pygame.image.load("images/plateau jeu d'echec.png").convert_alpha()
  selected_square = pygame.image.load("images/selected.png")
  position_bg = bg.get_rect()
  selected_squares = []
  selected = None
  partie.tour = "blanc"
  moved = False
  bot_answer = None
  selected_bot = None
  partie_finie = False
  tour_num = 0

  while not partie.terminee:
    selected_squares.clear()
    pieces = []
    fenetre.blit(bg, position_bg)


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

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        exit()

      if event.type == pygame.MOUSEBUTTONUP:
        mouse_pos = pygame.mouse.get_pos()
        for square_rect in selected_squares:
          if square_rect.collidepoint(mouse_pos):
            # Send the message here
            print("Selected square:", coords_from_pixel(square_rect.center[0], square_rect.center[1]))
            converted_coords = tuple(map(int, coords_from_pixel(square_rect.centerx, square_rect.centery)))
            from engine.endgame_and_opening_move_finder import convert_custom_move
            if selected_piece.type_de_piece == "pion":
              partie.pgn+=f" {tour_num}. {convert_custom_move((selected_piece, converted_coords))[1]}"
            else:
              partie.pgn+=f" {tour_num}. {endgame_and_opening_move_finder.symbol_from_piece(selected_piece)}{convert_custom_move((selected_piece, converted_coords))[1]}"
            partie.grille = selected_piece.move(converted_coords[0] - selected_piece.x,
                                                converted_coords[1] - selected_piece.y, partie.grille)
            partie.compteur_de_tour+=1
            selected_piece = None
            selected = None
            selected_squares.clear()
            partie.tour = chess_utils.couleur_oppose(partie.tour)
            break

      if check_click(pieces, event) and partie.tour == start_tour:
        selected = check_click(pieces, event)
      #Si pas de pièces sont séléctionnée et que c'est aux noirs donc au bot
      elif not selected and partie.tour == chess_utils.couleur_oppose(start_tour):
        selected_bot = True
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

          if chess_utils.roi_contre_roi(partie.grille):
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
      print(partie.pgn)
      time.sleep(10)
    if chess_utils.check_si_roi_restant(partie.grille):
      partie_finie = True
      print(partie.pgn)

    if chess_utils.roi_contre_roi(partie.grille) and partie_finie.terminee:
      print("Egalité ! Il ne reste que des rois sur le plateau.")
      bot_reflechit = afficher_text(fenetre, "Egalité ! Il ne reste que des rois sur le plateau.", fenetre.get_width(),
                                    fenetre.get_height(), 35, "Impact", center=True, couleur=(255, 255, 255))
      fenetre.blit(bot_reflechit[0], bot_reflechit[1])
      pygame.display.flip()
      partie.terminee = True
      print(partie.pgn)
      time.sleep(10)
    if chess_utils.roi_contre_roi(partie.grille):
      partie_finie = True
      print(partie.pgn)


    pygame.display.flip()







