import numpy as np
import pygame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import time


class GameOfLifeGUI:
    def __init__(self, game):
        self.game = game
        self.cell_size = min(1000 // game.width, 1000 // game.height)
        self.curve_color = (0, 0, 255)
        self.curve_width = 2
        self.width = self.game.width * self.cell_size
        self.height = self.game.height * self.cell_size
        self.screen = pygame.display.set_mode((1920, 1080))
        self.elapsed_time = []
        self.alive_cells = []
        pygame.display.set_caption("Game of Life")
        self.running = True
        self.update = False
        self.pause = False
        self.placement = False
        self.placement_gun = False
        self.placement_pentadecatlon = False
        self.placement_spaceship = False
        self.placement_tub = False
        self.placement_beacon = False
        self.selected_structure = None
        self.clock = pygame.time.Clock()

        self.load_images()
        self.set_button_positions()

    def load_images(self):
        self.button_play_image = pygame.image.load("image/bouton_play.png")
        self.button_pause_image = pygame.image.load("image/bouton_pause.png")
        self.button_save_image = pygame.image.load("image/bouton_save.png")
        self.button_load_image = pygame.image.load("image/bouton_load.png")
        self.deco_gauche_image = pygame.image.load("image/bois_cerf_gauche.png")
        self.deco_droit_image = pygame.image.load("image/bois_cerf_droit.png")
        self.deco_bonnet_image = pygame.image.load("image/bonnet.png")
        self.deco_cadeau_image = pygame.image.load("image/cadeau.png")
        self.deco_pere_noel_image = pygame.image.load("image/pere_noel.png")

    def set_button_positions(self):
        self.button_play_rect = self.button_play_image.get_rect(topleft=(1292, 964))
        self.button_pause_rect = self.button_pause_image.get_rect(topleft=(1107, 964))
        self.button_save_rect = self.button_save_image.get_rect(topleft=(1472, 964))
        self.button_load_rect = self.button_load_image.get_rect(topleft=(1652, 964))
        self.deco_gauche_rect = self.deco_gauche_image.get_rect(topleft=(1083, 847))
        self.deco_droit_rect = self.deco_droit_image.get_rect(topleft=(1199, 838))
        self.deco_bonnet_rect = self.deco_bonnet_image.get_rect(topleft=(1440, 876))
        self.deco_cadeau_rect = self.deco_cadeau_image.get_rect(topleft=(1282, 886))
        self.deco_pere_noel_rect = self.deco_pere_noel_image.get_rect(
            topleft=(1646, 855)
        )

    def toggle_placement_mode(self):
        self.placement = not self.placement
        if self.placement:
            self.handle_keydown_event_placement()

    def update_cell_on_click(self, pos):
        i, j = (pos[1] - 40) // self.cell_size, (pos[0] - 40) // self.cell_size

        if (
            0 <= i < self.game.height
            and 0 <= j < self.game.width
            and not self.placement
        ):
            self.game.board[i, j] = 1 - self.game.board[i, j]
            self.draw_board()

        if self.placement_spaceship:
            self.game.place_spaceship(i, j)
            self.draw_board()
            self.placement_spaceship = False

        elif self.placement_tub:
            self.game.place_tub(i, j)
            self.draw_board()
            self.placement_tub = False

        elif self.placement_pentadecatlon:
            self.game.place_pentadecatlon(i, j)
            self.draw_board()
            self.placement_pentadecatlon = False

        elif self.placement_gun:
            self.game.place_gun(i, j)
            self.draw_board()
            self.placement_gun = False

        elif self.placement_beacon:
            self.game.place_beacon(i, j)
            self.draw_board()
            self.placement_beacon = False

    def transition_between_state(self):
        if self.update:
            start_time = time.time()
            self.game.update_board()
            end_time = time.time()
            elapsed_time = (end_time - start_time) * 1000
            self.elapsed_time.append(elapsed_time)
            alive_cells_count = np.sum(self.game.board)
            self.alive_cells.append(alive_cells_count)
            print(f"Time taken for update: {elapsed_time:.4f} milliseconds")
            self.draw_board()
            self.draw_button()
            self.draw_curve(
                data=self.elapsed_time,
                x_label="Steps",
                y_label="Execution Time (ms)",
            )
            self.draw_curve(
                self.alive_cells,
                x_label="Steps",
                y_label="Number of Living Cells",
                offset=(1080, 450),
            )
            median_time = np.median(self.elapsed_time)
            self.draw_text(f"Median Execution Time: {median_time:.2f} ms", (1080, 30))
            nb_cell = np.sum(self.game.board)
            self.draw_text(f"Total Number of Cells: {nb_cell:.2f}", (1080, 450))
            self.draw_text(f"Number of steps: {len(self.elapsed_time):} ", (10, 10))
            self.update = False


    def draw_board(self):
        self.screen.fill((135, 206, 250))

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

    def draw_curve(self, data, width=2, x_label=None, y_label=None, offset=(1080, 10)):
        fig, ax = plt.subplots(
            figsize=(8, 4), facecolor=(135 / 255, 206 / 255, 250 / 255)
        )
        ax.plot(data, linewidth=width)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        canvas = FigureCanvas(fig)
        canvas.draw()
        size = canvas.get_width_height()
        image = pygame.image.fromstring(canvas.tostring_rgb(), size, "RGB")
        self.screen.blit(image, offset)
        plt.close(fig)

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

    def draw_text(self, text, offset):
        font = pygame.font.Font(None, 36)
        rendered_text = font.render(text, True, (0, 0, 0))
        self.screen.blit(rendered_text, offset)

    def handle_quit_event(self):
        self.running = False

    def handle_mouse_click(self):
        if pygame.mouse.get_pressed()[0]:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if self.button_play_rect.collidepoint(mouse_x, mouse_y):
                self.pause = False
                print("Resuming the simulation.")
            elif self.button_pause_rect.collidepoint(mouse_x, mouse_y):
                self.pause = True
                print("Simulation paused.")
            elif self.button_save_rect.collidepoint(mouse_x, mouse_y):
                filename = "game_state.txt"
                self.game.save_to_file(filename)
                print(f"Game state saved to {filename}")
            elif self.button_load_rect.collidepoint(mouse_x, mouse_y):
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
        elif event.key == pygame.K_1:
            self.placement_gun = not self.placement_gun

        elif event.key == pygame.K_2:
            self.placement_spaceship = not self.placement_spaceship

        elif event.key == pygame.K_3:
            self.placement_beacon = not self.placement_beacon

        elif event.key == pygame.K_4:
            self.placement_pentadecatlon = not self.placement_pentadecatlon

        elif event.key == pygame.K_5:
            self.placement_tub = not self.placement_tub

    def reset_game_board(self):
        self.game.board = np.random.choice(
            [0, 1], size=(self.game.height, self.game.height), p=[1, 0]
        )

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
