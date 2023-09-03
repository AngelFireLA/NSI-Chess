def start_menu(partie):
    import pygame
    import pygame_menu
    import engine.partie
    import os

    partie: engine.partie.Partie

    # Initialize pygame
    pygame.init()

    # Set up the display
    WINDOW_SIZE = (1000, 800)
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Basic Menu Example")

    # Create a menu
    menu = pygame_menu.Menu('Main Menu', WINDOW_SIZE[0], WINDOW_SIZE[1], theme=pygame_menu.themes.THEME_BLUE)

    # Increase font size for the main menu
    menu_theme = menu.get_theme()
    menu_theme.title_font = pygame_menu.font.FONT_OPEN_SANS
    menu_theme.title_font_size = 50
    menu_theme.widget_font = pygame_menu.font.FONT_OPEN_SANS
    menu_theme.widget_font_size = 30

    # Function to start the game with Human vs. Human
    def start_human_vs_human():
        print("Starting Human vs. Human game")
        partie.mode = "manuel"
        partie.run()
        # Add your Human vs. Human game code here

    # Function to start the game with Human vs. Bot
    def start_human_vs_bot(user_data: dict):
        depth = user_data[list(user_data.keys())[0]]
        print(depth)
        depth = depth[0][1]
        color_choice = user_data[list(user_data.keys())[1]]
        color_choice = color_choice[0][1]

        print(f"Starting Human vs. Bot game ")
        print(f"Selected Starting Color: {color_choice}")
        print(f"Selected Level : {depth}")


        partie.depth = depth
        partie.mode = "semi-auto"
        partie.run(color_choice)


    # Create sub-menus for better organization
    human_vs_human_submenu = pygame_menu.Menu('Human vs. Human', WINDOW_SIZE[0], WINDOW_SIZE[1],
                                              theme=pygame_menu.themes.THEME_BLUE)

    # Increase font size for the sub-menu
    submenu_theme = human_vs_human_submenu.get_theme()
    submenu_theme.title_font = pygame_menu.font.FONT_OPEN_SANS
    submenu_theme.title_font_size = 40
    submenu_theme.widget_font = pygame_menu.font.FONT_OPEN_SANS
    submenu_theme.widget_font_size = 25

    human_vs_bot_submenu = pygame_menu.Menu('Human vs. Bot', WINDOW_SIZE[0], WINDOW_SIZE[1],
                                            theme=pygame_menu.themes.THEME_BLUE)

    # Increase font size for the sub-menu
    submenu_theme = human_vs_bot_submenu.get_theme()
    submenu_theme.title_font = pygame_menu.font.FONT_OPEN_SANS
    submenu_theme.title_font_size = 40
    submenu_theme.widget_font = pygame_menu.font.FONT_OPEN_SANS
    submenu_theme.widget_font_size = 60

    # Add buttons, text input, and color selection to the Human vs. Human submenu
    human_vs_human_submenu.add.button('Start', start_human_vs_human)

    # Add labels, text input, and color selection to the Human vs. Bot submenu
    human_vs_bot_submenu.add.selector('Bot Level: ', [('2', 2), ('3', 3), ('4', 4), ('5', 5), ('6', 6)], default=2)
    human_vs_bot_submenu.add.selector('Starting Color: ', [('Black', 'noir'), ('White', 'blanc')], default=0)
    human_vs_bot_submenu.add.button('Start', lambda: start_human_vs_bot(human_vs_bot_submenu.get_input_data()))

    # Add the sub-menus to the main menu
    menu.add.button('Play Human vs. Human', human_vs_human_submenu)
    menu.add.button('Play Human vs. Bot', human_vs_bot_submenu)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Update and draw the menu
        screen.fill((0, 0, 0))
        menu.mainloop(screen)

        pygame.display.update()