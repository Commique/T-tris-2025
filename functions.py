from pygame import *
from pygame.locals import *
from variables import *

#Toutes nos fonctions

#Ajuster la taille des composants
def update_window(width, height):
    if height <= 2.2*width:
        pixel = height//22
    elif height > 2.2*width:
        pixel = width//10
    return pixel


#Debug. Print la grille pour afficher ses valeurs
def debug(grille):
    print("____________________________________________________")
    for i in grille:
        print(i)
    print("____________________________________________________")


#Fonction ou on cherche de potentielles collisions. Renvoie True si pas de collision
def check_collision(moving_bloc, moving_bloc_position, grille, direction):
    return True

#Fonction de rotation. Ne s'executera que si check_collision est True
def rotate(moving_bloc):
    nb_lines = len(moving_bloc)
    nb_columns = len(moving_bloc[0])
    moving_bloc_rotated = [[[]*nb_lines]*nb_columns]
    for i in range(nb_lines):
        pass
    return moving_bloc_rotated
