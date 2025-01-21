#Nos importations
import pygame
from pygame.locals import *
from functions import *
from variables import *

#Initialisation
pygame.init()
main_window = pygame.display.set_mode((800, 500), RESIZABLE)
main_window = pygame.display.set_mode()
screen_resolution = list(main_window.get_size())
main_window = pygame.display.set_mode((800, 500), RESIZABLE)
pygame.display.set_caption("Tétris")
pygame.display.set_icon(pygame.image.load("Tetris.jpg"))
clock = pygame.time.Clock()
last_update = pygame.time.get_ticks() + 2*vitesse
running = True

"""
BUG : 
-   Implémenter que la pièce baton se décale
-   La fonction de reset ne se declenche pas lorsque que Key_r is pressed

TODO :
- Le meilleur score de la session
- Changer couleur lettre + graphiques
- Niveaux ! Vitesse !
- Fenêtre de jeu game over
- Fenêtre paramètres de jeu : arrêt et replay 
- Bordure à droite avec bouton paramètres 
- Paramètres à gauche avec paramètres de vitesse
- Bordure grille de jeu
"""

while game_on:
    #Variable qui contient les touches pressées
    keys = pygame.key.get_pressed()

    #Limiter les fps à 60
    clock.tick(60)

    #Tout ce qui a un rapport avec l'affichage
    main_window.fill(color[1])
    width, height = pygame.display.get_surface().get_size()
    pixel = update_window(width, height)

    #Boucle du jeu
    if running:     
        #La pièce qui tombe toutes les vitesse/1000 seconde
        if pygame.time.get_ticks() >= last_update:
            bloc_bundle, grille, running, score_bundle = check_down_collision(bloc_bundle, grille, score_bundle)
            last_update = pygame.time.get_ticks() + vitesse
        
        #Tous les événements
        for event in pygame.event.get():
            #Fonction de fermeture
            if event.type == pygame.QUIT:
                running = False
                game_on = False
            
            #Les touches pressées
            if event.type == pygame.KEYDOWN:
                #Pause rapide du jeu
                if event.key == pygame.K_SPACE:
                    running = not running

                #Debug
                if event.key == pygame.K_p:
                    debug(grille)
                    print(bloc_bundle[1])
                    debug(bloc_bundle[0])

                #Changer rapidement la fenêtre
                if event.key == pygame.K_s:
                    if main_window.get_size() != (500, 500):
                        main_window = pygame.display.set_mode((500, 500), RESIZABLE)
                    else:
                        main_window = pygame.display.set_mode()
                        pygame.display.toggle_fullscreen()

                #Mouvement
                if event.key == pygame.K_DOWN:
                    bloc_bundle, grille, running, score_bundle = check_down_collision(bloc_bundle, grille, score_bundle)
                if event.key == pygame.K_UP:
                    bloc_bundle = check_up_collision(bloc_bundle, grille)
                if event.key == pygame.K_RIGHT:
                    bloc_bundle[1] = check_collision(bloc_bundle, grille, direction[2])
                if event.key == pygame.K_LEFT:
                    bloc_bundle[1] = check_collision(bloc_bundle, grille, direction[3])

        #Aller vite
        if keys[pygame.K_DOWN]:
            bloc_bundle, grille, running, score_bundle = check_down_collision(bloc_bundle, grille, score_bundle)

        #Game over
        if grille[0] != [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] and bloc_bundle[1][0] != 0:
            running = False

        #Changement level
        if score_bundle[1] >= 10 :
            score_bundle[0] +=1
            score_bundle[1] = 0
            vitesse -= vitesse*10/100
        
        #High_score
        if score_bundle[2] > score_bundle[3]:
            score_bundle[3] = score_bundle[2]
            score_bundle[5] = score_bundle[4]
    
    if not running:
        #Tous les évènements 
        for event in pygame.event.get():
            #Fonction de fermeture
            if event.type == pygame.QUIT:
                running = False
                game_on = False
            
            #Pause rapide du jeu
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                running = not running

            #Debug
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                debug(grille)
                print(bloc_bundle[1])
                debug(bloc_bundle[0])

            #Changer rapidement la fenêtre
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                if main_window.get_size() != (500, 500):
                    main_window = pygame.display.set_mode((500, 500), RESIZABLE)
                else:
                    main_window = pygame.display.set_mode()
    
    #Tout le temps actif
    #Remplissage des couleurs dans la grille
    #Variable pour centrer la grille
    top_left_corner = [width/2 - 5*pixel, height/2 - 11*pixel]
    if list(main_window.get_size())[0] == good_screen_resolution[0] and list(main_window.get_size())[1] == good_screen_resolution[1]:
        pygame.draw.rect(main_window, color[0], pygame.Rect(top_left_corner[0] - int(1/2*pixel), top_left_corner[1] - int(1/2*pixel), 11*pixel, 23*pixel), int(1/2*pixel))
    for y in range(len(grille)):
        for x in range(len(grille[y])):
            pygame.draw.rect(main_window, color[0], pygame.Rect(x*pixel + top_left_corner[0], y*pixel + top_left_corner[1], pixel, pixel), 1)
            if grille[y][x] != 0:
                pygame.draw.rect(main_window, color[grille[y][x]], pygame.Rect(x*pixel + top_left_corner[0]+1, y*pixel + top_left_corner[1]+1, pixel-2, pixel-2))
                pygame.draw.rect(main_window, brighter_color[grille[y][x]], pygame.Rect(x*pixel + top_left_corner[0] + int(1/4*pixel), y*pixel + top_left_corner[1] + int(1/4*pixel), int(1/4*pixel), int(1/4*pixel)))
    #Dessiner la pièce qui bouge
    for y in range(len(bloc_bundle[0])):
        for x in range(len(bloc_bundle[0][y])):
            if bloc_bundle[0][y][x] != 0:
                pygame.draw.rect(main_window, color[bloc_bundle[0][y][x]], pygame.Rect(x*pixel + top_left_corner[0]+1 + pixel*bloc_bundle[1][1], y*pixel + top_left_corner[1]+1 + pixel*bloc_bundle[1][0], pixel-2, pixel-2))
                pygame.draw.rect(main_window, brighter_color[bloc_bundle[0][y][x]], pygame.Rect(x*pixel + top_left_corner[0] + int(1/4*pixel) + pixel*bloc_bundle[1][1], y*pixel + top_left_corner[1] + int(1/4*pixel) + pixel*bloc_bundle[1][0], int(1/4*pixel), int(1/4*pixel)))
    #Dessiner la pièce qui va venir
    for y in range(len(blocs[bloc_bundle[4][1][bloc_bundle[4][0]]])):
        for x in range(len(blocs[bloc_bundle[4][1][bloc_bundle[4][0]]][y])):
            if blocs[bloc_bundle[4][1][bloc_bundle[4][0]]][y][x] != 0:
                pygame.draw.rect(main_window, color[0], pygame.Rect((x+7)*pixel + width/2, (y-9)*pixel + height/2, pixel, pixel), 2)
                pygame.draw.rect(main_window, color[blocs[bloc_bundle[4][1][bloc_bundle[4][0]]][y][x]], pygame.Rect((x+7)*pixel + width/2 + 1, (y-9)*pixel + height/2 + 1, pixel-2, pixel-2))
                pygame.draw.rect(main_window, brighter_color[blocs[bloc_bundle[4][1][bloc_bundle[4][0]]][y][x]], pygame.Rect((x+7)*pixel + width/2 + int(1/4*pixel), (y-9)*pixel + height/2 + int(1/4*pixel), int(1/4*pixel), int(1/4*pixel)))


    #Fonction de reset de la grille
    if keys[pygame.K_r]:
        grille, bloc_bundle, running, score_bundle = reset(score_bundle)

    #Afficher le titre au dessus
    police = pygame.font.Font("Brick Tetris.otf", 2*pixel)
    game_title =  police.render("TÉTRIS", True, color[8], color[1])
    game_titleRect = game_title.get_rect()
    game_titleRect.center = (width/2, height/2 - 13*pixel)
    main_window.blit(game_title, game_titleRect)

    #Afficher le score
    score_display =  police.render(str(score_bundle[2]), True, score_bundle[4])
    score_displayRect = score_display.get_rect()
    score_displayRect.topleft = (width/2 + 7*pixel, height/2 - 11*pixel)
    main_window.blit(police.render("Score : ", True, color[0]), score_displayRect)
    score_displayRect.topleft = (width/2 + 7*pixel + police.render("Score : ", True, color[0]).get_rect().width, height/2 - 11*pixel)
    main_window.blit(score_display, score_displayRect)

    #Afficher le high_score
    high_score_display =  police.render(str(score_bundle[3]), True, score_bundle[5])
    high_score_displayRect = high_score_display.get_rect()
    high_score_displayRect.topleft = (width/2 + 7*pixel, height/2 - 6*pixel)
    main_window.blit(police.render("Highscore : ", True, color[0]), high_score_displayRect)
    high_score_displayRect.topleft = (width/2 + 7*pixel + police.render("Highscore : ", True, color[0]).get_rect().width, height/2 - 6*pixel)
    main_window.blit(high_score_display, high_score_displayRect)

    #Actualiser l'écran
    pygame.display.flip()

#Quitter le programme
pygame.quit()