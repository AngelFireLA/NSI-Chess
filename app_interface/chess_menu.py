
def start_menu(fen="default"):
    import pygame
    import pygame_menu
    import os
    pygame.init()
    from core_engine.partie import Partie
    a = [[[1, 1], [1, -1], [-1, -1], [-1, 1]], [2, 1], [2, -1], [-2, 1], [-2, -1], [1, 2], [1, -2], [-1, 2], [-1, -2]]


    # Initialize pygame


    # Set up the display
    WINDOW_SIZE = (1200, 800)
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Jeux d'échecs")

    # Create a menu
    menu = pygame_menu.Menu('Menu Principal', WINDOW_SIZE[0], WINDOW_SIZE[1], theme=pygame_menu.themes.THEME_BLUE)

    # Increase font size for the main menu
    menu_theme = menu.get_theme()
    menu_theme.title_font = pygame_menu.font.FONT_OPEN_SANS
    menu_theme.title_font_size = 50
    menu_theme.widget_font = pygame_menu.font.FONT_OPEN_SANS
    menu_theme.widget_font_size = 30
    derniere_partie = False
    # Function to start the game with Human vs. Human
    def start_human_vs_human(user_data: dict):
        print("Starting Human vs. Human game")
        partie = Partie()
        loaded_fen = False
        if derniere_partie:
            load_last_game = user_data[list(user_data.keys())[0]]
            load_last_game = load_last_game[0][1]
            if load_last_game:
                # get content of dernière position.txt
                with open("dernière position.txt", "r") as f:
                    content = f.read()
                    loaded_fen = content
        if loaded_fen:
            partie.setup_from_fen(loaded_fen)
        else:
            partie.setup_from_fen(fen)
        partie.mode = "manuel"
        partie.run()
        # Add your Human vs. Human game code here

    # Function to start the game with Human vs. Bot
    def start_human_vs_bot(user_data: dict):
        depth = user_data[list(user_data.keys())[0]]
        depth = depth[0][1]
        color_choice = user_data[list(user_data.keys())[1]]
        color_choice = color_choice[0][1]

        print(f"Starting Human vs. Bot game ")
        print(f"Selected Starting Color: {color_choice}")
        print(f"Selected Level : {depth}")

        partie = Partie()
        partie.setup_from_fen(fen)
        partie.depth = depth
        partie.mode = "semi-auto"
        partie.run(color_choice)


    # Create sub-menus for better organization
    human_vs_human_submenu = pygame_menu.Menu('Humain vs. Humain', WINDOW_SIZE[0], WINDOW_SIZE[1],
                                              theme=pygame_menu.themes.THEME_BLUE)

    # Increase font size for the sub-menu
    submenu_theme = human_vs_human_submenu.get_theme()
    submenu_theme.title_font = pygame_menu.font.FONT_OPEN_SANS
    submenu_theme.title_font_size = 40
    submenu_theme.widget_font = pygame_menu.font.FONT_OPEN_SANS
    submenu_theme.widget_font_size = 25

    human_vs_bot_submenu = pygame_menu.Menu('Humain vs. Bot', WINDOW_SIZE[0], WINDOW_SIZE[1],
                                            theme=pygame_menu.themes.THEME_BLUE)

    # Increase font size for the sub-menu
    submenu_theme = human_vs_bot_submenu.get_theme()
    submenu_theme.title_font = pygame_menu.font.FONT_OPEN_SANS
    submenu_theme.title_font_size = 40
    submenu_theme.widget_font = pygame_menu.font.FONT_OPEN_SANS
    submenu_theme.widget_font_size = 60


    derniere_partie = os.path.exists("dernière position.txt")
    # Add labels, text input, and color selection to the Human vs. Bot submenu
    human_vs_bot_submenu.add.selector('Puissance du Bot: ', [('2', 2), ('3', 3), ('4', 4), ('5', 5), ('6', 6)], default=2)
    human_vs_bot_submenu.add.selector('Votre Couleur: ', [('Noirs', 'noir'), ('Blancs', 'blanc')], default=1)
    if derniere_partie:
        human_vs_bot_submenu.add.selector('Charger le plateau sauvegardé: ', [('Oui', True), ('Non', False)], default=1)
        human_vs_human_submenu.add.selector('Charger le plateau sauvegardé: ', [('Oui', True), ('Non', False)], default=1)


    human_vs_bot_submenu.add.button('Commencer la partie', lambda: start_human_vs_bot(human_vs_bot_submenu.get_input_data()))
    # Add buttons, text input, and color selection to the Human vs. Human submenu
    human_vs_human_submenu.add.button('Commencer la partie', lambda: start_human_vs_human(human_vs_human_submenu.get_input_data()))
    # Add the sub-menus to the main menu
    menu.add.button('Jouer Humain vs. Humain', human_vs_human_submenu)
    menu.add.button('Jouer Humain vs. Bot', human_vs_bot_submenu)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Update and draw the menu
        screen.fill((0, 0, 0))

        menu.mainloop(screen)

        pygame.display.update()