import pygame
from pygame.locals import *
from functions import *
from variables import *
from random import randint as ri

pygame.init()
main_window = pygame.display.set_mode((10*pixel,22*pixel), RESIZABLE)
pygame.display.set_caption("Tétris")
pygame.display.set_icon(pygame.image.load("Tetris.jpg"))
clock = pygame.time.Clock()
last_update = pygame.time.get_ticks() + 2000


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
    y = -1
    for i in moving_bloc:
        y += 1
        x = -1
        for u in i:
            x += 1
            if moving_bloc[y][x] != 0:
                grille[moving_bloc_position[0]+y][moving_bloc_position[1]+x] = 0

    #La pièce qui tombe toutes les 1 seconde
    if pygame.time.get_ticks() >= last_update:
        last_update = last_update = pygame.time.get_ticks() + 1000
        moving_bloc_position[0] += 1
    
    #Collisions /!\ IMPORTANT
    #pass for now    

    #Ajouter à la grille la pièce qui tombe (On a déjà tout vérifié)
    y = -1
    for i in moving_bloc:
        y += 1
        x = -1
        for u in i:
            x += 1
            if moving_bloc[y][x] != 0:
                grille[moving_bloc_position[0]+y][moving_bloc_position[1]+x] = moving_bloc[y][x]

    #Tous les événements
    for event in pygame.event.get():
        #Fonction de fermeture
        if event.type == pygame.QUIT:
            running = False
        
        #Debug
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_p:
                debug(grille)

    #Fonction de fermeture alternative
    if keys[pygame.K_w]:
        running = False

    #Remplissage des couleurs dans la grille
    top_right_corner = [width/2 - 5*pixel, height/2 - 11*pixel]
    y = -1
    for i in grille:
        y += 1
        x = -1
        for u in i:
            x += 1
            pygame.draw.rect(main_window, color[0], pygame.Rect(x*pixel + top_right_corner[0], y*pixel + top_right_corner[1], pixel, pixel), 1)
            if u != 0:
                pygame.draw.rect(main_window, color[u], pygame.Rect(x*pixel + top_right_corner[0]+1, y*pixel + top_right_corner[1]+1, pixel-2, pixel-2))
    


    pygame.display.flip()



pygame.quit()