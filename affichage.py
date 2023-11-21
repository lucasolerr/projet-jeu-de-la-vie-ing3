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
    image_carre_survol = pygame.image.load("image/carre_survol.png")
    image_carre_survol = pygame.transform.scale(
        image_carre_survol, (taille_case, taille_case)
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




def afficher_menu(grille):
    # Initialisation de Pygame
    pygame.init()

    # Définir la taille de la fenêtre et la taille de la grille
    fenetre_largeur, fenetre_hauteur = 1200, 650
    taille_case = 12
    nbr_case = 50

    # Fenêtre

    # fenetre = pygame.display.set_mode((fenetre_largeur, fenetre_hauteur))
    fenetre = pygame.display.set_mode((0, 0), pygame.WINDOWMAXIMIZED)
    pygame.display.set_caption("Le jeu de la vie")

    # image :
    image_carre_mort = pygame.image.load("image/carre_mort.png")
    image_carre_mort = pygame.transform.scale(
        image_carre_mort, (taille_case, taille_case)
    )

    # Boucle principale
    en_cours = True
    while en_cours:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                en_cours = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Vérifiez si le clic bouton gauche
                    pos_souris = pygame.mouse.get_pos()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    en_cours = False  # Quitter la fenêtre si Échap est pressé
        # Position de la souris
        pos_souris = pygame.mouse.get_pos()


        fenetre.fill((255, 255, 255))

        pygame.display.flip()

    pygame.quit()


