import pygame
from pygame.locals import *

pygame.init()
pixel = 30
main_window = pygame.display.set_mode((10*pixel,22*pixel), RESIZABLE)
pygame.display.set_caption("Tétris")
clock = pygame.time.Clock()
running = True
color = [(0,0,0),
         (255,255,255),
         (255,0,0),
         (0,255,0),
         (0,0,255)]

while running:
    main_window.fill(color[1])

    width, height = pygame.display.get_surface().get_size()
    if height <= 2.2*width:
        pixel = height//22
    elif height > 2.2*width:
        pixel = width//10

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
    #grille = [[0]*10]*22
    grille = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 2, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 2, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 2, 0, 0, 0],
            [0, 0, 0, 0, 0, 3, 2, 0, 0, 0],
            [0, 0, 0, 0, 3, 3, 3, 0, 0, 0],
            [0, 0, 0, 0, 0, 4, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 4, 4, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 4, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 3, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 3, 0, 0, 0],
            [0, 2, 2, 2, 2, 0, 3, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 3, 0, 0, 0],
            [0, 0, 0, 0, 0, 2, 2, 0, 0, 0],
            [0, 0, 0, 0, 2, 2, 0, 0, 0, 0]]
    y = -1
    for i in grille:
        y += 1
        x = -1
        for u in i:
            x += 1
            pygame.draw.rect(main_window, color[0], pygame.Rect(x*pixel, y*pixel, pixel, pixel), 1)
            if u != 0:
                pygame.draw.rect(main_window, color[u], pygame.Rect(x*pixel+1, y*pixel+1, pixel-2, pixel-2))
    

    #Si on veut modifier la taille de la fenêtre
    if keys[pygame.K_a] and not pixel >= 50:
        pixel += 1
    if keys[pygame.K_z] and not pixel <= 10:
        pixel -= 1

    pygame.display.flip()


pygame.quit()