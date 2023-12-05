import os

import matplotlib

from GrilleElement import Grille
import pygame
from affichage import GameMenu

if __name__ == "__main__":
    # créer la grille
    # blindage pour être sur que la taille est un nb entier
    ###
    #
    #     while True:
    #         # demander la taille de la grille à l'utilisateur
    #         lignes = input("saisir la taille N de la grille (NxN): ")
    #         if lignes.isnumeric() or (
    #             lignes[1:].isnumeric() and lignes[0] == "-"
    #         ):  # verifie si le nb est un entier positif
    #             # ou entier negatif : 1er terme - et 2eme terme un entier
    #             break
    #         else:
    #             print("Veuillez saisir un entier")
    #     lignes = int(lignes)  # pour caster le nb
    #     colonnes = lignes
    # grille = Grille(lignes, colonnes)
    #
    # ##

    # matplotlib.use("TkAgg")
    # Initialisation de Pygame
    pygame.init()
    # Taille de la fenêtre
    info = pygame.display.Info()
    screen = pygame.display.set_mode((info.current_w, info.current_h))
    CLOCK_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(
        CLOCK_EVENT, 300
    )  # Générer l'événement toutes les 1000 millisecondes (1 seconde)

    # Éléments du menu
    menu_items = ["Jouer", "Charger", "Quitter"]

    # Création du menu
    menu = GameMenu(screen, menu_items)

    # Exécution du menu
    menu.run()

    # Boucle_principale(grille)
