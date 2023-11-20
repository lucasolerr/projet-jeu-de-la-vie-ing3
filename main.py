from Jeu import Jouer
from GrilleElement import Grille

if __name__ == "__main__":
    print("Bonjour Monde!!")

    # créer la grille
    # blindage pour être sur que la taille est un nb entier
    while True:
        # demander la taille de la grille à l'utilisateur
        lignes = input("saisir la taille N de la grille (NxN): ")
        if lignes.isnumeric() or (
            lignes[1:].isnumeric() and lignes[0] == "-"
        ):  # verifie si le nb est un entier positif
            # ou entier negatif : 1er terme - et 2eme terme un entier
            break
        else:
            print("Veuillez saisir un entier")
    lignes = int(lignes)  # pour caster le nb
    colonnes = lignes
grille = Grille(lignes, colonnes)
Jouer(grille)
