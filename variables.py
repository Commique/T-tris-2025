from pygame import *
from pygame.locals import *
from random import randint as ri

#Toutes nos variables
running = True

#Le standard du jeu pour plus de facilité
pixel = 30

#Vitesse (en milisecondes)
vitesse = 1000

#Toutes les directions possibles
direction = [
    "down",
    "up",
    "right",
    "left"
]

#Toutes les couleurs possibles
color = [
    (0,0,0),
    (255,255,255),
    (255,0,0),
    (0,255,0),
    (0,0,255)
]

#Tous les blocs possibles
blocs = [
    [[2, 2, 2, 2]],     #I
    [[2, 2],            #O
     [2, 2]],
    [[2, 2, 2],         #T
     [0, 2, 0]],
    [[2, 2, 2],         #L
     [2, 0, 0]],
    [[2, 2, 2],         #J
     [0, 0, 2]],
    [[2, 2, 0],         #Z
     [0, 2, 2]],
    [[0, 2, 2],         #S
     [2, 2, 0]]
]

moving_bloc_color = last_moving_bloc_color = color[ri(2,4)]
moving_bloc = last_moving_bloc = blocs[ri(0, 6)]
moving_bloc_position = last_moving_bloc_position = [0, 3]   #y, x
if moving_bloc == blocs[1]:
    moving_bloc_position = [0, 4]    

#Grille
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