import pygame
import time


def afficher_grille(
    grille,
    carres,
    fenetre,
    image_carre_mort,
    image_carre_vivant,
):
    # Dessiner les carrés en fonction de leurs états
    for i, rect in enumerate(carres):
        ligne, colonne = i // grille.colonnes, i % grille.colonnes
        cellule = grille.grille2D[ligne][colonne]
        if cellule.check_actual_state():
            fenetre.blit(image_carre_vivant, rect.topleft)
        else:
            fenetre.blit(image_carre_mort, rect.topleft)


def afficher_grille_survol(
    grille,
    carres,
    survole,
    fenetre,
    image_carre_survol,
    image_carre_mort,
    image_carre_vivant,
):
    for i, rect in enumerate(carres):
        ligne, colonne = i // grille.colonnes, i % grille.colonnes
        cellule = grille.grille2D[ligne][colonne]

        if survole[i]:
            fenetre.blit(image_carre_survol, rect.topleft)
        elif cellule.check_actual_state():
            fenetre.blit(image_carre_vivant, rect.topleft)
        else:
            fenetre.blit(image_carre_mort, rect.topleft)


def affichage_general(grille):

    # initialisation nombre iteration
    iteration = 0

    # Initialisation de Pygame
    pygame.init()

    # Définir la taille de la grille

    taille_case = 12
    nbr_case = grille.lignes

    fenetre = pygame.display.set_mode((0, 0), pygame.WINDOWMAXIMIZED)
    pygame.display.set_caption("Le jeu de la vie")

    # image :
    image_carre_mort = pygame.image.load("image/carre_mort.png")
    image_carre_mort = pygame.transform.scale(
        image_carre_mort, (taille_case, taille_case)
    )

    image_carre_vivant = pygame.image.load("image/carre_vivant.png")
    image_carre_vivant = pygame.transform.scale(
        image_carre_vivant, (taille_case, taille_case)
    )

    # liste de rectangles pour chaque carré
    carres = [
        pygame.Rect(
            50 + x * taille_case, 20 + y * taille_case, taille_case, taille_case
        )
        for x in range(grille.colonnes)
        for y in range(grille.lignes)
    ]

    #  liste pour suivre l'état survolé / cliqué de chaque carré
    survole = [False] * (nbr_case * nbr_case)
    etats_carres = [False] * (nbr_case * nbr_case)

    # Boucle principale
    en_cours = True
    while en_cours:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                en_cours = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Vérifiez si le clic bouton gauche
                    pos_souris = pygame.mouse.get_pos()
                    for i, rect in enumerate(carres):
                        if rect.collidepoint(pos_souris):
                            etats_carres[i] = not etats_carres[i]  # Mort / Vivant
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    en_cours = False  # Quitter la fenêtre si Échap est pressé
                if event.key == pygame.K_RETURN:
                    debut = time.time()
                    grille.etat_suivant()
                    fin = time.time()
                    temps_execution = fin - debut
                    print(f"Temps d'exécution : {temps_execution:.6f} secondes")
                    """
                    # Nombre d'itération
                    iteration += 1

                    # Calculer le nombre de cellules vivantes
                    vivantes = grille.update_and_count_vivantes()

                    # affichage du graphique
                    if iteration >= 1:  # verification que le nombre d'iteration n'est pas nul
                        graph.Afficher_Graph(iteration, vivantes)
                        # Mise à jour du graphique
                        graph.update_graph(iteration, vivantes)
                    """

        # Position de la souris
        pos_souris = pygame.mouse.get_pos()

        # Survole l'un des carrés
        for i, rect in enumerate(carres):
            if rect.collidepoint(pos_souris):
                survole[i] = True
            else:
                survole[i] = False

        fenetre.fill((255, 255, 255))

        afficher_grille(
            grille,
            carres,
            fenetre,
            image_carre_mort,
            image_carre_vivant,
        )
        pygame.display.flip()

    pygame.quit()


def affichage_choix_grille():
    return

# Initialisation de Pygame
pygame.init()

class GameMenu:
    def __init__(
        self, screen, items,
        bg_color=(0, 0, 0), font=None,
        font_size=100, font_color=(255, 255, 255)
    ):
        self.screen = screen
        self.scr_width = self.screen.get_rect().width
        self.scr_height = self.screen.get_rect().height

        # Background Main Menu
        self.bg_color = bg_color

        # Gère l'écart entre le cadre de sélection et le texte de l'élément
        self.paddingx = 8
        self.paddingy = 20

        # Informe de l'écran actuel affiché
        self.start_selected = False
        self.settings_selected = False
        self.quit_select = False

        # Le premier élement sera sélectionné par défaut avec l'index 0.
        # Si le second élément est sélectionné l'index passera à 1, etc.
        self.index_selected = 0

        # init font
        self.font = pygame.font.Font(font, font_size)

        # Element courant sélectionné
        self.current_item = ()

        # Positionnement des éléments visuels
        self.menu_items = []

        for index, item in enumerate(items):
            label = self.font.render(item, 1, font_color)
            width = label.get_rect().width
            height = label.get_rect().height + 20

            posx = (self.scr_width / 2) - (width / 2)
            t_h = len(items) * height
            posy = (self.scr_height / 2) - (t_h / 2) + (index * height)

            self.menu_items.append([item, label, (width, height), (posx, posy)])

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
                            if self.current_item[0] == "Jouer":
                                self.start_selected = True
                            elif self.current_item[0] == "Charger":
                                self.settings_selected = True
                            elif self.current_item[0] == "Quitter":
                                self.quit_select = True
                                mainloop = False

            self.current_item = self.menu_items[self.index_selected]
            self.screen.fill(self.bg_color)

            if not self.start_selected or not self.settings_selected:

                for name, label, (width, height), (posx, posy) in self.menu_items:
                    self.screen.blit(label, (posx, posy))
                    name, label, (width, height), (posx, posy) = self.current_item
                    pygame.draw.rect(
                        self.screen, (255, 255, 255),
                        [
                            posx - self.paddingx, posy - self.paddingy,
                            width + self.paddingx + self.paddingx, height + self.paddingy
                        ], 2)

            if self.start_selected:
                affichage_choix_grille()
                self.start_selected = False

                pygame.display.flip()

if __name__ == "__main__":
    # Taille de la fenêtre
    screen = pygame.display.set_mode((0, 0), pygame.WINDOWMAXIMIZED)

    # Éléments du menu
    menu_items = ["Jouer","Charger","Quitter"]

    # Création du menu
    menu = GameMenu(screen, menu_items)

    # Exécution du menu
    menu.run()

