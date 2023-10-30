from CelluleElement import Cellule
import random as rand
from random import randint


# classe grille possédant la taille de la grille & la grille
# prend en param les lignes et les colonnes entrées par l'utilisateur
class Grille:
    # méthode d'init de la classe Grille()
    def __init__(self, lignes, colonnes):
        self.lignes = lignes
        self.colonnes = colonnes
        self.grille2D = [
            [Cellule() for _ in range(self.colonnes)] for _ in range(self.lignes)
        ]

        self.build_grille()

    # #méthode pour initialiser la grille aléatoirement avec des 0=mort et 1=vivant
    # plus utilisé car grille définit autrement
    # def init_grille(self):
    #     for i in range(self.lignes):
    #         for j in range(self.lignes):
    #             self.grille2D[i][j] = rand.randint(0,1)
    #     print (self.grille2D)

    # méthode pour générer une nouvelle grille avec des cellules aléatoirement mortes ou vivantes
    def build_grille(self):
        for lignes in self.grille2D:
            for colonnes in lignes:
                cell = randint(0, 2)
                if cell == 1:
                    colonnes.cell_alive()

    # méthode d'affichage de la grille sous forme de lettre pour meilleure visibilité
    def afficher_grille(self):
        for lignes in self.grille2D:
            for colonnes in lignes:
                if colonnes.check_actual_state():
                    print("*", end="")
                else:
                    print("M", end="")
            print()

    # méthode pour définir les voisins de chaque cellule
    # return une liste des voisins de la cell
    def find_voisin(self, cell_ligne, cell_colonne):
        # créer une liste vide pour stocker les cellules voisines
        list_voisins = []
        # on parcour les cell en partant de la cellule a checker
        # on parcourt entre:  -1 = cell précedante / 0 = même ligne ou colonne que la cell / 1 = cellule suivante
        for lignes in range(-1, 2):
            for colonnes in range(-1, 2):
                voisin_ligne = cell_ligne + lignes
                voisin_colonne = cell_colonne + colonnes

                # on vérifie que la cellule trouvé ne soit pas hors cadre ou que ça soit la même cellule
                voisin_OK = True
                if (voisin_ligne) == cell_ligne and (voisin_colonne) == cell_colonne:
                    voisin_OK = False
                if (voisin_ligne) < 0 or (voisin_colonne) >= self.colonnes:
                    voisin_OK = False
                if (voisin_colonne) < 0 or (voisin_ligne) >= self.lignes:
                    voisin_OK = False

                if voisin_OK:
                    list_voisins.append(self.grille2D[voisin_ligne][voisin_colonne])
        return list_voisins

    # méthode pour mettre à jour la grille
    # création de 2 listes pour cell vivantes et mortes
    # on parcours la grille en comptant les cell selon leur état actuel
    def etat_suivant(self):
        list_vivantes = []
        list_mortes = []

        for lignes in range(len(self.grille2D)):
            for colonnes in range(len(self.grille2D[lignes])):
                find_voisin = self.find_voisin(lignes, colonnes)
                # création d'une liste pour stocker le nb et les cell voisines vivantes
                nb_voisin_alive = []

                for cell_voisine in find_voisin:
                    if cell_voisine.check_actual_state():
                        # on rempli la liste au fur et à mesure
                        nb_voisin_alive.append(cell_voisine)

                cell = self.grille2D[lignes][colonnes]
                etat_cell = cell.check_actual_state()

                # on test les règles du jeu sur la cellule actuelle
                # on remplit à chaque fois la liste de cell morte ou vivante en fonction
                # si cell vivante alors :
                if etat_cell == True:
                    # reste vivante si elle a 2 ou 3 cell voisine vivantes
                    if len(nb_voisin_alive) == 2 or len(nb_voisin_alive) == 3:
                        list_vivantes.append(cell)
                    # meurt de sous ou de surpopulation
                    if len(nb_voisin_alive) < 2 or len(nb_voisin_alive) > 3:
                        list_mortes.append(cell)
                # si cell morte alors :
                else:
                    # vit si exactement 3 cell voisines vivantes
                    if len(nb_voisin_alive) == 3:
                        list_vivantes.append(cell)
        # Enfin, on modifie l'état actuel de chaque cell analysée en parcourant les 2 listes créées
        for cellule in list_vivantes:
            cellule.cell_alive()
        for cellule in list_mortes:
            cellule.cell_dead()


"""
# Proposition de code de calcul optimisé
def precalculate_neighbors(self):
    self.neighbors = {}
    for ligne in range(self.lignes):
        for colonne in range(self.colonnes):
            neighbors = []
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == 0 and j == 0:
                        continue  # On ignore elle-même
                    voisin_ligne = ligne + i
                    voisin_colonne = colonne + j
                    if 0 <= voisin_ligne < self.lignes and 0 <= voisin_colonne < self.colonnes:
                        neighbors.append(self.grille2D[voisin_ligne][voisin_colonne])
            self.neighbors[(ligne, colonne)] = neighbors

def etat_suivant(self):
    new_live_cells = set()
    new_dead_cells = set()

    for ligne in range(self.lignes):
        for colonne in range(self.colonnes):
            cell = self.grille2D[ligne][colonne]
            neighbors = self.neighbors[(ligne, colonne)]
            nb_voisin_alive = sum(1 for neighbor in neighbors if neighbor.check_actual_state())

            if cell.check_actual_state():
                if nb_voisin_alive == 2 or nb_voisin_alive == 3:
                    new_live_cells.add(cell)
                else:
                    new_dead_cells.add(cell)
            else:
                if nb_voisin_alive == 3:
                    new_live_cells.add(cell)

    for cellule in new_live_cells:
        cellule.cell_alive()
    for cellule in new_dead_cells:
        cellule.cell_dead()

"""