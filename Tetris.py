#Nos importations
import pygame
from pygame.locals import *
from functions import *
from variables import *


#/!\ IMPORTANT : utiliser emumerate() à la place de range() /!\
#=> Fonctions


#Initialisation
pygame.init()
main_window = pygame.display.set_mode((10*pixel,22*pixel), RESIZABLE)
pygame.display.set_caption("Tétris")
pygame.display.set_icon(pygame.image.load("Tetris.jpg"))
clock = pygame.time.Clock()
last_update = pygame.time.get_ticks() + 2*vitesse

while game_on:
    #Boucle du jeu
    while running:
        #Limiter les fps à 60
        clock.tick(60)

        #Tout ce qui a un rapport avec l'affichage
        main_window.fill(color[1])
        width, height = pygame.display.get_surface().get_size()
        pixel = update_window(width, height)

        """
        Bugs : 
        -   Le nettoyage de la grille ne se fait pas correctement, certaines fois deux pièce apparaissent, mettant fin au jeu
        => L'appel de la fonction de nettoyage n'est pris en compte par les autres fonctions
        Modifier le random
        Draw la pièce séparément
        """

        #Variable qui contient les touches pressées
        keys = pygame.key.get_pressed()
        
        #La pièce qui tombe toutes les vitesse/1000 seconde
        if pygame.time.get_ticks() >= last_update:
            moving_bloc, moving_bloc_position, last_moving_bloc, last_moving_bloc_position, grille, running = check_down_collision(moving_bloc, moving_bloc_position, grille, last_moving_bloc, last_moving_bloc_position)
            last_update = pygame.time.get_ticks() + vitesse
        
        #Tous les événements
        for event in pygame.event.get():
            #Fonction de fermeture
            if event.type == pygame.QUIT:
                running = False
            
            #Debug
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_p:
                    debug(grille)
                    print(moving_bloc_position)
                    debug(moving_bloc)
            
            #Mouvement
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    moving_bloc, moving_bloc_position, last_moving_bloc, last_moving_bloc_position, grille, running = check_down_collision(moving_bloc, moving_bloc_position, grille, last_moving_bloc, last_moving_bloc_position)
                if event.key == pygame.K_UP:
                    moving_bloc, moving_bloc_position = check_up_collision(moving_bloc, moving_bloc_position, grille)
                if event.key == pygame.K_RIGHT:
                    moving_bloc_position = check_collision(moving_bloc, moving_bloc_position, grille, direction[2])
                if event.key == pygame.K_LEFT:
                    moving_bloc_position = check_collision(moving_bloc, moving_bloc_position, grille, direction[3])

        #Aller vite
        if keys[pygame.K_DOWN]:
            moving_bloc, moving_bloc_position, last_moving_bloc, last_moving_bloc_position, grille, running = check_down_collision(moving_bloc, moving_bloc_position, grille, last_moving_bloc, last_moving_bloc_position)
        
        #Fonction de fermeture alternative
        if keys[pygame.K_w]:
            running = False

        #Remplissage des couleurs dans la grille
        #Variable pour centrer la grille
        top_right_corner = [width/2 - 5*pixel, height/2 - 11*pixel]
        for y in range(len(grille)):
            for x in range(len(grille[y])):
                pygame.draw.rect(main_window, color[0], pygame.Rect(x*pixel + top_right_corner[0], y*pixel + top_right_corner[1], pixel, pixel), 1)
                if grille[y][x] != 0:
                    pygame.draw.rect(main_window, color[grille[y][x]], pygame.Rect(x*pixel + top_right_corner[0]+1, y*pixel + top_right_corner[1]+1, pixel-2, pixel-2))
        #Dessiner la pièce qui bouge
        for y in range(len(moving_bloc)):
            for x in range(len(moving_bloc[y])):
                if moving_bloc[y][x] != 0:
                    pygame.draw.rect(main_window, color[moving_bloc[y][x]], pygame.Rect(x*pixel + top_right_corner[0]+1 + pixel*moving_bloc_position[1], y*pixel + top_right_corner[1]+1 + pixel*moving_bloc_position[0], pixel-2, pixel-2))

        #Game over
        if grille[0] != [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] and moving_bloc_position[0] != 0:
            running = False

        #Actualiser l'écran
        pygame.display.flip()
    
    break

#Quitter le programme
pygame.quit()