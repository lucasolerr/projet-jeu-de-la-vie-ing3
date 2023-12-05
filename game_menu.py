import pygame
from game_engine import GameOfLife
from game_renderer import GameOfLifeGUI
from game_grid_size import GridSizeMenu

class GameMenu:
    def __init__(
        self,
        screen,
        items,
        background_image_path="image/fond_noel.jpg",
        font=None,
        font_size=100,
        font_color=(255, 255, 255),
        hover_color=(16, 25, 80),  # Couleur text hover
    ):
        self.screen = screen
        self.scr_width = self.screen.get_rect().width
        self.scr_height = self.screen.get_rect().height

        # image de fond
        self.background_image = pygame.image.load(background_image_path)

        # Gère l'écart entre le cadre de sélection et le texte de l'élément
        self.paddingx = 10
        self.paddingy = 20

        # Informe de l'écran actuel affiché
        self.start_selected = False
        self.settings_selected = False
        self.quit_select = False
        self.playing = False

        self.user_input = ""

        # Le premier élement sera sélectionné par défaut avec l'index 0.
        self.index_selected = 0

        self.font = pygame.font.Font(font, font_size)

        # Element sélectionné
        self.current_item = ()
        self.selected_action = None

        # Hover couleur
        self.hover_color = hover_color

        # Positionnement des éléments visuels
        self.menu_items = []

        for index, item in enumerate(items):
            label = self.font.render(item, 1, font_color)
            width = label.get_rect().width
            height = label.get_rect().height + 45

            posx = (self.scr_width / 2) - (width / 2)
            t_h = len(items) * height
            posy = (self.scr_height / 2) - (t_h / 2) + (index * height)

            self.menu_items.append([item, label, (width, height), (posx, posy)])

    def choose_grid_size(self):
        # Nouvelle fonction pour le sous-menu de sélection de la taille de la grille
        grid_size_menu = GridSizeMenu(self.screen, self)
        grid_size_menu.run()

    def run(self):
        # gère la boucle de menu, par défaut l'écran menu ne s'arrête jamais
        mainloop = True
        while mainloop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mainloop = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        if self.index_selected > 0:
                            self.index_selected -= 1

                    if event.key == pygame.K_ESCAPE:
                        mainloop = False

                    if event.key == pygame.K_DOWN:
                        if self.index_selected < (len(self.menu_items) - 1):
                            self.index_selected += 1

                    if event.key == pygame.K_RETURN:
                        if len(self.current_item) > 0:
                            self.selected_action = self.current_item[0]

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # Verifie le clique gauche de la souris
                    mouse_pos = event.pos
                    for index, (_, _, (width, height), (posx, posy)) in enumerate(
                        self.menu_items
                    ):
                        item_rect = pygame.Rect(
                            posx - self.paddingx,
                            posy - self.paddingy,
                            width + 2 * self.paddingx,
                            height + 2 * self.paddingy,
                        )
                        if item_rect.collidepoint(mouse_pos):
                            self.index_selected = index
                            self.current_item = self.menu_items[self.index_selected]
                            self.selected_action = self.current_item[0]
                            break

            self.current_item = self.menu_items[self.index_selected]
            scaled_background = pygame.transform.scale(
                self.background_image, (self.scr_width, self.scr_height)
            )
            self.screen.blit(scaled_background, (0, 0))

            for name, label, (width, height), (posx, posy) in self.menu_items:
                if self.current_item == [name, label, (width, height), (posx, posy)]:
                    label = self.font.render(name, 1, self.hover_color)
                else:
                    label = self.font.render(name, 1, (255, 255, 255))

                self.screen.blit(label, (posx, posy))
                name, label, (width, height), (posx, posy) = self.current_item

            if self.selected_action:
                if self.selected_action == "Jouer":
                    self.choose_grid_size()
                    if self.playing:
                        self.user_input = int(self.user_input)
                        game_launcher(self.user_input)
                        mainloop = False
                elif self.selected_action == "Charger":
                    game_launcher(load=True)
                    self.settings_selected = True
                    mainloop = False
                elif self.selected_action == "Quitter":
                    self.quit_select = True
                    mainloop = False

            pygame.display.flip()


def game_launcher(taille=50, load=False):
    game = GameOfLife(width=taille, height=taille)
    if load:
        game.load_from_file("game_state.txt")
    gui = GameOfLifeGUI(game)

    gui.run()