import pygame
from pygame.locals import *
from functions import *
from variables import *

pygame.init()
main_window = pygame.display.set_mode((10*pixel,22*pixel), RESIZABLE)
pygame.display.set_caption("Tétris")
pygame.display.set_icon(Tetris.jpg)
clock = pygame.time.Clock()

while running:
    #Tout ce qui a un rapport avec l'affichage
    main_window.fill(color[1])
    width, height = pygame.display.get_surface().get_size()
    pixel = update_window(width, height)

    #Variable qui contient les touches pressées
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        #Fonction de fermeture
        if event.type == pygame.QUIT:
            running = False
        
        #Debug
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_p:
                print("____________________________________________________")
                for i in grille:
                    print(i)
                print("____________________________________________________")

    if keys[pygame.K_w]:
        running = False

    #Grille et remplissage des couleurs
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
    

    #Si on veut modifier la taille de la fenêtre
    if keys[pygame.K_a] and not pixel >= 50:
        pixel += 1
    if keys[pygame.K_z] and not pixel <= 10:
        pixel -= 1

    pygame.display.flip()



pygame.quit()