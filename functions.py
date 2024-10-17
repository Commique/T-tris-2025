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
def check_down_collision(moving_bloc, moving_bloc_position, grille, last_moving_bloc, last_moving_bloc_position):
    running = True
    moving_bloc_position[0] += 1
    #Bloc ne doit pas exéder la taille de la grille
    if moving_bloc_position[0] + len(moving_bloc) <= len(grille):
        #Check for collisions
        for i in range(len(moving_bloc)):
            for u in range(len(moving_bloc[i])):
                if moving_bloc[i][u] != 0:
                    if grille[moving_bloc_position[0]+i][moving_bloc_position[1]+u] != 0:
                        #Check for a potential collision at spawn
                        future_bloc = blocs[ri(0,6)]
                        future_bloc_position = [0, 3]
                        if future_bloc == blocs[1]:
                            future_bloc_position = [0, 4]
                        for i in range(len(future_bloc)):
                            for u in range(len(future_bloc[i])):
                                if future_bloc[i][u] != 0:
                                    if grille[future_bloc_position[0]+i][future_bloc_position[1]+u] != 0:
                                        running = False
                        last_moving_bloc, last_moving_bloc_position = moving_bloc, moving_bloc_position
                        moving_bloc_position[0] -= 1
                        moving_bloc = future_bloc
                        moving_bloc_position = future_bloc_position
                        return moving_bloc, moving_bloc_position, last_moving_bloc, last_moving_bloc_position, running
        #Si pas de collision
        return moving_bloc, moving_bloc_position, last_moving_bloc, last_moving_bloc_position, running
    #La pièce touche le bas de la grille
    else:
        last_moving_bloc, last_moving_bloc_position = moving_bloc, moving_bloc_position
        moving_bloc_position[0] -= 1
        moving_bloc = blocs[ri(0,6)]
        moving_bloc_position = [0, 3]
        if moving_bloc == blocs[1]:
            moving_bloc_position = [0, 4]
        return moving_bloc, moving_bloc_position, last_moving_bloc, last_moving_bloc_position, running

#Collisions par rotation
def check_up_collision(moving_bloc, moving_bloc_position, grille):
    rotated = rotate(moving_bloc)
    #Bloc ne doit pas exéder la taille de la grille
    if moving_bloc_position[1] + len(rotated[0]) <= len(grille[0]):
        #Check for collisions
        for i in range(len(rotated)):
            for u in range(len(rotated[i])):
                if rotated[i][u] != 0:
                    if grille[moving_bloc_position[0]+i][moving_bloc_position[1]+u] != 0:
                        return moving_bloc
        return rotated
    else:
        return moving_bloc

#Collisions latérales
def check_collision(moving_bloc, moving_bloc_position, grille, direction):
    if direction == "right":
        moving_bloc_position[1] += 1
        #Bloc ne doit pas exéder la taille de la grille
        if moving_bloc_position[1] + len(moving_bloc[0]) <= len(grille[0]):
            #Check for collisions
            for i in range(len(moving_bloc)):
                for u in range(len(moving_bloc[i])):
                    if moving_bloc[i][u] != 0:
                        if grille[moving_bloc_position[0]+i][moving_bloc_position[1]+u] != 0:
                            moving_bloc_position[1] -= 1
                            return moving_bloc_position
            return moving_bloc_position
        else:
            moving_bloc_position[1] -= 1
            return moving_bloc_position
    elif direction == "left":
        moving_bloc_position[1] -= 1
        #Bloc ne doit pas exéder la taille de la grille
        if moving_bloc_position[1] >= 0:
            #Check for collisions
            for i in range(len(moving_bloc)):
                for u in range(len(moving_bloc[i])):
                    if moving_bloc[i][u] != 0:
                        if grille[moving_bloc_position[0]+i][moving_bloc_position[1]+u] != 0:
                            moving_bloc_position[1] += 1
                            return moving_bloc_position
            return moving_bloc_position
        else:
            moving_bloc_position[1] += 1
            return moving_bloc_position

#Fonction de rotation. Ne s'executera que si check_collision est True
def rotate(moving_bloc):
    moving_bloc_rotated = [0]*len(moving_bloc[0])
    for i in range(len(moving_bloc_rotated)):
        moving_bloc_rotated[i] = [0]*len(moving_bloc)
    for i in range(len(moving_bloc)):
        for u in range(len(moving_bloc[i])):
            moving_bloc_rotated[u][len(moving_bloc)-1-i] = moving_bloc[i][u]
    return moving_bloc_rotated

#Fonction de nettoyage des lignes
def is_in_a_line(grille):
    for i in range(len(grille)):
        if grille[i][0]*grille[i][1]*grille[i][2]*grille[i][3]*grille[i][4]*grille[i][5]*grille[i][6]*grille[i][7]*grille[i][8]*grille[i][9] != 0:
            grille.pop(i)
            grille = grille[::-1]
            grille.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            grille = grille[::-1]
    return grille