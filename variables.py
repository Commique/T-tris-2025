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
    (0, 0, 0),          #0
    (255, 255, 255),    #1
    (255, 0, 0),        #2
    (0, 255, 0),        #3
    (0, 0, 255),        #4
    (255, 255, 0),      #5
    (255, 0, 255),      #6
    (0, 255, 255),      #7
    (255, 165, 0),      #8
    (170, 0, 255)       #9
]

#Tous les blocs possibles
blocs = [
    [[7, 7, 7, 7]],     #I
    [[5, 5],            #O
     [5, 5]],
    [[9, 9, 9],         #T
     [0, 9, 0]],
    [[8, 8, 8],         #L
     [8, 0, 0]],
    [[4, 4, 4],         #J
     [0, 0, 4]],
    [[2, 2, 0],         #Z
     [0, 2, 2]],
    [[0, 3, 3],         #S
     [3, 3, 0]]
]

moving_bloc = last_moving_bloc = blocs[ri(0, 6)]
moving_bloc_position = last_moving_bloc_position = [0, 3]   #y, x
if moving_bloc == blocs[1]:
    moving_bloc_position = last_moving_bloc_position = [0, 4]    

#Grille
grille = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]