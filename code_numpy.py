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
        self.clock = pygame.time.Clock()

    def update_cell_on_click(self, pos):
        # Convertir la position du clic en indices de tableau
        i, j = (pos[1] - 40) // self.cell_size, (pos[0] - 40) // self.cell_size

        # Assurez-vous que les indices sont valides
        if 0 <= i < self.game.height and 0 <= j < self.game.width:
            # Inverser l'état de la cellule
            self.game.board[i, j] = 1 - self.game.board[i, j]

            # Redessiner la planche
            self.draw_board()

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

    def draw_text(self, str, offset):
        font = pygame.font.Font(None, 36)
        text = font.render(str, True, (0, 0, 0))
        self.screen.blit(text, offset)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic gauche
                    self.update_cell_on_click(pygame.mouse.get_pos())
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r:
                    self.game.board = np.zeros((self.height, self.width), dtype=int)
                elif event.key == pygame.K_RETURN:
                    start_time = time.time()
                    self.game.update_board()
                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    elapsed_time = (end_time - start_time) * 1000
                    self.elapsed_time.append(elapsed_time)
                    alive_cells_count = np.sum(self.game.board)
                    self.alive_cells.append(alive_cells_count)
                    print(f"Time taken for update: {elapsed_time:.4f} millis seconds")
                    self.draw_board()
                    self.draw_curve(
                        data=self.elapsed_time,
                        x_label="Etapes",
                        y_label="Temps exécution (ms)",
                    )
                    self.draw_curve(
                        data=self.alive_cells,
                        x_label="Etapes",
                        y_label="Nb cellules Vivantes",
                        offset=(1080, 500),
                    )
                    median_time = np.median(self.elapsed_time)
                    self.draw_text(
                        f"Temps médian d'exécution : {median_time:.2f} ms", (1080, 30)
                    )
                    nb_cell = np.sum(self.game.board)
                    self.draw_text(f"Nb total de celulles : {nb_cell:.2f}", (1080, 500))
                    pygame.display.flip()
                elif event.key == pygame.K_s:
                    filename = "game_state.txt"
                    self.game.save_to_file(filename)
                    print(f"Game state saved to {filename}")
                elif event.key == pygame.K_l:
                    # Press 'l' to load the state from a file
                    filename = "game_state.txt"
                    self.game.load_from_file(filename)
                    print(f"Game state loaded from {filename}")
                    self.draw_board()

    def run(self):
        while self.running:
            self.handle_events()
            self.clock.tick(10)  # Adjust the speed as needed
            pygame.display.flip()


def jeu_principal(taille):
    game = GameOfLife(width=taille, height=taille)
    gui = GameOfLifeGUI(game)

    gui.run()


if __name__ == "__main__":
    pygame.init()

    game = GameOfLife(width=50, height=50)
    gui = GameOfLifeGUI(game)

    gui.run()

    pygame.quit()
