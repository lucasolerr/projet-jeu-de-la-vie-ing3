from GrilleElement import Grille

def Jouer(): 
    # demander la taille de la grille à l'utilisateur
    lignes = int (input("saisir la taille N de la grille (NxN): "))
    colonnes = lignes
    # créer la grille 
    grille = Grille(lignes, colonnes)

    #afficher la grille une première fois 
    grille.afficher_grille()

    # choix de l'utilisateur
    choix = '' 
    while choix != 'q' : 
        choix = input("Cliquer sur q pour quitter ou presser entrer pour update la grille: ") 
        # on update la grille en cliquant sur enrtrée avec mise à jour des cellules en fonction de leur état 
        grille.etat_suivant()
        grille.afficher_grille()
