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
buttons = []
pygame.mixer.init()
pygame.mixer.music.load(musique_ambiance[0])
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
        self.button_text = button_text

        #Définir les propriétés du bouton
        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.buttonRect.topleft = (self.x, self.y)
        self.buttonSurf = police.render(self.button_text, True, self.text_color)

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
            
            #Redéfinir la couleur du texte
            police = pygame.font.Font("MarkaziText-Bold.ttf", pixel)
            self.buttonSurf = police.render(self.button_text, True, self.text_color)
            
            #Centrer le texte et le faire afficher
            self.buttonSurface.blit(self.buttonSurf, [self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
                                                    self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2])
            #Afficher le bouton
            main_window.blit(self.buttonSurface, self.buttonRect)

#Fonctions des boutons
def parameter_display():
    global show_parameters
    show_parameters = not show_parameters

def start_function():
    global is_on_start
    is_on_start = False

def restart_function():
    global is_game_over
    is_game_over = False
    global grille, bloc_bundle, running, score_bundle, vitesse
    grille, bloc_bundle, running, score_bundle, vitesse, current_theme = reset(score_bundle)

def quit_function():
    global game_on
    game_on = False

"""
BUG : 

TODO :
- Paramètres dans le rectangle à gauche avec paramètres de vitesse et reset + tout le blablabla
"""

#Les boutons
parametres = Button(0, 0, 0, 0, colors[0][4], brighter_colors[0][4], colors[0][3], colors[0][6], "Paramètres", parameter_display, False)
start_button = Button(0, 0, 0, 0, colors[0][4], brighter_colors[0][4], colors[0][3], colors[0][6], "Start", start_function, True)
restart_button = Button(0, 0, 0, 0, colors[0][4], brighter_colors[0][4], colors[0][3], colors[0][6], "Restart", restart_function, False)
quit_button = Button(0, 0, 0, 0, colors[0][4], brighter_colors[0][4], colors[0][3], colors[0][6], "Quit", quit_function, False)

#Fenêtre de lancement
while is_on_start:
    #Variable qui contient les touches pressées
    keys = pygame.key.get_pressed()

    #Limiter les fps à 60
    clock.tick(60)

    #Tous les événements
    for event in pygame.event.get():
        #Fonction de fermeture
        if event.type == pygame.QUIT:
            is_on_start = False
            game_on = False

    #Démarage rapide du jeu
    if keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:
        is_on_start = False

    #Tout ce qui a un rapport avec l'affichage
    main_window.fill(colors[0][1])
    width, height = pygame.display.get_surface().get_size()
    pixel = update_window(width, height)

    #Redéfinir les caractéristiques des boutons
    start_button.x = width / 2 - 3 * pixel
    start_button.y = height / 2 + 6 * pixel
    start_button.width = 6 * pixel
    start_button.height = 3 * pixel
    start_button.buttonRect = pygame.Rect(start_button.x, start_button.y, start_button.width, start_button.height)
    start_button.buttonSurface = pygame.Surface((start_button.width, start_button.height))
    police = pygame.font.Font("MarkaziText-Bold.ttf", pixel)
    start_button.buttonSurf = police.render("Start", True, colors[0][6])

    #S'occuper des boutons
    for object in buttons:
        object.process_button()
    
    #Redéfinir la police
    police = pygame.font.Font("MarkaziText-Bold.ttf", 10*pixel)

    #Afficher le titre au dessus    
    game_title = police.render("TÉTRIS", True, colors[0][6])
    game_titleRect = game_title.get_rect()
    game_titleRect.center = (width/2, height/2)
    main_window.blit(game_title, game_titleRect)

    #Actualiser l'écran
    pygame.display.flip()

#Boutton start
start_button.rendering = False

#Redéfinir la police
police = pygame.font.Font("MarkaziText-Bold.ttf", 2*pixel)

#La musique
pygame.mixer.music.load(playlist[current_theme - 1])
pygame.mixer.music.play()

#Boucle principale
while game_on:
    #Variable qui contient les touches pressées 
    keys = pygame.key.get_pressed()

    #Limiter les fps à 60
    clock.tick(60)

    #Tout ce qui a un rapport avec l'affichage
    main_window.fill(colors[0][1])
    width, height = pygame.display.get_surface().get_size()
    pixel = update_window(width, height)

    if is_game_over:
        running = False

    #Boucle du jeu
    if running:
        #La pièce qui tombe toutes les vitesse/1000 seconde
        if pygame.time.get_ticks() >= last_update:
            bloc_bundle, grille, is_game_over, score_bundle = check_down_collision(bloc_bundle, grille, score_bundle)
            last_update = pygame.time.get_ticks() + vitesse
        
        #Tous les événements
        for event in pygame.event.get():
            #Fonction de fermeture
            if event.type == pygame.QUIT:
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
                if event.key == pygame.K_UP:
                    start_up_held_down = pygame.time.get_ticks()
                    time_up_held_down = pygame.time.get_ticks()
                    bloc_bundle = check_up_collision(bloc_bundle, grille)
                if event.key == pygame.K_RIGHT:
                    start_right_held_down = pygame.time.get_ticks()
                    time_right_held_down = pygame.time.get_ticks()
                    bloc_bundle[1] = check_collision(bloc_bundle, grille, direction[2])
                if event.key == pygame.K_LEFT:
                    start_left_held_down = pygame.time.get_ticks()
                    time_left_held_down = pygame.time.get_ticks()
                    bloc_bundle[1] = check_collision(bloc_bundle, grille, direction[3])
                if event.key == pygame.K_RETURN:
                    count = bloc_bundle[4][0]
                    while bloc_bundle[4][0] == count:
                        bloc_bundle, grille, is_game_over, score_bundle = check_down_collision(bloc_bundle, grille, score_bundle)

        #Aller vite
        current_time = pygame.time.get_ticks()
        if keys[pygame.K_DOWN]:
            bloc_bundle, grille, is_game_over, score_bundle = check_down_collision(bloc_bundle, grille, score_bundle)
        if keys[pygame.K_UP]:
            if current_time - time_up_held_down > 200:
                bloc_bundle = check_up_collision(bloc_bundle, grille)
                time_up_held_down = current_time
            if current_time - start_up_held_down > 400:
                bloc_bundle = check_up_collision(bloc_bundle, grille)
        else:
            start_up_held_down = current_time
        if keys[pygame.K_RIGHT]:
            if current_time - time_right_held_down > 200:
                bloc_bundle[1] = check_collision(bloc_bundle, grille, direction[2])
                time_right_held_down = current_time
            if current_time - start_right_held_down > 400:
                bloc_bundle[1] = check_collision(bloc_bundle, grille, direction[2])
        else: 
            start_right_held_down = current_time
        if keys[pygame.K_LEFT]:
            if current_time - time_left_held_down > 200:
                bloc_bundle[1] = check_collision(bloc_bundle, grille, direction[3])
                time_left_held_down = current_time
            if current_time - start_left_held_down > 400:
                bloc_bundle[1] = check_collision(bloc_bundle, grille, direction[3])
        else:
            start_left_held_down = current_time

        #Game over
        if grille[0] != [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] and bloc_bundle[1][0] != 0:
            is_game_over = True

        #Changement level
        if score_bundle[1] >= 10:
            score_bundle[0] += 1
            score_bundle[1] -= 10
            vitesse -= vitesse*10/100
            current_theme = current_theme + 1 if current_theme < 5 else 1
            pygame.mixer.music.load(playlist[current_theme - 1])
            pygame.mixer.music.play(fade_ms=1000)
        
        #High_score
        if score_bundle[2] > score_bundle[3]:
            score_bundle[3] = score_bundle[2]
            score_bundle[5] = score_bundle[4]
    
    #Pause ou game over
    if not running:
        #Tous les évènements 
        for event in pygame.event.get():
            #Fonction de fermeture
            if event.type == pygame.QUIT:
                game_on = False
            
            #Pause rapide du jeu
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if not is_game_over:
                    running = not running
                if is_game_over:
                    is_game_over = False
                    grille, bloc_bundle, running, score_bundle, vitesse, current_theme = reset(score_bundle)

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
            grille, bloc_bundle, running, score_bundle, vitesse, current_theme = reset(score_bundle)

    #Écran de game over
    if is_game_over:
        parametres.rendering = False

        #Mettre les boutons restart et quit
        #Restart
        restart_button.x = width / 2 - 8 * pixel
        restart_button.y = height / 2 + 6 * pixel
        restart_button.width = 6 * pixel
        restart_button.height = 3 * pixel
        restart_button.buttonRect = pygame.Rect(restart_button.x, restart_button.y, restart_button.width, restart_button.height)
        restart_button.buttonSurface = pygame.Surface((restart_button.width, restart_button.height))
        police = pygame.font.Font("MarkaziText-Bold.ttf", pixel)
        restart_button.buttonSurf = police.render("Restart", True, colors[0][6])
        restart_button.rendering = True

        #Quit
        quit_button.x = width / 2 + 2 * pixel
        quit_button.y = height / 2 + 6 * pixel
        quit_button.width = 6 * pixel
        quit_button.height = 3 * pixel
        quit_button.buttonRect = pygame.Rect(quit_button.x, quit_button.y, quit_button.width, quit_button.height)
        quit_button.buttonSurface = pygame.Surface((quit_button.width, quit_button.height))
        police = pygame.font.Font("MarkaziText-Bold.ttf", pixel)
        quit_button.buttonSurf = police.render("Quit", True, colors[0][6])
        quit_button.rendering = True

        #Redéfinir la police
        police = pygame.font.Font("MarkaziText-Bold.ttf", 7*pixel)

        #Afficher Game Over au dessus    
        game_title = police.render("GAME OVER", True, colors[0][6])
        game_titleRect = game_title.get_rect()
        game_titleRect.center = (width/2, height/2 - 6*pixel)
        main_window.blit(game_title, game_titleRect)

        police = pygame.font.Font("MarkaziText-Bold.ttf", 5*pixel)

        #Afficher le score
        score_display =  police.render(str(score_bundle[2]), True, score_bundle[4])
        score_displayRect = score_display.get_rect()
        score_displayRect.topleft = (width/2 - 10*pixel, height/2 - 5*pixel)
        main_window.blit(police.render("Score : ", True, colors[0][0]), score_displayRect)
        score_displayRect.topleft = (width/2 - 10*pixel + police.render("Score : ", True, colors[0][0]).get_rect().width, height/2 - 5*pixel)
        main_window.blit(score_display, score_displayRect)
        

        #Afficher le high_score
        high_score_display =  police.render(str(score_bundle[3]), True, score_bundle[5])
        high_score_displayRect = high_score_display.get_rect()
        high_score_displayRect.topleft = (width/2 - 10*pixel, height/2 - 1*pixel)
        main_window.blit(police.render("Highscore : ", True, colors[0][0]), high_score_displayRect)
        high_score_displayRect.topleft = (width/2 - 10*pixel + police.render("Highscore : ", True, colors[0][0]).get_rect().width, height/2 - 1*pixel)
        main_window.blit(high_score_display, high_score_displayRect)

    if not is_game_over:
        restart_button.rendering = False
        quit_button.rendering = False
        parametres.rendering = True

    #Tout le temps actif si pas game over
    #Remplissage des couleurs dans la grille
    #Variable pour centrer la grille
    if not is_game_over:
        top_left_corner = [width/2 - 5*pixel, height/2 - 11*pixel]
        pygame.draw.rect(main_window, colors[0][0], pygame.Rect(top_left_corner[0] - int(1/2*pixel), top_left_corner[1] - int(1/2*pixel), 11*pixel, 23*pixel))
        for y in range(len(grille)):
            for x in range(len(grille[y])):
                pygame.draw.rect(main_window, colors[0][0], pygame.Rect(x*pixel + top_left_corner[0], y*pixel + top_left_corner[1], pixel, pixel), 1)
                if grille[y][x] != 0:
                    pygame.draw.rect(main_window, colors[current_theme][grille[y][x]-2], pygame.Rect(x*pixel + top_left_corner[0]+1, y*pixel + top_left_corner[1]+1, pixel-2, pixel-2))
                    pygame.draw.rect(main_window, brighter_colors[current_theme][grille[y][x]-2], pygame.Rect(x*pixel + top_left_corner[0] + int(1/4*pixel), y*pixel + top_left_corner[1] + int(1/4*pixel), int(1/4*pixel), int(1/4*pixel)))
                else:
                    pygame.draw.rect(main_window, colors[0][1], pygame.Rect(x*pixel + top_left_corner[0]+1, y*pixel + top_left_corner[1]+1, pixel-2, pixel-2))
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
                    pygame.draw.rect(main_window, colors[0][0], pygame.Rect((x+8)*pixel + width/2, (y-8)*pixel + height/2, pixel, pixel), 2)
                    pygame.draw.rect(main_window, colors[current_theme][blocs[bloc_bundle[4][1][bloc_bundle[4][0]]][y][x]-2], pygame.Rect((x+8)*pixel + width/2 + 1, (y-8)*pixel + height/2 + 1, pixel-2, pixel-2))
                    pygame.draw.rect(main_window, brighter_colors[current_theme][blocs[bloc_bundle[4][1][bloc_bundle[4][0]]][y][x]-2], pygame.Rect((x+8)*pixel + width/2 + int(1/4*pixel), (y-8)*pixel + height/2 + int(1/4*pixel), int(1/4*pixel), int(1/4*pixel)))

        #Afficher le score
        score_display =  police.render(str(score_bundle[2]), True, score_bundle[4])
        score_displayRect = score_display.get_rect()
        score_displayRect.topleft = (width/2 + 8*pixel, height/2 - 11*pixel)
        main_window.blit(police.render("Score : ", True, colors[0][0]), score_displayRect)
        score_displayRect.topleft = (width/2 + 8*pixel + police.render("Score : ", True, colors[0][0]).get_rect().width, height/2 - 11*pixel)
        main_window.blit(score_display, score_displayRect)
    
        #Afficher le high_score
        high_score_display =  police.render(str(score_bundle[3]), True, score_bundle[5])
        high_score_displayRect = high_score_display.get_rect()
        high_score_displayRect.topleft = (width/2 + 8*pixel, height/2 - 5*pixel)
        main_window.blit(police.render("Highscore : ", True, colors[0][0]), high_score_displayRect)
        high_score_displayRect.topleft = (width/2 + 8*pixel + police.render("Highscore : ", True, colors[0][0]).get_rect().width, height/2 - 5*pixel)
        main_window.blit(high_score_display, high_score_displayRect)

        if show_parameters:
            #Dessiner les paramètres
            pygame.draw.rect(main_window, darker_colors[0][3], pygame.Rect(top_left_corner[0] - 13*pixel - int(1/2*pixel), top_left_corner[1] - int(1/2*pixel), 11*pixel, 23*pixel))
        
        #Redéfinir les caractéristiques du bouton parametres
        parametres.x = width / 2 + 8 * pixel
        parametres.y = height / 2 + 6 * pixel
        parametres.width = 6 * pixel
        parametres.height = 3 * pixel
        parametres.buttonRect = pygame.Rect(parametres.x, parametres.y, parametres.width, parametres.height)
        parametres.buttonSurface = pygame.Surface((parametres.width, parametres.height))
        police = pygame.font.Font("MarkaziText-Bold.ttf", pixel)
        parametres.buttonSurf = police.render("Paramètres", True, colors[0][6])
        police = pygame.font.Font("MarkaziText-Bold.ttf", 2*pixel)
        parametres.rendering = True

    #Afficher le titre au dessus
    if not is_game_over:
        police = pygame.font.Font("MarkaziText-Bold.ttf", 2*pixel)
        game_title =  police.render("TÉTRIS", True, colors[0][6])
        game_titleRect = game_title.get_rect()
        game_titleRect.center = (width/2, height/2 - 13*pixel)
        main_window.blit(game_title, game_titleRect)
    else:
        police = pygame.font.Font("MarkaziText-Bold.ttf", 5*pixel)
        game_title =  police.render("TÉTRIS", True, colors[0][6])
        game_titleRect = game_title.get_rect()
        game_titleRect.center = (width/2, height/2 - 11*pixel)
        main_window.blit(game_title, game_titleRect)

    #S'occuper des boutons
    for object in buttons:
        object.process_button()

    #Actualiser l'écran
    pygame.display.flip()

#Quitter le programme
pygame.quit()