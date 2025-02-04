from pygame import *
from pygame.locals import *
from variables import blocs, colors
from random import shuffle as sh, randint as  ri

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
def check_down_collision(bloc_bundle, grille, score_bundle):
    running = True
    lines_cleared = 0
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
                        bloc_bundle, grille, running, score_bundle = new_piece(bloc_bundle, grille, score_bundle)
                        #On retourne running au cas ou la partie est terminée
                        return bloc_bundle, grille, running, score_bundle
        #Si pas de collision
        return bloc_bundle, grille, running, score_bundle
    #La pièce touche le bas de la grille
    else:
        bloc_bundle[1][0] -= 1
        return new_piece(bloc_bundle, grille, score_bundle)

#Ajouter une nouvelle pièce
def new_piece(bloc_bundle, grille, score_bundle):
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
    grille, bloc_bundle[1], lines_cleared = is_in_a_line(grille, bloc_bundle[1])
    score_bundle = score_function(lines_cleared, score_bundle)
    bloc_bundle[4][0] += 1
    if bloc_bundle[4][0] == 7:
        bloc_bundle[4][0] = 0
        bloc_bundle[4][1] = bloc_bundle[4][2]
        sh(bloc_bundle[4][2])
    return bloc_bundle, grille, running, score_bundle

#Collisions par rotation
def check_up_collision(bloc_bundle, grille):
    #On essaie une rotation
    rotated = rotate(bloc_bundle[0])
    rotated_position = bloc_bundle[1]
    if bloc_bundle[0] == [[6, 6, 6, 6]]:
        rotated_position[1] += 1
    elif bloc_bundle[0] == [[6], [6], [6], [6]]:
        rotated_position[1] -= 1
    #Bloc ne doit pas exéder la taille de la grille
    if rotated_position[1] >= 0 and rotated_position[1] + len(rotated[0]) <= len(grille[0]) and rotated_position[0] + len(rotated) <= len(grille):
        #Check for collisions
        for i in range(len(rotated)):
            for u in range(len(rotated[i])):
                if rotated[i][u] != 0:
                    if grille[rotated_position[0]+i][rotated_position[1]+u] != 0:
                        return bloc_bundle
        bloc_bundle[0] = rotated
        bloc_bundle[1] = rotated_position
        return bloc_bundle
    else:
        #Le bloc ne peut pas tourner, on n'applique pas la rotation
        if bloc_bundle[0] == [[6, 6, 6, 6]]:
            rotated_position[1] -= 1
        elif bloc_bundle[0] == [[6], [6], [6], [6]]:
            rotated_position[1] += 1
        return bloc_bundle

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
def is_in_a_line(grille, moving_bloc_position):
    number_lines = 0
    for i in range(len(grille)):
        if product(grille[i]) != 0:
            number_lines += 1
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
def reset(last_score_bundle):
    running = True
    
    level_game = 0
    total_cleared_lines = 0
    score_total = 0
    high_score = last_score_bundle[3]
    score_color = (0,0,0)
    high_score_color = last_score_bundle[5]
    score_bundle = [level_game, total_cleared_lines, score_total, high_score, score_color, high_score_color]

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
    #Reset Bloc Bundle
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

    vitesse = 300
    return grille, bloc_bundle, running, score_bundle, vitesse

#Fonction de calcul de score 
def score_function(lines_cleared, score_bundle):
    if lines_cleared == 1 :
        score_bundle[2] += 40*(score_bundle[0] + 1)
        score_bundle[1] += lines_cleared
    elif lines_cleared == 2 :
        score_bundle[2] += 100*(score_bundle[0] + 1)
        score_bundle[1] += lines_cleared
    elif lines_cleared == 3 : 
        score_bundle[2] += 300*(score_bundle[0] + 1)
        score_bundle[1] += lines_cleared
    elif lines_cleared == 4 :
        score_bundle[2] += 1200*(score_bundle[0] + 1)
        score_bundle[1] += lines_cleared
    if lines_cleared != 0:
        score_bundle[4] = colors[0][0]
    return score_bundle