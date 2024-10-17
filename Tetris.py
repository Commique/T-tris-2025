#Nos importations
import pygame
from pygame.locals import *
from functions import *
from variables import *
from random import randint as ri

#Initialisation
pygame.init()
main_window = pygame.display.set_mode((10*pixel,22*pixel), RESIZABLE)
pygame.display.set_caption("Tétris")
pygame.display.set_icon(pygame.image.load("Tetris.jpg"))
clock = pygame.time.Clock()
last_update = pygame.time.get_ticks() + vitesse

#Boucle du jeu
while running:
    #Limiter les fps à 60
    clock.tick(60)

    #Tout ce qui a un rapport avec l'affichage
    main_window.fill(color[1])
    width, height = pygame.display.get_surface().get_size()
    pixel = update_window(width, height)

    #Variable qui contient les touches pressées
    keys = pygame.key.get_pressed()

    #Enlever de la grille la pièce qui tombe
    for i in range(len(moving_bloc)):
        for u in range(len(moving_bloc[i])):
            if moving_bloc[i][u] != 0:
                grille[moving_bloc_position[0]+i][moving_bloc_position[1]+u] = 0

    #La pièce qui tombe toutes les 1 seconde
    if pygame.time.get_ticks() >= last_update:
        moving_bloc, moving_bloc_position, moving_bloc_color, last_moving_bloc, last_moving_bloc_position, last_moving_bloc_color = check_down_collision(moving_bloc, moving_bloc_position, moving_bloc_color, grille, last_moving_bloc, last_moving_bloc_position, last_moving_bloc_color)
        last_update = last_update = pygame.time.get_ticks() + vitesse
    
    #Tous les événements
    for event in pygame.event.get():
        #Fonction de fermeture
        if event.type == pygame.QUIT:
            running = False
        
        #Debug
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_p:
                debug(grille)
        
        #Mouvement + Collisions /!\ IMPORTANT /!\
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                if check_up_collision():
                    moving_bloc = rotate(moving_bloc)
            if event.key == pygame.K_RIGHT:
                if check_collision(moving_bloc, moving_bloc_position, grille, direction[2]):
                    moving_bloc_position[1] += 1
            if event.key == pygame.K_LEFT:
                if check_collision(moving_bloc, moving_bloc_position, grille, direction[3]):
                    moving_bloc_position[1] -= 1

    #Tomber vite
    if keys[pygame.K_DOWN]:
        moving_bloc, moving_bloc_position, moving_bloc_color, last_moving_bloc, last_moving_bloc_position, last_moving_bloc_color = check_down_collision(moving_bloc, moving_bloc_position, moving_bloc_color, grille, last_moving_bloc, last_moving_bloc_position, last_moving_bloc_color)

    #Redessiner la pièce qui vient de se faire enlever car la fonction n'était pas à jour
    for i in range(len(last_moving_bloc)):
        for u in range(len(last_moving_bloc[i])): 
            if last_moving_bloc[i][u] != 0:
                grille[last_moving_bloc_position[0]+i][last_moving_bloc_position[1]+u] = last_moving_bloc[i][u]

    #Ajouter à la grille la pièce qui tombe (On a déjà tout vérifié)
    for i in range(len(moving_bloc)):
        for u in range(len(moving_bloc[i])):
            if moving_bloc[i][u] != 0:
                grille[moving_bloc_position[0]+i][moving_bloc_position[1]+u] = moving_bloc[i][u]

    #Fonction de fermeture alternative
    if keys[pygame.K_w]:
        running = False

    #Remplissage des couleurs dans la grille
    top_right_corner = [width/2 - 5*pixel, height/2 - 11*pixel]
    for y in range(len(grille)):
        for x in range(len(grille[y])):
            pygame.draw.rect(main_window, color[0], pygame.Rect(x*pixel + top_right_corner[0], y*pixel + top_right_corner[1], pixel, pixel), 1)
            if grille[y][x] != 0:
                pygame.draw.rect(main_window, color[grille[y][x]], pygame.Rect(x*pixel + top_right_corner[0]+1, y*pixel + top_right_corner[1]+1, pixel-2, pixel-2))
    

    #Actualiser l'écran
    pygame.display.flip()


#Quitter le programme
pygame.quit()