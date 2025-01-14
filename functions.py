from pygame import *
from pygame.locals import *
from variables import blocs 
from random import shuffle as sh

#Toutes nos fonctions

#Ajuster la taille des composants
def update_window(width, height):
    if height <= 2.2*width:
        pixel = height//22
    elif height > 2.2*width:
        pixel = width//10
    return int((8/10)*pixel)


#Debug. Print la grille pour afficher ses valeurs
def debug(grille):
    print("____________________________________________________")
    for i in grille:
        print(i)
    print("____________________________________________________")

#Fonctions ou on cherche de potentielles collisions
def check_down_collision(bloc_bundle, grille):
    running = True
    #On essaie de faire descendre la pièce
    bloc_bundle[1][0] += 1
    #Bloc ne doit pas exéder la taille de la grille
    if bloc_bundle[1][0] + len(bloc_bundle[0]) <= len(grille):
        #Check for collisions
        for i in range(len(bloc_bundle[0])):
            for u in range(len(bloc_bundle[0][i])):
                if bloc_bundle[0][i][u] != 0:
                    if grille[bloc_bundle[1][0]+i][bloc_bundle[1][1]+u] != 0:
                        #Ici il y a collision, on ajoute une nouvelle pièce
                        bloc_bundle[1][0] -= 1
                        bloc_bundle, grille, running = new_piece(bloc_bundle, grille)
                        if not running:
                            #On arrête le programme
                            return bloc_bundle, grille, running
                        grille, bloc_bundle[1], number_lines = is_in_a_line(grille, bloc_bundle[1], number_lines)
                        lines_cleared=number_lines
                        number_lines=0
                        return bloc_bundle, grille, running, lines_cleared #On retourne running pour arrêter la partie
        #Si pas de collision
        return bloc_bundle, grille, running
    #La pièce touche le bas de la grille
    else:
        bloc_bundle[1][0] -= 1
        return new_piece(bloc_bundle, grille)

#Ajouter une nouvelle pièce
def new_piece(bloc_bundle, grille):
    running = True
    #Ici, la pièce a rencontré un obstacle, on en créé une autre et on nettoie la grille
    #Check for a potential collision at spawn
    #Création d'un potentiel bloc qui doit vérifier des conditions pour venir dans le jeu, sinon Game Over
    future_bloc = blocs[bloc_bundle[4][1][bloc_bundle[4][0]]]
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
    bloc_bundle[2], bloc_bundle[3] = bloc_bundle[0], bloc_bundle[1]
    bloc_bundle[0] = future_bloc
    bloc_bundle[1] = future_bloc_position
    #On ajoute la pièce
    grille = add_piece(bloc_bundle[2], bloc_bundle[3], grille)
    #Check remplissage de la grille
    grille, bloc_bundle[1] = is_in_a_line(grille, bloc_bundle[1])
    bloc_bundle[4][0] += 1
    if bloc_bundle[4][0] == 7:
        bloc_bundle[4][0] = 0
        bloc_bundle[4][1] = bloc_bundle[4][2]
        sh(bloc_bundle[4][2])
    return bloc_bundle, grille, running

#Collisions par rotation
def check_up_collision(bloc_bundle, grille):
    #On essaie une rotation
    rotated = rotate(bloc_bundle[0])
    rotated_position = bloc_bundle[1]
    if bloc_bundle[0] == [[7, 7, 7, 7]]:
        rotated_position[1] += 1
    elif bloc_bundle[0] == [[7], [7], [7], [7]]:
        rotated_position[1] -= 1
    #Bloc ne doit pas exéder la taille de la grille
    if rotated_position[1] + len(rotated[0]) <= len(grille[0]) and rotated_position[0] + len(rotated) <= len(grille):
        #Check for collisions
        for i in range(len(rotated)):
            for u in range(len(rotated[i])):
                if rotated[i][u] != 0:
                    if grille[rotated_position[0]+i][rotated_position[1]+u] != 0:
                        return bloc_bundle[0], bloc_bundle[1]
        return rotated, rotated_position
    else:
        #Le bloc ne peut pas tourner, on n'applique pas la rotation
        return bloc_bundle[0], bloc_bundle[1]

#Collisions latérales
def check_collision(bloc_bundle, grille, direction):
    if direction == "right":
        #On essaie de le déplacer
        bloc_bundle[1][1] += 1
        #Bloc ne doit pas exéder la taille de la grille
        if bloc_bundle[1][1] + len(bloc_bundle[0][0]) <= len(grille[0]):
            #Check for collisions
            for i in range(len(bloc_bundle[0])):
                for u in range(len(bloc_bundle[0][i])):
                    if bloc_bundle[0][i][u] != 0:
                        if grille[bloc_bundle[1][0]+i][bloc_bundle[1][1]+u] != 0:
                            #Ici il y a collision 
                            bloc_bundle[1][1] -= 1
                            return bloc_bundle[1]
            #Ici il n'y en a pas
            return bloc_bundle[1]
        else:
            #Ici le bloc déborde, on annule le mouvement
            bloc_bundle[1][1] -= 1
            return bloc_bundle[1]
    elif direction == "left":
        #Pareil que pour droite mais à gauche
        bloc_bundle[1][1] -= 1
        #Bloc ne doit pas exéder la taille de la grille
        if bloc_bundle[1][1] >= 0:
            #Check for collisions
            for i in range(len(bloc_bundle[0])):
                for u in range(len(bloc_bundle[0][i])):
                    if bloc_bundle[0][i][u] != 0:
                        if grille[bloc_bundle[1][0]+i][bloc_bundle[1][1]+u] != 0:
                            bloc_bundle[1][1] += 1
                            return bloc_bundle[1]
            return bloc_bundle[1]
        else:
            bloc_bundle[1][1] += 1
            return bloc_bundle[1]

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
def is_in_a_line(grille, moving_bloc_position, number_lines):
    for i in range(len(grille)):
        if product(grille[i]) != 0:
            number_lines +=1
            grille.pop(i)
            grille = grille[::-1]
            grille.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            grille = grille[::-1]
            moving_bloc_position[0] += 1
    return grille, moving_bloc_position, number_lines

#Ajouter la pièce à la grille
def add_piece(last_moving_bloc, last_moving_bloc_position, grille):
    for i in range(len(last_moving_bloc)):
        for u in range(len(last_moving_bloc[i])):
            if last_moving_bloc[i][u] != 0:
                grille[last_moving_bloc_position[0]+i][last_moving_bloc_position[1]+u] = last_moving_bloc[i][u]
    return grille

#Fonction de reset de la grille
def reset():
    running = True
    bloc_list = [0,1,2,3,4,5,6]
    bloc_list_1 = bloc_list.copy()
    bloc_list_2 = bloc_list.copy()
    sh(bloc_list_1)
    sh(bloc_list_2)
    counting_list = [0, bloc_list_1, bloc_list_2]
    moving_bloc = last_moving_bloc = blocs[counting_list[1][counting_list[0]]]
    counting_list[0] += 1
    moving_bloc_position = last_moving_bloc_position = [0, 3]   #y, x
    if moving_bloc == blocs[1]:
        moving_bloc_position = last_moving_bloc_position = [0, 4]    

    bloc_bundle = [moving_bloc, moving_bloc_position, last_moving_bloc, last_moving_bloc_position, counting_list]

    #Grille
    grille = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
    return grille, bloc_bundle, running