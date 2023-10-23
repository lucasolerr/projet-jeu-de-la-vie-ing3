# classe Cellule qui stocke l'état actuel de la cellule (Vivante ou Morte)
# définition des méthodes pour modifier et connaitre en temps réel l'état actuel de la cellule
class Cellule: 

    #méthode d'init d'une cellule avec uniquement son statut: Morte par defaut 
    def __init__(self):
        self.state = 'M'

    #méthode pour créer une cellule morte 
    def cell_dead(self): 
        self.state = 'M'

    #méthode pour créer une cellule vivante 
    def cell_alive(self): 
        self.state = '*'

    #méthode pour définir l'état actuel de la cellule : return True= Vivante / False= Morte
    def check_actual_state(self): 
        if self.state == '*': 
            return True 
        else: 
            return False
        

    