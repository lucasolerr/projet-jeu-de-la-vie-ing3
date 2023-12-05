import pygame

class GridSizeMenu:
    def __init__(
        self,
        screen,
        game_menu,
        font=None,
        font_size=50,
        background_image_path="image/fond_noel.jpg",
    ):
        self.screen = screen
        self.scr_width = self.screen.get_rect().width
        self.scr_height = self.screen.get_rect().height

        self.bg_color = (0, 0, 0)
        self.paddingx = 8
        self.paddingy = 20

        self.index_selected = 0
        self.font = pygame.font.Font(font, font_size)
        self.current_item = ""
        self.game_menu = game_menu

        # self.user_input = ""
        self.background_image = pygame.image.load(background_image_path)

    def run(self):
        choix_loop = True
        while choix_loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    choix_loop = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game_menu.selected_action = None
                        self.game_menu.start_selected = False
                        choix_loop = False

                    if event.key == pygame.K_RETURN:
                        try:
                            selected_size = int(self.game_menu.user_input)
                            print(
                                f"Taille de la grille sélectionnée : {selected_size}x{selected_size}"
                            )
                            if selected_size >= 50:
                                # FAIRE LA CREATION DE GRILLE ICI
                                self.game_menu.selected_action = None
                                self.game_menu.start_selected = False
                                self.game_menu.playing = True
                                choix_loop = False

                        except ValueError:
                            print("Veuillez entrer un nombre valide.")

                    if event.key == pygame.K_BACKSPACE:
                        self.game_menu.user_input = self.game_menu.user_input[:-1]

                    if event.key in (
                        pygame.K_0,
                        pygame.K_1,
                        pygame.K_2,
                        pygame.K_3,
                        pygame.K_4,
                        pygame.K_5,
                        pygame.K_6,
                        pygame.K_7,
                        pygame.K_8,
                        pygame.K_9,
                    ):
                        self.game_menu.user_input += event.unicode

            scaled_background = pygame.transform.scale(
                self.background_image, (self.scr_width, self.scr_height)
            )
            self.screen.blit(scaled_background, (0, 0))

            pygame.draw.rect(
                self.screen,
                (255, 255, 255),
                (self.scr_width / 2 - 100, self.scr_height / 2 - 10, 200, 40),
                2,
            )

            label1 = self.font.render(f"Taille de la grille > 50 :", 1, (255, 255, 255))
            width = label1.get_rect().width
            height = label1.get_rect().height + 20
            posx = (self.scr_width / 2) - (width / 2)
            posy = (self.scr_height / 2) - height
            self.screen.blit(label1, (posx, posy))

            label = self.font.render(f"{self.game_menu.user_input} ", 1, (16, 25, 80))
            posx = self.scr_width / 2 - 10
            posy = self.scr_height / 2 - 1
            self.screen.blit(label, (posx, posy))

            pygame.display.flip()