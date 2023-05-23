from typing import Tuple

import pygame


milieu = (50,50)
grille = []
for i in range (8):
  colonne = []
  ligne = []
  for j in range(8):
    ligne.append((milieu[0]+100*j, milieu[0]+100*i))
  grille.append(ligne)

def get_position(x, y):
  return grille[y][x]

def afficher(grid):
  combo = []
  for i in range(8):
    for j in range(8):
      if grid[i][j]:
        coordinates = grille[i][j]
        combo.append((grid[i][j], coordinates))
  return combo


def check_click(surfaces, event):
  if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button clicked
    mouse_pos = pygame.mouse.get_pos()  # Get current mouse position
    for surface, pos in surfaces:
      print(pos)
      if pos.collidepoint(mouse_pos):
        # Check if mouse position is within the surface
        print("yes")
        return surface, pos  # Store the selected surface
  return None  # Return None if no surface is clicked


def set_grille(grille):
  global plateau
  plateau = grille

plateau = []


def start():
  global plateau
  pygame.init()
  selected_piece = None
  fenetre = pygame.display.set_mode((1000, 800))

  perso = pygame.image.load("images/plateau jeu d'echec.png").convert_alpha()
  position_perso = perso.get_rect()

  while True:

    pieces = []
    fenetre.blit(perso, position_perso)

    for piece, pos in afficher(plateau):
      if piece:
        surface = pygame.image.load(f"images/{piece.type_de_piece} {piece.couleur}.png")
        position = surface.get_rect(center=(pos[0], pos[1]))
        fenetre.blit(surface, position)
        pieces.append((surface, position))  # Store the surface in the surfaces list

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        exit()

      selected_surface = check_click(pieces, event)
      if selected_surface:
        # Do something with the selected surface
        print("Selected surface:", selected_surface)

    pygame.display.flip()



