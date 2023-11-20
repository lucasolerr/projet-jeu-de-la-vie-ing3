from GrilleElement import Grille
import graph
import pygame
from affichage import affichage_general
import time


def Jouer(grille):
    # initialisation nombre iteration
    iteration = 0
    # afficher la grille une première fois
    #grille.afficher_grille()
    affichage_general(grille)

    # choix de l'utilisateur
    choix = " "
    while choix != "q":
        choix = input(
            "Cliquer sur q pour quitter ou presser entrer pour update la grille: "
        )
        # on update la grille en cliquant sur entrée avec mise à jour des cellules en fonction de leur état
        if choix == "":
            debut = time.time()
            affichage_general(grille)
            grille.etat_suivant()
            fin = time.time()
            temps_execution = fin - debut
            grille.afficher_grille()
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
