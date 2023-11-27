import matplotlib.pyplot as plt

# Listes vides x,y graph
x_data = []
y_data = []


# Initialisation  graphique
def init_graph():
    plt.ion()  # Activer le mode interactif (de matplotlib) pour les mises à jour à chaque itération
    plt.figure()
    plt.xlabel("Nombre d'itérations")
    plt.ylabel("Nombre de cellules vivantes")
    plt.title("Évolution du nombre de cellules vivantes")


# Fonction pour mettre à jour le graphique avec lors de chaque itération
def update_graph(x, y):
    x_data.append(x)  # actualisation valeur
    y_data.append(y)  # actualisation valeur
    plt.plot(x_data, y_data, marker="o", linestyle="-")
    plt.draw()
    plt.xlabel("Nombre d'itérations")
    plt.ylabel("Nombre de cellules vivantes")
    plt.title("Évolution du nombre de cellules vivantes")
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


'''if choix == "":
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
                graph.update_graph(iteration, vivantes)'''