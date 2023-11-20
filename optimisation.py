import numpy as np
import time

def afficher_grille(grille):
    for ligne in grille:
        print(" ".join(["■" if cellule else "□" for cellule in ligne]))
    print()

def etat_suivant(grille):
    lignes, colonnes = len(grille), len(grille[0])
    nouvelle_grille = np.zeros((lignes, colonnes), dtype=int)

    for i in range(lignes):
        for j in range(colonnes):
            voisins = (
                grille[i - 1:i + 2, j - 1:j + 2].sum() - grille[i, j]
            )
            if grille[i, j] == 1 and 2 <= voisins <= 3:
                nouvelle_grille[i, j] = 1
            elif grille[i, j] == 0 and voisins == 3:
                nouvelle_grille[i, j] = 1

    return nouvelle_grille

def jeu_de_la_vie(taille, iterations):
    grille = np.random.choice([0, 1], size=(taille, taille), p=[0.7, 0.3])

    for iteration in range(iterations):
        debut = time.time()
        grille = etat_suivant(grille)
        fin = time.time()
        temps_calcul = fin - debut

        print(f"Iteration {iteration + 1}/{iterations} - Temps de calcul: {temps_calcul:.6f} secondes")
        afficher_grille(grille)

# Paramètres du jeu
taille_grille = 50
nombre_iterations = 5

# Exécuter le jeu de la vie
jeu_de_la_vie(taille_grille, nombre_iterations)
