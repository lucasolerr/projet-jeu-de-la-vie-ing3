import pygame
import sys

#code graph en pygame à adapter
#ajouter le compteur de cellules vivantes à chaque itération


# Listes vides x, y graph
x_data = []
y_data = []

# Initialisation graphique
def init_graph():
    global x_data, y_data
    x_data = []
    y_data = []

    pygame.init()

    # Définir la taille de la fenêtre
    largeur, hauteur = 800, 600
    fenetre = pygame.display.set_mode((largeur, hauteur))
    pygame.display.set_caption("Évolution du nombre de cellules vivantes")

    # Définir la couleur de la ligne
    couleur_ligne = (0, 0, 255)

    return fenetre, couleur_ligne

# Fonction pour mettre à jour le graphique lors de chaque itération
def update_graph(fenetre, x, y, couleur_ligne):
    global x_data, y_data
    x_data.append(x)
    y_data.append(y)

    fenetre.fill((255, 255, 255))  # Effacer l'écran

    # Dessiner la ligne
    for i in range(1, len(x_data)):
        pygame.draw.line(fenetre, couleur_ligne, (x_data[i-1], y_data[i-1]), (x_data[i], y_data[i]), 2)

    pygame.display.flip()
    pygame.time.delay(10)  # Pause courte pour actualiser le graphique

# Fonction pour afficher le graphique et le garder ouvert
def show_graph():
    pygame.quit()
    sys.exit()

# Fonction pour réinitialiser les données du graphique
def reset_graph():
    global x_data, y_data
    x_data.clear()
    y_data.clear()

# Fonction pour afficher le graphique
def Afficher_Graph(iteration, vivantes, fenetre, couleur_ligne):
    update_graph(fenetre, iteration, vivantes, couleur_ligne)
