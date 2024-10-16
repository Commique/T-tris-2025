from pygame import *
from pygame.locals import *

#Toutes nos variables
running = True
pixel = 30
color = [(0,0,0),
         (255,255,255),
         (255,0,0),
         (0,255,0),
         (0,0,255)]

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