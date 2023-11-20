from GrilleElement import Grille
import graph


def Jouer(grille):
    # initialisation nombre iteration
    iteration = 0
    # afficher la grille une première fois
    grille.afficher_grille()

    # choix de l'utilisateur
    choix = " "
    while choix != "q":
        choix = input(
            "Cliquer sur q pour quitter ou presser entrer pour update la grille: "
        )
        # on update la grille en cliquant sur entrée avec mise à jour des cellules en fonction de leur état
        if choix == "":
            grille.etat_suivant()
            grille.afficher_grille()
            # Nombre d'itération
            iteration += 1

            # Calculer le nombre de cellules vivantes
            vivantes = grille.update_and_count_vivantes()

            # affichage du graphique
            if iteration >= 1:  # verification que le nombre d'iteration n'est pas nul
                graph.Afficher_Graph(iteration, vivantes)
                # Mise à jour du graphique
                graph.update_graph(iteration, vivantes)
