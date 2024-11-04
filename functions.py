from pygame import *
from pygame.locals import *
from variables import blocs 
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
    #On essaie de faire descendre la pièce
    moving_bloc_position[0] += 1
    #Bloc ne doit pas exéder la taille de la grille
    if moving_bloc_position[0] + len(moving_bloc) <= len(grille):
        #Check for collisions
        for i in range(len(moving_bloc)):
            for u in range(len(moving_bloc[i])):
                if moving_bloc[i][u] != 0:
                    if grille[moving_bloc_position[0]+i][moving_bloc_position[1]+u] != 0:
                        moving_bloc, moving_bloc_position, last_moving_bloc, last_moving_bloc_position, grille, running = new_piece(grille, moving_bloc, moving_bloc_position)
                        if not running:
                            return moving_bloc, moving_bloc_position, last_moving_bloc, last_moving_bloc_position, grille, running
                        grille = is_in_a_line(grille)
                        return moving_bloc, moving_bloc_position, last_moving_bloc, last_moving_bloc_position, grille, running #On retourne running pour arrêter la partie
        #Si pas de collision
        return moving_bloc, moving_bloc_position, last_moving_bloc, last_moving_bloc_position, grille, running
    #La pièce touche le bas de la grille
    else:
        #Nouvelle pièce 
        last_moving_bloc, last_moving_bloc_position = moving_bloc, moving_bloc_position
        moving_bloc_position[0] -= 1
        moving_bloc = blocs[ri(0,6)]
        moving_bloc_position = [0, 3]
        #Cas du carré
        if moving_bloc == blocs[1]:
            moving_bloc_position = [0, 4]
        #On ajoute la pièce
        grille = add_piece(moving_bloc, moving_bloc_position, grille)
        grille = add_piece(last_moving_bloc, last_moving_bloc_position, grille)
        #Check remplissage de la grille
        grille = is_in_a_line(grille)
        return moving_bloc, moving_bloc_position, last_moving_bloc, last_moving_bloc_position, grille, running

#Ajouter une nouvelle pièce
def new_piece(grille, moving_bloc, moving_bloc_position):
    running = True
    #Ici, la pièce a rencontré un obstacle, on en créé une autre et on nettoie la grille
    #Check for a potential collision at spawn
    #Création d'un potentiel bloc qui doit vérifier des conditions pour venir dans le jeu, sinon Game Over
    future_bloc = blocs[ri(0,6)]
    future_bloc_position = [0, 3]
    #Ajustement de la position pour le carré
    if future_bloc == blocs[1]:
        future_bloc_position = [0, 4]
    #On vérifie qu'aucun bloc n'est déjà présent
    for i in range(len(future_bloc)):
        for u in range(len(future_bloc[i])):
            if future_bloc[i][u] != 0:
                #Check for Game Over 
                if grille[future_bloc_position[0]+i][future_bloc_position[1]+u] != 0:
                    running = False
    #On inverse les variables avant de remettre à 0 celles du bloc qui bouge 
    last_moving_bloc, last_moving_bloc_position = moving_bloc, moving_bloc_position
    moving_bloc_position[0] -= 1
    moving_bloc = future_bloc
    moving_bloc_position = future_bloc_position
    grille = add_piece(last_moving_bloc, last_moving_bloc_position, grille)
    return moving_bloc, moving_bloc_position, last_moving_bloc, last_moving_bloc_position, grille, running

#Collisions par rotation
def check_up_collision(moving_bloc, moving_bloc_position, grille):
    #On essaie une rotation
    rotated = rotate(moving_bloc)
    rotated_position = moving_bloc_position
    if moving_bloc == [[7, 7, 7, 7]]:
        rotated_position[1] += 1
    elif moving_bloc == [[7], [7], [7], [7]]:
        rotated_position[1] -= 1
    #Bloc ne doit pas exéder la taille de la grille
    if rotated_position[1] + len(rotated[0]) <= len(grille[0]) and rotated_position[0] + len(rotated) <= len(grille):
        #Check for collisions
        for i in range(len(rotated)):
            for u in range(len(rotated[i])):
                if rotated[i][u] != 0:
                    if grille[rotated_position[0]+i][rotated_position[1]+u] != 0:
                        return moving_bloc, moving_bloc_position
        return rotated, rotated_position
    else:
        #Le bloc ne peut pas tourner, on n'applique pas la rotation
        return moving_bloc, moving_bloc_position

#Collisions latérales
def check_collision(moving_bloc, moving_bloc_position, grille, direction):
    if direction == "right":
        #On essaie de le déplacer
        moving_bloc_position[1] += 1
        #Bloc ne doit pas exéder la taille de la grille
        if moving_bloc_position[1] + len(moving_bloc[0]) <= len(grille[0]):
            #Check for collisions
            for i in range(len(moving_bloc)):
                for u in range(len(moving_bloc[i])):
                    if moving_bloc[i][u] != 0:
                        if grille[moving_bloc_position[0]+i][moving_bloc_position[1]+u] != 0:
                            #Ici il y a collision 
                            moving_bloc_position[1] -= 1
                            return moving_bloc_position
            #Ici il n'y en a pas
            return moving_bloc_position
        else:
            #Ici le bloc déborde, on annule le mouvement
            moving_bloc_position[1] -= 1
            return moving_bloc_position
    elif direction == "left":
        #Pareil que pour droite mais à gauche
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

#Fonction de rotation
def rotate(moving_bloc):
    moving_bloc_rotated = [0]*len(moving_bloc[0])
    for i in range(len(moving_bloc_rotated)):
        moving_bloc_rotated[i] = [0]*len(moving_bloc)
    for i in range(len(moving_bloc)):
        for u in range(len(moving_bloc[i])):
            moving_bloc_rotated[u][len(moving_bloc)-1-i] = moving_bloc[i][u]
    return moving_bloc_rotated

#Effectuer une multiplication de ligne
def product(liste: list) -> int:
    result = 1
    for i in liste:
        result *= i
    return result

#Fonction de nettoyage des lignes
def is_in_a_line(grille):
    for i in range(len(grille)):
        if product(grille[i]) != 0:
            grille.pop(i)
            grille = grille[::-1]
            grille.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            grille = grille[::-1]
    return grille

#Ajouter la pièce à la grille
def add_piece(moving_bloc, moving_bloc_position, grille):
    for i in range(len(moving_bloc)):
        for u in range(len(moving_bloc[i])):
            if moving_bloc[i][u] != 0:
                grille[moving_bloc_position[0]+i][moving_bloc_position[1]+u] = moving_bloc[i][u]
    return grille