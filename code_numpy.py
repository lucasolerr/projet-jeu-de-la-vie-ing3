import numpy as np
import pygame
import time


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
        neighbors_count = np.zeros_like(self.board, dtype=int)

        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i != 0 or j != 0:
                    neighbors_count += np.roll(
                        np.roll(self.board, i, axis=0), j, axis=1
                    )

        live_neighbors = neighbors_count
        self.board = np.where(
            (self.board == 1) & ((live_neighbors < 2) | (live_neighbors > 3)),
            0,
            np.where(
                (self.board == 1) & ((live_neighbors == 2) | (live_neighbors == 3)),
                1,
                np.where((self.board == 0) & (live_neighbors == 3), 1, self.board),
            ),
        )


class GameOfLifeGUI:
    def __init__(self, game):
        self.game = game
        self.cell_size = 5  # Adjust the cell size as needed
        self.width = self.game.width * self.cell_size
        self.height = self.game.height * self.cell_size
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Game of Life")

        self.running = True
        self.clock = pygame.time.Clock()

    def draw_board(self):
        self.screen.fill((255, 255, 255))  # White background
        for i in range(self.game.height):
            for j in range(self.game.width):
                if self.game.board[i, j] == 1:
                    pygame.draw.rect(
                        self.screen,
                        (0, 0, 0),
                        (
                            j * self.cell_size,
                            i * self.cell_size,
                            self.cell_size,
                            self.cell_size,
                        ),
                    )

        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    start_time = time.time()
                    self.game.update_board()
                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    print(f"Time taken for update: {elapsed_time:.4f} seconds")
                    self.draw_board()
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


if __name__ == "__main__":
    pygame.init()

    game = GameOfLife(width=50, height=50)
    gui = GameOfLifeGUI(game)

    gui.run()

    pygame.quit()
