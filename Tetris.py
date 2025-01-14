#Nos importations
import pygame
from pygame.locals import *
from functions import *
from variables import *

#Initialisation
pygame.init()
main_window = pygame.display.set_mode((700,700), RESIZABLE)
"""pygame.display.toggle_fullscreen()"""
pygame.display.set_caption("Tétris")
pygame.display.set_icon(pygame.image.load("Tetris.jpg"))
clock = pygame.time.Clock()
last_update = pygame.time.get_ticks() + 2*vitesse
police = pygame.font.Font("Brick Tetris.ttf", 2*pixel)
game_title =  police.render("TÉTRIS", True , color[4], color[1])
game_titleRect = game_title.get_rect()
running = True

while game_on:
    #Boucle du jeu
    if running:
        #Limiter les fps à 60
        clock.tick(60)

        #Tout ce qui a un rapport avec l'affichage
        main_window.fill(color[1])
        width, height = pygame.display.get_surface().get_size()
        pixel = update_window(width, height)
       
        """
        BUG : 
        -   Implémenter que la pièce baton se décale
        -   La fonction de reset ne se declenche pas lorsque que Key_r is pressed 
        Idée de la cause : la fonction de création pièces run sans s'arrêter, le programme continue à l'infini et ne sort pas de la boucle
        """

        #Variable qui contient les touches pressées
        keys = pygame.key.get_pressed()

        #La pièce qui tombe toutes les vitesse/1000 seconde
        if pygame.time.get_ticks() >= last_update:
            bloc_bundle, grille, running = check_down_collision(bloc_bundle, grille)
            last_update = pygame.time.get_ticks() + vitesse
        
        #Tous les événements
        for event in pygame.event.get():
            #Fonction de fermeture
            if event.type == pygame.QUIT:
                running = False
                game_on = False

            #Debug
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_p:
                    debug(grille)
                    print(bloc_bundle[1])
                    debug(bloc_bundle[0])
            
            #Mouvement
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    bloc_bundle, grille, running, lines_cleared = check_down_collision(bloc_bundle, grille)
                if event.key == pygame.K_UP:
                    bloc_bundle[0], bloc_bundle[1] = check_up_collision(bloc_bundle, grille)
                if event.key == pygame.K_RIGHT:
                    bloc_bundle[1] = check_collision(bloc_bundle, grille, direction[2])
                if event.key == pygame.K_LEFT:
                    bloc_bundle[1] = check_collision(bloc_bundle, grille, direction[3])

        #Aller vite
        if keys[pygame.K_DOWN]:
            bloc_bundle, grille, running, lines_cleared = check_down_collision(bloc_bundle, grille)
            bloc_bundle, grille, running = check_down_collision(bloc_bundle, grille)
        
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
        for y in range(len(bloc_bundle[0])):
            for x in range(len(bloc_bundle[0][y])):
                if bloc_bundle[0][y][x] != 0:
                    pygame.draw.rect(main_window, color[bloc_bundle[0][y][x]], pygame.Rect(x*pixel + top_right_corner[0]+1 + pixel*bloc_bundle[1][1], y*pixel + top_right_corner[1]+1 + pixel*bloc_bundle[1][0], pixel-2, pixel-2))

        #Game over

        if grille[0] != [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] and bloc_bundle[1][0] != 0:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_r]:
        grille, bloc_bundle, running = reset()
    
    #Score pour chaque ligne detruite
    if lines_cleared == 1 :
        score_total += 40(level_game+1)
        total_cleared_lines += lines_cleared
    elif lines_cleared == 2 :
        score_total += 100(level_game+1)
        total_cleared_lines += lines_cleared
    elif lines_cleared == 3 : 
        score_total += 300(level_game +1)
        total_cleared_lines += lines_cleared
    elif lines_cleared == 4 :
        score_total += 1200(level_game+1)
        total_cleared_lines += lines_cleared

    #Changement level
    if total_cleared_lines >= 10 :
        level_game +=1
        total_cleared_lines = 0 
    


    #Afficher les trucs que l'on veut sur le côté
    """
    Ce que l'on veut :
        - Le jeu au centre
        - Le score
        - Les prochaines pièces 
        - Le meilleur score de la session
        - Tétris, écrit en gros ou une image *non* pixelisée
        - Changer couleur lettre + graphiques
        - Niveaux ! Vitesse !
    """
    game_titleRect.center = (width/2, height/2 - 13*pixel)
    main_window.blit(game_title, game_titleRect)
    
    #Actualiser l'écran
    pygame.display.flip()

#Quitter le programme
pygame.quit()