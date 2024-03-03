import pygame


def set_button_images(button_surface, pressed_button_surface, cross_button_surface, left_arrow_surface, right_arrow_surface):
    global button, pressed_button, cross_button,  left_arrow, right_arrow
    button = button_surface
    pressed_button = pressed_button_surface
    cross_button = cross_button_surface
    left_arrow = left_arrow_surface
    right_arrow = right_arrow_surface



class Button:

    def __init__(self, x, y, taille, texte, fenetre, button_type, couleur_texte=None, taille_texte=36,  montrer=True, temps_animation=100, background_color=None):
        self.largeur = button_type.get_width()
        self.hauteur = button_type.get_height()
        self.image = pygame.transform.scale(button_type, (int(self.largeur * taille), int(self.hauteur * taille)))
        self.pressed_image = pygame.transform.scale(pressed_button, (int(self.largeur * taille), int(self.hauteur * taille)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.texte = texte
        self.couleur_texte = couleur_texte
        self.taille_texte = taille_texte
        self.button_type = button_type
        self.fenetre = fenetre
        self.montrer = montrer
        self.temps_animation = temps_animation
        self.clicked = False

    def placer_texte(self, x, y, text, size, color=None):
        font = pygame.font.Font(pygame.font.get_default_font(), size)
        if color:
            text = font.render(text, True, color)
        else:
            text = font.render(text, True, (150, 150, 150))
        self.fenetre.blit(text, text.get_rect(center=(x, y)))

    def draw(self):
        action = False
        if self.montrer:
            pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(pos)and pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                #Si c'est un boutton en bar, on démarre l'animation
                if self.button_type == button:

                    self.fenetre.blit(self.pressed_image, (self.rect.x, self.rect.y + 5))
                    self.placer_texte(self.rect.center[0], self.rect.center[1] + 5, self.texte, self.taille_texte,
                                      (0, 0, 0))
                    pygame.display.update()
                    pygame.time.delay(self.temps_animation)
                    self.fenetre.blit(self.image, (self.rect.x, self.rect.y))
                    self.placer_texte(self.rect.center[0], self.rect.center[1], self.texte, self.taille_texte,
                                      (0, 0, 0))
                    pygame.display.update()
                    pygame.time.delay(self.temps_animation)

                action = True

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
            self.fenetre.blit(self.image, (self.rect.x, self.rect.y))
            #si c'est un boutton eb barre, afficher le texte nécessaire
            if self.button_type == button:
                self.placer_texte(self.rect.center[0], self.rect.center[1], self.texte, self.taille_texte, (0, 0, 0))

        return action

    def initier_click(self):
        self.fenetre.blit(self.pressed_image, (self.rect.x, self.rect.y + 5))
        self.placer_texte(self.rect.center[0], self.rect.center[1] + 5, self.texte, self.taille_texte, (0, 0, 0))
        pygame.display.update()
        pygame.time.delay(1000)
        self.fenetre.blit(self.image, (self.rect.x, self.rect.y))
        self.placer_texte(self.rect.center[0], self.rect.center[1], self.texte, self.taille_texte, (0, 0, 0))
        pygame.display.update()
        return True