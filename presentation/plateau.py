
# classe plateau permettant de bouger dans la grille
# cette classe correspond globalement à une grille mais on va pouvoir se mouvoir à l'intérieur 
# chaque lignes de la grille est définit comme une liste : self.grille[X][Y] 
# X : num de lignes & Y : num de la colonne
# grace à cette classe on pourra plus facilement connaitre les cellules voisines de chaque cellule de la grille
class Plateau: 

    #création d'une grille sous forme de 4 listes (1 liste = 1 ligne)
    # expl : A est dans la case self.grid[0][0] 
    # H est dans la case self.grid[2][1]
    def __init__(self):
        self.plateau = [['A','B','C'], 
                       ['D','E','F'],
                       ['G','H','I'], 
                       ['J','K','L']]
        
    def afficher_plateau(self): 
        for lignes in self.plateau: 
            print(lignes)
        



