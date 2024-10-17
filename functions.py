from pygame import *
from pygame.locals import *
from variables import *
from random import randint as ri

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

#Fonctions ou on cherche de potentielles collisions
def check_down_collision(moving_bloc, moving_bloc_position, moving_bloc_color, grille, last_moving_bloc, last_moving_bloc_position, last_moving_bloc_color):
    moving_bloc_position[0] += 1
    if moving_bloc_position[0] + len(moving_bloc) <= len(grille) and moving_bloc_position[1] + len(moving_bloc[0]) <= len(grille[0]):
        for i in range(len(moving_bloc)):
            for u in range(len(moving_bloc[i])):
                if moving_bloc[i][u] != 0:
                    if grille[moving_bloc_position[0]+i][moving_bloc_position[1]+u] != 0:
                        last_moving_bloc, last_moving_bloc_position, last_moving_bloc_color = moving_bloc, moving_bloc_position, moving_bloc_color
                        moving_bloc_position[0] -= 1
                        moving_bloc_color = color[ri(2,4)]
                        moving_bloc = blocs[ri(0,6)]
                        moving_bloc_position = [0, 3]
                        if moving_bloc == blocs[1]:
                            moving_bloc_position = [0, 4]
                        return moving_bloc, moving_bloc_position, moving_bloc_color, last_moving_bloc, last_moving_bloc_position, last_moving_bloc_color
        return moving_bloc, moving_bloc_position, moving_bloc_color, last_moving_bloc, last_moving_bloc_position, last_moving_bloc_color
    else:
        last_moving_bloc, last_moving_bloc_position, last_moving_bloc_color = moving_bloc, moving_bloc_position, moving_bloc_color
        moving_bloc_position[0] -= 1
        moving_bloc_color = color[ri(2,4)]
        moving_bloc = blocs[ri(0,6)]
        moving_bloc_position = [0, 3]
        if moving_bloc == blocs[1]:
            moving_bloc_position = [0, 4]
        return moving_bloc, moving_bloc_position, moving_bloc_color, last_moving_bloc, last_moving_bloc_position, last_moving_bloc_color

def check_up_collision():
    return True

def check_collision(moving_bloc, moving_bloc_position, grille, direction):
    if direction == "right":
        return True
    elif direction == "left":
        return True

#Fonction de rotation. Ne s'executera que si check_collision est True
def rotate(moving_bloc):
    moving_bloc_rotated = [0]*len(moving_bloc[0])
    for i in range(len(moving_bloc_rotated)):
        moving_bloc_rotated[i] = [0]*len(moving_bloc)
    for i in range(len(moving_bloc)):
        for u in range(len(moving_bloc[i])):
            moving_bloc_rotated[u][len(moving_bloc)-1-i] = moving_bloc[i][u]
    return moving_bloc_rotated