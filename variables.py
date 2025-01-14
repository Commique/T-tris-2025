from pygame import *
from pygame.locals import *
from random import shuffle as sh

#Toutes nos variables
running = True
game_on = True
last_update=0

#Le standard du jeu pour plus de facilité
pixel = 30

#Vitesse (en milisecondes)
vitesse = 300

#Level game Tetris
level_game = 0
total_cleared_lines = 0
score_total = 0
score_bundle = [level_game, total_cleared_lines, score_total]

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

bloc_list = [0,1,2,3,4,5,6]
bloc_list_1 = bloc_list.copy()
bloc_list_2 = bloc_list.copy()
sh(bloc_list_1)
sh(bloc_list_2)
counting_list = [0, bloc_list_1, bloc_list_2]
moving_bloc = last_moving_bloc = blocs[counting_list[1][counting_list[0]]]
counting_list[0] += 1
moving_bloc_position = last_moving_bloc_position = [0, 3]   #y, x
if moving_bloc == blocs[1]:
    moving_bloc_position = last_moving_bloc_position = [0, 4]    

bloc_bundle = [moving_bloc, moving_bloc_position, last_moving_bloc, last_moving_bloc_position, counting_list]
#Il n'y a pas une redondance entre moving_block et last_moving_block

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
