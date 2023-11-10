import matplotlib.pyplot as plt 
from GrilleElement import Grille

# Listes vides x,y graph
x_data = []
y_data = []

# Initialisation  graphique
def init_graph():
    plt.ion()  # Activer le mode interactif (de matplotlib) pour les mises à jour à chaque itération 
    plt.figure()
    plt.xlabel('Nombre d\'itérations')
    plt.ylabel('Nombre de cellules vivantes')
    plt.title('Évolution du nombre de cellules vivantes')

# Fonction pour mettre à jour le graphique avec lors de chaque itération
def update_graph(x, y):
    x_data.append(x)  # actualisation valeur
    y_data.append(y)  #actualisation valeur 
    plt.plot(x_data, y_data, marker='o', linestyle='-')
    plt.draw()
    plt.pause(0.001)  # Pause courte pour actualiser le graphique

# Fonction pour afficher le graphique et le garder ouvert
def show_graph():
    plt.ioff()  # Désactiver le mode interactif
    plt.show()

# Réinitialiser les données du graphique
def reset_graph():
    x_data.clear()
    y_data.clear()
    plt.clf()

# Fonction pour afficher le graphique
def Afficher_Graph(iteration, vivantes):
    update_graph(iteration, vivantes)
   