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
        self.default_color = default_color
        self.hovered_color = hovered_color
        self.pressed_color = pressed_color

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
            'pressed': pressed_color
        }

    #Fonctionnement des boutons 
    def process_button(self):
        global mouse_click
        if self.rendering:
            mousePos = pygame.mouse.get_pos()
            #Etat par défaut
            self.buttonSurface.fill(self.fillColors['normal'])
            if self.buttonRect.collidepoint(mousePos):
                #La souris est sur le bouton
                self.buttonSurface.fill(self.fillColors['hover'])
                if pygame.mouse.get_pressed(num_buttons=3)[0] and not mouse_click and not self.alreadyPressed:
                    self.buttonSurface.fill(self.fillColors['pressed'])
                    self.onclickFunction()
                    self.alreadyPressed = True
                    mouse_click = True
                elif not pygame.mouse.get_pressed(num_buttons=3)[0]:
                    #Le bouton n'est pas pressé
                    self.alreadyPressed = False
                    mouse_click = False
            
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

def start_function(difficulty):
    global is_on_start, base_speed, scaling
    is_on_start = False

    #Définir des preset pour chaque difficulté
    if difficulty == "easy":
        base_speed = 500
        scaling = 10
    elif difficulty == "normal":
        base_speed = 350
        scaling = 15
    elif difficulty == "hard":
        base_speed = 200
        scaling = 20

def restart_function():
    global grille, bloc_bundle, running, score_bundle, vitesse, current_theme, is_game_over, base_speed
    is_game_over = False
    vitesse = base_speed
    grille, bloc_bundle, running, score_bundle, current_theme = reset(score_bundle)

def quit_function():
    global game_on
    game_on = False

def dark_function():
    global is_dark
    is_dark = not is_dark

"""
BUG :

TODO :
- Paramètres dans le rectangle à gauche avec bouton mute, et mode de jeu
"""

def start_game(restart=False):
    global is_on_start, game_on, current_theme

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
    police = pygame.font.Font("MarkaziText-Bold.ttf", 2*pixel)

    restart_button.rendering = False
    quit_button.rendering = False
    easy_button.rendering = True
    normal_button.rendering = True
    hard_button.rendering = True
    
    #Redéfinir les caractéristiques des boutons easy, normal et hard
    easy_button.x = width / 2 - 12 * pixel
    easy_button.y = height / 2 + 6 * pixel
    easy_button.width = 6 * pixel
    easy_button.height = 3 * pixel
    easy_button.buttonRect = pygame.Rect(easy_button.x, easy_button.y, easy_button.width, easy_button.height)
    easy_button.buttonSurface = pygame.Surface((easy_button.width, easy_button.height))
    easy_button.buttonSurf = police.render("Facile", True, colors[0][6])

    normal_button.x = width / 2 - 4 * pixel
    normal_button.y = height / 2 + 5.5 * pixel
    normal_button.width = 8 * pixel
    normal_button.height = 4 * pixel
    normal_button.buttonRect = pygame.Rect(normal_button.x, normal_button.y, normal_button.width, normal_button.height)
    normal_button.buttonSurface = pygame.Surface((normal_button.width, normal_button.height))
    normal_button.buttonSurf = police.render("Normal", True, colors[0][6])

    hard_button.x = width / 2 + 6 * pixel
    hard_button.y = height / 2 + 6 * pixel
    hard_button.width = 6 * pixel
    hard_button.height = 3 * pixel
    hard_button.buttonRect = pygame.Rect(hard_button.x, hard_button.y, hard_button.width, hard_button.height)
    hard_button.buttonSurface = pygame.Surface((hard_button.width, hard_button.height))
    hard_button.buttonSurf = police.render("Difficile", True, colors[0][6])

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
    
    if restart:
        restart_function()

def restart_game():
    global is_on_start
    is_on_start = True
    dark_button.rendering = False
    restart_button.rendering = False
    parametres.rendering = False
    pygame.mixer.music.load(musique_ambiance[0])
    pygame.mixer.music.play()
    while is_on_start:
        start_game(True)
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play()
    
    #Bouttons
    easy_button.rendering = False
    normal_button.rendering = False
    hard_button.rendering = False

    #La musique
    pygame.mixer.music.load(playlist[current_theme - 1])
    pygame.mixer.music.play()

#Les boutons
parametres = Button(0, 0, 0, 0, colors[0][4], brighter_colors[0][4], colors[0][3], colors[0][6], "Paramètres", parameter_display, False)
easy_button = Button(0, 0, 0, 0, colors[0][4], brighter_colors[0][4], colors[0][3], colors[0][6], "Facile", lambda:start_function("easy"), True)
normal_button = Button(0, 0, 0, 0, colors[0][4], brighter_colors[0][4], colors[0][3], colors[0][6], "Normal", lambda:start_function("normal"), True)
hard_button = Button(0, 0, 0, 0, colors[0][4], brighter_colors[0][4], colors[0][3], colors[0][6], "Difficile", lambda:start_function("hard"), True)
restart_button = Button(0, 0, 0, 0, colors[0][4], brighter_colors[0][4], colors[0][3], colors[0][6], "Restart", restart_game, False)
quit_button = Button(0, 0, 0, 0, colors[0][4], brighter_colors[0][4], colors[0][3], colors[0][6], "Quit", quit_function, False)
dark_button = Button(0, 0, 0, 0, brighter_colors[0][3], colors[0][3], darker_colors[0][3], colors[0][6], "Dark Mode", dark_function, False)

#Fenêtre de lancement
while is_on_start:
    start_game()
    vitesse = base_speed
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.play()

#Bouttons
easy_button.rendering = False
normal_button.rendering = False
hard_button.rendering = False

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
        
        #La musique ne doit pas être sur pause
        pygame.mixer.music.unpause()

        #La musique ne doit pas s'arrêter
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play()

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
        else:
            start_up_held_down = current_time
        if keys[pygame.K_RIGHT]:
            if current_time - time_right_held_down > 200:
                bloc_bundle[1] = check_collision(bloc_bundle, grille, direction[2])
                time_right_held_down = current_time
        else: 
            start_right_held_down = current_time
        if keys[pygame.K_LEFT]:
            if current_time - time_left_held_down > 200:
                bloc_bundle[1] = check_collision(bloc_bundle, grille, direction[3])
                time_left_held_down = current_time
        else:
            start_left_held_down = current_time

        #Game over
        if grille[0] != [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] and bloc_bundle[1][0] != 0:
            is_game_over = True

        #Changement level
        if score_bundle[1] >= number_of_lines_to_be_cleared:
            score_bundle[0] += 1
            score_bundle[1] -= number_of_lines_to_be_cleared
            vitesse -= vitesse*scaling/100
            current_theme = current_theme + 1 if current_theme < 5 else 1
            pygame.mixer.music.load(playlist[current_theme - 1])
            pygame.mixer.music.play(fade_ms=1000)
        
        #High_score
        if score_bundle[2] > score_bundle[3]:
            score_bundle[3] = score_bundle[2]
            score_bundle[5] = score_bundle[4]
    
    #Pause ou game over
    if not running:
        #La musique doit être sur pause
        pygame.mixer.music.pause()
        
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
                    restart_game()

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
            vitesse = base_speed
            grille, bloc_bundle, running, score_bundle, current_theme = reset(score_bundle)
            pygame.mixer.music.load(playlist[current_theme - 1])
            pygame.mixer.music.play()

    #Écran de game over
    if is_game_over:
        parametres.rendering = False
        dark_button.rendering = False

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
        restart_button.fillColors = {
            'normal': colors[0][4],
            'hover': brighter_colors[0][4],
            'pressed': colors[0][3]
            }
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
                if not is_dark and grille[y][x] == 0:
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

        #Afficher les bons boutons
        quit_button.rendering = False

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

        #Afficher le level
        level_display =  police.render(str(score_bundle[0]), True, colors[0][0])
        level_displayRect = level_display.get_rect()
        level_displayRect.topleft = (width/2 + 8*pixel, height/2 - 1*pixel)
        main_window.blit(police.render("Level : ", True, colors[0][0]), level_displayRect)
        level_displayRect.topleft = (width/2 + 8*pixel + police.render("Level : ", True, colors[0][0]).get_rect().width, height/2 - 1*pixel)
        main_window.blit(level_display, level_displayRect)

        if show_parameters:
            #Dessiner les paramètres
            pygame.draw.rect(main_window, brighter_colors[0][3], pygame.Rect(top_left_corner[0] - 13*pixel - int(1/2*pixel), top_left_corner[1] - int(1/2*pixel), 11*pixel, 23*pixel))

            #Contrôles
            police = pygame.font.Font("MarkaziText-Bold.ttf", pixel)
            main_window.blit(police.render("Contrôles :", True, colors[0][0]), (top_left_corner[0] - 13*pixel, top_left_corner[1]))
            main_window.blit(police.render("Flèche du haut : Rotation", True, colors[0][0]), (top_left_corner[0] - 13*pixel, top_left_corner[1] + pixel))
            main_window.blit(police.render("Flèche de gauche : Gauche", True, colors[0][0]), (top_left_corner[0] - 13*pixel, top_left_corner[1] + 2*pixel))
            main_window.blit(police.render("Flèche de droite : Droite", True, colors[0][0]), (top_left_corner[0] - 13*pixel, top_left_corner[1] + 3*pixel))
            main_window.blit(police.render("Flèche du bas : Bas", True, colors[0][0]), (top_left_corner[0] - 13*pixel, top_left_corner[1] + 4*pixel))
            main_window.blit(police.render("Espace : Pause", True, colors[0][0]), (top_left_corner[0] - 13*pixel, top_left_corner[1] + 5*pixel))
            main_window.blit(police.render("Entrée : Bas instantané", True, colors[0][0]), (top_left_corner[0] - 13*pixel, top_left_corner[1] + 6*pixel))

            police = pygame.font.Font("MarkaziText-Bold.ttf", 2*pixel)

            #Dark mode
            dark_button.x = top_left_corner[0] - 11*pixel
            dark_button.y = top_left_corner[1] + 8*pixel
            dark_button.width = 6 * pixel
            dark_button.height = 3 * pixel
            dark_button.buttonRect = pygame.Rect(dark_button.x, dark_button.y, dark_button.width, dark_button.height)
            dark_button.buttonSurface = pygame.Surface((dark_button.width, dark_button.height))
            dark_button.buttonSurf = police.render("Dark Mode", True, colors[0][6])
            dark_button.rendering = True

            #Restart
            restart_button.x = top_left_corner[0] - 11*pixel
            restart_button.y = top_left_corner[1] + 12*pixel
            restart_button.width = 6 * pixel
            restart_button.height = 3 * pixel
            restart_button.buttonRect = pygame.Rect(restart_button.x, restart_button.y, restart_button.width, restart_button.height)
            restart_button.buttonSurface = pygame.Surface((restart_button.width, restart_button.height))
            restart_button.buttonSurf = police.render("Restart", True, colors[0][6])
            restart_button.fillColors = {
                'normal': brighter_colors[0][3],
                'hover': colors[0][3],
                'pressed': darker_colors[0][3]
                }
            restart_button.rendering = True
        
        else:
            dark_button.rendering = False
            restart_button.rendering = False

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