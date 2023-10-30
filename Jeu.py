from GrilleElement import Grille


def Jouer():
    # blindage pour être sur que la taille est un nb entier 
    while True: 
        # demander la taille de la grille à l'utilisateur
        lignes = input("saisir la taille N de la grille (NxN): ")
        if lignes.isnumeric() or (lignes[1:].isnumeric() and lignes[0]=="-"): #verifie si le nb est un entier positif
                                                                    # ou entier negatif : 1er terme - et 2eme terme un entier 
            break
        else : 
            print("Veuillez saisir un entier")
    lignes = int(lignes) #pour caster le nb
    colonnes = lignes
    # créer la grille
    grille = Grille(lignes, colonnes)

    # afficher la grille une première fois
    grille.afficher_grille()

    # choix de l'utilisateur
    choix = " "
    while choix != "q":
        choix = input("Cliquer sur q pour quitter ou presser entrer pour update la grille: ")
        # on update la grille en cliquant sur entrée avec mise à jour des cellules en fonction de leur état
        if (choix == ''): 
            grille.etat_suivant()
            grille.afficher_grille()

