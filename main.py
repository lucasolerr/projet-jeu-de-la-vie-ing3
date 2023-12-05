import pygame
from game_menu import GameMenu

if __name__ == "__main__":
    # matplotlib.use("TkAgg")

    pygame.init()
    info = pygame.display.Info()
    screen = pygame.display.set_mode((info.current_w, info.current_h - 80))
    CLOCK_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(
        CLOCK_EVENT, 300
    )
    menu_items = ["Jouer", "Charger", "Quitter"]
    menu = GameMenu(screen, menu_items)
    menu.run()

