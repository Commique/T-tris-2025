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
police = pygame.font.Font("MarkaziText-Bold.ttf", 2*pixel)
running = True
buttons = []
pygame.mixer.init()
pygame.mixer.music.load(playlist[current_theme])
pygame.mixer.music.play()

#Defintion propriétés des boutons
class Button():
    def __init__(self, x, y, width, height, default_color, hovered_color, pressed_color, text_color, button_text, onclickFunction=None, rendering=True):
        #Définir la police pour les boutons
        police = pygame.font.Font("MarkaziText-Bold.ttf", pixel)

        #Définir les variables
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.alreadyPressed = False
        self.rendering = rendering
        self.text_color = text_color

        #Définir les propriétés du bouton
        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.buttonRect.topleft = (self.x, self.y)
        self.buttonSurf = police.render(button_text, True, self.text_color)

        #Ajouter le bouton à la liste des boutons
        buttons.append(self)

        #Définir les différentes couleurs du bouton
        self.fillColors = {
            'normal': default_color,
            'hover': hovered_color,
            'pressed': pressed_color,
        }

    #Fonctionnement des boutons 
    def process_button(self):
        if self.rendering:
            mousePos = pygame.mouse.get_pos()
            #Etat par défaut
            self.buttonSurface.fill(self.fillColors['normal'])
            if self.buttonRect.collidepoint(mousePos):
                #La souris est sur le bouton
                self.buttonSurface.fill(self.fillColors['hover'])
                if pygame.mouse.get_pressed(num_buttons=3)[0]:
                    #Le bouton est pressé
                    if not self.alreadyPressed:
                        self.buttonSurface.fill(self.fillColors['pressed'])
                        self.onclickFunction()
                        self.alreadyPressed = True
                else:
                    #Le bouton n'est pas pressé
                    self.alreadyPressed = False
            
            #Centrer le texte et le faire afficher
            self.buttonSurface.blit(self.buttonSurf, [self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
                                                    self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2])
            #Afficher le bouton
            main_window.blit(self.buttonSurface, self.buttonRect)

#Fonction pour afficher ou non les paramètres
def parameter_display():
    global show_parameters
    show_parameters = not show_parameters   

"""
BUG : 
-  Un bouton en trop

TODO :
- Fenêtre de jeu game over
- Fenêtre paramètres de jeu : arrêt et replay 
- Bordure à droite avec bouton paramètres 
- Paramètres à gauche avec paramètres de vitesse
- Bordure grille de jeu
"""

#Les boutons
parametres = Button(0, 0, 0, 0, colors[0][6], brighter_colors[0][4], colors[0][3], colors[0][0], "Paramètres", parameter_display, True)
start_button = Button(0, 0, 0, 0, colors[0][6], brighter_colors[0][4], colors[0][3], colors[0][3], "Start", parameter_display, True)

#Boucle principale
while game_on:
    #Variable qui contient les touches pressées
    keys = pygame.key.get_pressed()

    #Redéfinir la police
    police = pygame.font.Font("MarkaziText-Bold.ttf", 2*pixel)

    #Limiter les fps à 60
    clock.tick(60)

    #Tout ce qui a un rapport avec l'affichage
    main_window.fill(colors[0][1])
    width, height = pygame.display.get_surface().get_size()
    pixel = update_window(width, height)

    #Redéfinir les caractéristiques des boutons
    parametres.x = width / 2 + 7 * pixel
    parametres.y = height / 2 + 6 * pixel
    parametres.width = 6 * pixel
    parametres.height = 3 * pixel
    parametres.buttonRect = pygame.Rect(parametres.x, parametres.y, parametres.width, parametres.height)
    parametres.buttonSurface = pygame.Surface((parametres.width, parametres.height))
    police = pygame.font.Font("MarkaziText-Bold.ttf", pixel)
    parametres.buttonSurf = police.render("Paramètres", True, colors[0][6])
    police = pygame.font.Font("MarkaziText-Bold.ttf", 2*pixel)

    #S'occuper des boutons
    for object in buttons:
        object.process_button()

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
        if score_bundle[1] >= 2:
            score_bundle[0] += 1
            score_bundle[1] = 0
            vitesse -= vitesse*10/100
            current_theme = current_theme + 1 if current_theme < 5 else 1
            pygame.mixer.music.load(playlist[current_theme])
            pygame.mixer.music.play(fade_ms=1000)
        
        #High_score
        if score_bundle[2] > score_bundle[3]:
            score_bundle[3] = score_bundle[2]
            score_bundle[5] = score_bundle[4]
        
        pygame.mixer.music.unpause()
    
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
        
        #Fonction de reset de la grille
        if keys[pygame.K_r]:
            grille, bloc_bundle, running, score_bundle, vitesse = reset(score_bundle)
        
        pygame.mixer.music.pause()
    
    #Tout le temps actif
    #Remplissage des couleurs dans la grille
    #Variable pour centrer la grille
    top_left_corner = [width/2 - 5*pixel, height/2 - 11*pixel]
    if list(main_window.get_size())[0] == good_screen_resolution[0] and list(main_window.get_size())[1] == good_screen_resolution[1]:
        pygame.draw.rect(main_window, colors[0][0], pygame.Rect(top_left_corner[0] - int(1/2*pixel), top_left_corner[1] - int(1/2*pixel), 11*pixel, 23*pixel), int(1/2*pixel))
    for y in range(len(grille)):
        for x in range(len(grille[y])):
            pygame.draw.rect(main_window, colors[0][0], pygame.Rect(x*pixel + top_left_corner[0], y*pixel + top_left_corner[1], pixel, pixel), 1)
            if grille[y][x] != 0:
                pygame.draw.rect(main_window, colors[current_theme][grille[y][x]-2], pygame.Rect(x*pixel + top_left_corner[0]+1, y*pixel + top_left_corner[1]+1, pixel-2, pixel-2))
                pygame.draw.rect(main_window, brighter_colors[current_theme][grille[y][x]-2], pygame.Rect(x*pixel + top_left_corner[0] + int(1/4*pixel), y*pixel + top_left_corner[1] + int(1/4*pixel), int(1/4*pixel), int(1/4*pixel)))
    #Dessiner la pièce qui bouge
    for y in range(len(bloc_bundle[0])):
        for x in range(len(bloc_bundle[0][y])):
            if bloc_bundle[0][y][x] != 0:
                pygame.draw.rect(main_window, colors[current_theme][bloc_bundle[0][y][x]-2], pygame.Rect(x*pixel + top_left_corner[0]+1 + pixel*bloc_bundle[1][1], y*pixel + top_left_corner[1]+1 + pixel*bloc_bundle[1][0], pixel-2, pixel-2))
                pygame.draw.rect(main_window, brighter_colors[current_theme][bloc_bundle[0][y][x]-2], pygame.Rect(x*pixel + top_left_corner[0] + int(1/4*pixel) + pixel*bloc_bundle[1][1], y*pixel + top_left_corner[1] + int(1/4*pixel) + pixel*bloc_bundle[1][0], int(1/4*pixel), int(1/4*pixel)))
    #Dessiner la pièce qui va venir
    for y in range(len(blocs[bloc_bundle[4][1][bloc_bundle[4][0]]])):
        for x in range(len(blocs[bloc_bundle[4][1][bloc_bundle[4][0]]][y])):
            if blocs[bloc_bundle[4][1][bloc_bundle[4][0]]][y][x] != 0:
                pygame.draw.rect(main_window, colors[0][0], pygame.Rect((x+7)*pixel + width/2, (y-8)*pixel + height/2, pixel, pixel), 2)
                pygame.draw.rect(main_window, colors[current_theme][blocs[bloc_bundle[4][1][bloc_bundle[4][0]]][y][x]-2], pygame.Rect((x+7)*pixel + width/2 + 1, (y-8)*pixel + height/2 + 1, pixel-2, pixel-2))
                pygame.draw.rect(main_window, brighter_colors[current_theme][blocs[bloc_bundle[4][1][bloc_bundle[4][0]]][y][x]-2], pygame.Rect((x+7)*pixel + width/2 + int(1/4*pixel), (y-8)*pixel + height/2 + int(1/4*pixel), int(1/4*pixel), int(1/4*pixel)))

    #Afficher le titre au dessus    
    game_title =  police.render("TÉTRIS", True, colors[0][6])
    game_titleRect = game_title.get_rect()
    game_titleRect.center = (width/2, height/2 - 13*pixel)
    main_window.blit(game_title, game_titleRect)

    #Afficher le score
    score_display =  police.render(str(score_bundle[2]), True, score_bundle[4])
    score_displayRect = score_display.get_rect()
    score_displayRect.topleft = (width/2 + 7*pixel, height/2 - 11*pixel)
    main_window.blit(police.render("Score : ", True, colors[0][0]), score_displayRect)
    score_displayRect.topleft = (width/2 + 7*pixel + police.render("Score : ", True, colors[0][0]).get_rect().width, height/2 - 11*pixel)
    main_window.blit(score_display, score_displayRect)

    #Afficher le high_score
    high_score_display =  police.render(str(score_bundle[3]), True, score_bundle[5])
    high_score_displayRect = high_score_display.get_rect()
    high_score_displayRect.topleft = (width/2 + 7*pixel, height/2 - 5*pixel)
    main_window.blit(police.render("Highscore : ", True, colors[0][0]), high_score_displayRect)
    high_score_displayRect.topleft = (width/2 + 7*pixel + police.render("Highscore : ", True, colors[0][0]).get_rect().width, height/2 - 5*pixel)
    main_window.blit(high_score_display, high_score_displayRect)

    if show_parameters:
        #Dessiner les paramètres
        pygame.draw.rect(main_window, darker_colors[0][3], pygame.Rect(top_left_corner[0] - 13*pixel - int(1/2*pixel), top_left_corner[1] - int(1/2*pixel), 11*pixel, 23*pixel))
    
    #Actualiser l'écran
    pygame.display.flip()

#Quitter le programme
pygame.quit()