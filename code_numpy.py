import numpy as np
import pygame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import time
import scipy.signal


class GameOfLife:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = np.random.choice([0, 1], size=(height, width), p=[0.7, 0.3])

    def save_to_file(self, filename):
        np.savetxt(filename, self.board, fmt="%d")

    def load_from_file(self, filename):
        self.board = np.loadtxt(filename, dtype=int)

    def update_board(self):
        kernel = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])

        neighbors_count = scipy.signal.convolve2d(
            self.board, kernel, mode="same", boundary="fill", fillvalue=0
        )

        self.board = np.where(
            (self.board == 1) & ((neighbors_count < 2) | (neighbors_count > 3)),
            0,
            np.where(
                (self.board == 1) & ((neighbors_count == 2) | (neighbors_count == 3)),
                1,
                np.where((self.board == 0) & (neighbors_count == 3), 1, self.board),
            ),
        )


class GameOfLifeGUI:
    def __init__(self, game):
        self.game = game
        self.cell_size = min(1000 // game.width, 1000 // game.height)
        self.curve_color = (0, 0, 255)
        self.curve_width = 2
        self.width = self.game.width * self.cell_size
        self.height = self.game.height * self.cell_size
        self.screen = pygame.display.set_mode((1920, 1080))
        self.elapsed_time = list()
        self.alive_cells = list()
        pygame.display.set_caption("Game of Life")

        self.running = True
        self.update = False
        self.pause = False
        self.placement = False
        self.selected_structure = None
        self.clock = pygame.time.Clock()

        self.button_play_image = pygame.image.load("image/bouton_play.png")
        self.button_play_rect = self.button_play_image.get_rect()
        self.button_play_rect.topleft = (1292, 964)

        self.button_pause_image = pygame.image.load("image/bouton_pause.png")
        self.button_pause_rect = self.button_pause_image.get_rect()
        self.button_pause_rect.topleft = (1107, 964)

        self.button_save_image = pygame.image.load("image/bouton_save.png")
        self.button_save_rect = self.button_save_image.get_rect()
        self.button_save_rect.topleft = (1472, 964)

        self.button_load_image = pygame.image.load("image/bouton_load.png")
        self.button_load_rect = self.button_save_image.get_rect()
        self.button_load_rect.topleft = (1652, 964)

        self.deco_gauche_image = pygame.image.load("image/bois_cerf_gauche.png")
        self.deco_gauche_rect = self.deco_gauche_image.get_rect()
        self.deco_gauche_rect.topleft = (1083, 847)

        self.deco_droit_image = pygame.image.load("image/bois_cerf_droit.png")
        self.deco_droit_rect = self.deco_droit_image.get_rect()
        self.deco_droit_rect.topleft = (1199, 838)

        self.deco_bonnet_image = pygame.image.load("image/bonnet.png")
        self.deco_bonnet_rect = self.deco_bonnet_image.get_rect()
        self.deco_bonnet_rect.topleft = (1440, 876)

        self.deco_cadeau_image = pygame.image.load("image/cadeau.png")
        self.deco_cadeau_rect = self.deco_cadeau_image.get_rect()
        self.deco_cadeau_rect.topleft = (1282, 886)

        self.deco_pere_noel_image = pygame.image.load("image/pere_noel.png")
        self.deco_pere_noel_rect = self.deco_pere_noel_image.get_rect()
        self.deco_pere_noel_rect.topleft = (1646, 855)

        self.deco_guirlande_droit1_image = pygame.image.load(
            "image/guirlande_droit.png"
        )
        self.deco_guirlande_droit1_rect = self.deco_guirlande_droit1_image.get_rect()
        self.deco_guirlande_droit1_rect.topleft = (1815, 0)

        self.deco_guirlande_droit2_image = pygame.image.load(
            "image/guirlande_droit.png"
        )
        self.deco_guirlande_droit2_rect = self.deco_guirlande_droit2_image.get_rect()
        self.deco_guirlande_droit2_rect.topleft = (1815, 450)

        self.deco_guirlande_gauche1_image = pygame.image.load(
            "image/guirlande_gauche.png"
        )
        self.deco_guirlande_gauche1_rect = self.deco_guirlande_gauche1_image.get_rect()
        self.deco_guirlande_gauche1_rect.topleft = (0, 0)

        self.deco_guirlande_gauche2_image = pygame.image.load(
            "image/guirlande_gauche.png"
        )
        self.deco_guirlande_gauche2_rect = self.deco_guirlande_gauche2_image.get_rect()
        self.deco_guirlande_gauche2_rect.topleft = (0, 450)

    def place_generator(self, i, j):
        # Exemple de structure générateur (Gosper Glider Gun)
        gun = np.array(
            [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            ]
        )
        self.game.board[i : i + 8, j : j + 22] = gun

    def toggle_placement_mode(self):
        self.placement = not self.placement
        if self.placement:
            # switch sur la touche
            self.handle_keydown_event_placement()

    def update_cell_on_click(self, pos):
        # Convertir la position du clic en indices de tableau
        i, j = (pos[1] - 40) // self.cell_size, (pos[0] - 40) // self.cell_size

        if self.placement:
            self.place_generator(i, j)
        # Assurez-vous que les indices sont valides
        if 0 <= i < self.game.height and 0 <= j < self.game.width:
            # Inverser l'état de la cellule
            self.game.board[i, j] = 1 - self.game.board[i, j]

            # Redessiner la planche
            self.draw_board()

    def transition_between_state(self):
        if self.update:
            start_time = time.time()
            self.game.update_board()
            end_time = time.time()
            elapsed_time = (end_time - start_time) * 1000
            self.elapsed_time.append(elapsed_time)
            alive_cells_count = np.sum(self.game.board)
            self.alive_cells.append(alive_cells_count)
            print(f"Time taken for update: {elapsed_time:.4f} millis seconds")
            self.draw_board()
            self.draw_button()
            self.draw_curve(
                data=self.elapsed_time,
                x_label="Etapes",
                y_label="Temps exécutions (ms)",
            )
            self.draw_curve(
                self.alive_cells,
                x_label="Etapes",
                y_label="Nb cellules vivantes",
                offset=(1080, 450),
            )
            median_time = np.median(self.elapsed_time)
            self.draw_text(
                f"Temps médian d'exécution : {median_time:.2f} ms", (1080, 30)
            )
            nb_cell = np.sum(self.game.board)
            self.draw_text(f"Nb total de celulles : {nb_cell:.2f}", (1080, 450))
            self.update = False

    def draw_board(self):
        self.screen.fill((135, 206, 250))

        # Dessiner les cellules
        for i in range(self.game.height):
            for j in range(self.game.width):
                if self.game.board[i, j] == 1:
                    pygame.draw.rect(
                        self.screen,
                        (0, 0, 100),
                        (
                            j * self.cell_size + 40,
                            i * self.cell_size + 40,
                            self.cell_size,
                            self.cell_size,
                        ),
                    )

        # Dessiner la bordure autour de chaque cellule
        for i in range(self.game.height + 1):
            pygame.draw.line(
                self.screen,
                (0, 0, 0),
                (40, i * self.cell_size + 40),
                (40 + self.game.width * self.cell_size, i * self.cell_size + 40),
                1,
            )

        for j in range(self.game.width + 1):
            pygame.draw.line(
                self.screen,
                (0, 0, 0),
                (j * self.cell_size + 40, 40),
                (j * self.cell_size + 40, 40 + self.game.height * self.cell_size),
                1,
            )

    def draw_curve(
        self,
        data,
        width=2,
        x_label=None,
        y_label=None,
        offset=(1080, 10),
    ):
        fig, ax = plt.subplots(
            figsize=(8, 4), facecolor=(135 / 255, 206 / 255, 250 / 255)
        )
        ax.plot(data, linewidth=width)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)

        # Convertir le graphique en image Pygame
        canvas = FigureCanvas(fig)
        canvas.draw()

        size = canvas.get_width_height()
        image = pygame.image.fromstring(canvas.tostring_rgb(), size, "RGB")

        # Afficher l'image à la position spécifiée
        self.screen.blit(image, offset)

    def draw_button(self):
        self.screen.blit(self.button_play_image, self.button_play_rect)
        self.screen.blit(self.button_pause_image, self.button_pause_rect)
        self.screen.blit(self.button_save_image, self.button_save_rect)
        self.screen.blit(self.button_load_image, self.button_load_rect)

        self.screen.blit(self.deco_bonnet_image, self.deco_bonnet_rect)
        self.screen.blit(self.deco_gauche_image, self.deco_gauche_rect)
        self.screen.blit(self.deco_droit_image, self.deco_droit_rect)
        self.screen.blit(self.deco_pere_noel_image, self.deco_pere_noel_rect)
        self.screen.blit(self.deco_cadeau_image, self.deco_cadeau_rect)

        # self.screen.blit(self.deco_guirlande_droit1_image, self.deco_guirlande_droit1_rect)
        # self.screen.blit(self.deco_guirlande_droit2_image, self.deco_guirlande_droit2_rect)
        # self.screen.blit(self.deco_guirlande_gauche1_image, self.deco_guirlande_gauche1_rect)
        # self.screen.blit(self.deco_guirlande_gauche2_image, self.deco_guirlande_gauche2_rect)

    def draw_text(self, str, offset):
        font = pygame.font.Font(None, 36)
        text = font.render(str, True, (0, 0, 0))
        self.screen.blit(text, offset)

    def handle_quit_event(self):
        self.running = False

    def handle_mouse_click(self):
        if pygame.mouse.get_pressed()[0]:  # Left click
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if self.button_play_rect.collidepoint(mouse_x, mouse_y):
                # REPRISE DE LA SIMULATION
                self.pause = False
                print("Reprise de la simulation.")

            elif self.button_pause_rect.collidepoint(mouse_x, mouse_y):
                # MISE EN PAUSE DE LA SIMULATION
                self.pause = True
                print("Simulation en pause.")

            elif self.button_save_rect.collidepoint(mouse_x, mouse_y):
                # SAUVEGARDE DE LA GRILLE
                filename = "game_state.txt"
                self.game.save_to_file(filename)
                print(f"Game state saved to {filename}")

            elif self.button_load_rect.collidepoint(mouse_x, mouse_y):
                # CHARGEMENT DE LA GRILLE
                filename = "game_state.txt"
                self.game.load_from_file(filename)
                print(f"Game state loaded from {filename}")
                self.handle_return_key()
            else:
                self.update_cell_on_click(pygame.mouse.get_pos())

    def handle_keydown_event(self, event):
        if event.key == pygame.K_ESCAPE:
            self.handle_quit_event()
        elif event.key == pygame.K_r:
            self.reset_game_board()
        elif event.key == pygame.K_RETURN:
            self.handle_return_key()
        elif event.key == pygame.K_s:
            self.save_game_state()
        elif event.key == pygame.K_l:
            self.load_game_state()
        elif event.key == pygame.K_SPACE:
            self.pause = not self.pause
        elif event.key == pygame.K_g:
            self.placement = not self.placement

    def reset_game_board(self):
        self.game.board = np.zeros((self.height, self.width), dtype=int)

    def handle_return_key(self):
        self.update = True
        self.transition_between_state()

    def save_game_state(self):
        filename = "game_state.txt"
        self.game.save_to_file(filename)
        print(f"Game state saved to {filename}")

    def load_game_state(self):
        filename = "game_state.txt"
        self.game.load_from_file(filename)
        print(f"Game state loaded from {filename}")
        self.draw_board()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.handle_quit_event()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_click()
            elif event.type == pygame.KEYDOWN:
                self.handle_keydown_event(event)
            elif event.type == pygame.USEREVENT + 1:
                if self.pause == False:
                    self.update = True
                    self.transition_between_state()

    def run(self):
        self.handle_return_key()
        while self.running:
            self.handle_events()
            self.clock.tick(60)  # Adjust the speed as needed
            pygame.display.flip()


def jeu_principal(taille=50, load=False):
    game = GameOfLife(width=taille, height=taille)
    if load:
        game.load_from_file("game_state.txt")
    gui = GameOfLifeGUI(game)

    gui.run()


if __name__ == "__main__":
    pygame.init()

    game = GameOfLife(width=50, height=50)
    gui = GameOfLifeGUI(game)

    gui.run()

    pygame.quit()
