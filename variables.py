from pygame import *
from pygame.locals import *
from random import shuffle as sh

#Toutes nos variables
game_on = True
last_update = 0
good_screen_resolution = [1366, 745]
show_parameters = True
current_theme = 1

#Le standard du jeu pour plus de facilité
pixel = 30

#Vitesse (en milisecondes)
vitesse = 300

#Level game Tetris
level_game = 0
total_cleared_lines = 0
score_total = 0
high_score = 0
score_color = (0,0,0)
high_score_color = score_color
score_bundle = [level_game, total_cleared_lines, score_total, high_score, score_color, high_score_color]

#Toutes les directions possibles
direction = [
    "down",
    "up",
    "right",
    "left"
]

#Toutes les couleurs possibles
colors = [
    [(0, 0, 0),         # Black
    (255, 255, 255),    # White
    (199, 172, 146),    # Khaki
    (148, 168, 154),    # Campbrige Blue
    (156, 179, 128),    # Olivine
    (212, 224, 155),    # Vanilla
    (164, 74, 63)],     # Chestnut
    # Thème 1
    [(255, 0, 0),       # Red
    (0, 255, 0),        # Green
    (0, 0, 255),        # Blue
    (255, 255, 0),      # Yellow
    (0, 255, 255),      # Cyan
    (255, 165, 0),      # Orange
    (255, 0, 255)],     # Magenta
    # Thème 2
    [(128, 0, 128),     # Purple
    (255, 105, 180),    # Hot Pink
    (128, 128, 0),      # Olive
    (0, 128, 128),      # Teal
    (60, 179, 113),     # Medium Sea Green
    (123, 104, 238),    # Medium Slate Blue
    (255, 99, 71)],     # Tomato
    # Thème 3
    [(75, 0, 130),      # Indigo
    (240, 230, 140),    # Khaki
    (0, 0, 139),        # Dark Blue
    (0, 100, 0),        # Dark Green
    (255, 20, 147),     # Deep Pink
    (233, 150, 122),    # Dark Salmon
    (218, 112, 214)],   # Orchid
    # Thème 4
    [(255, 215, 0),     # Gold
    (0, 191, 255),      # Deep Sky Blue
    (255, 69, 0),       # Orange Red
    (70, 130, 180),     # Steel Blue
    (32, 178, 170),     # Light Sea Green
    (147, 112, 219),    # Medium Purple
    (170, 0, 255)]      # Purple
]

#Fonction pour éclaircir une couleur
def lighten_color(color, factor=0.5):
    return tuple(min(255, int(c + (255 - c) * factor)) for c in color)

#Créer la liste des couleurs plus claires
brighter_colors = [[lighten_color(color) for color in theme] for theme in colors]

#Fonction pour assombrir une couleur
def darken_color(color, factor=0.5):
    return tuple(max(0, int(c * (1 - factor))) for c in color)

#Créer la liste des couleurs plus sombres
darker_colors = [[darken_color(color) for color in theme] for theme in colors]

#Playlist de musique
playlist=["music_tetris1.mp3"]


#Tous les blocs possibles
blocs = [
    [[6, 6, 6, 6]],     #I
    [[5, 5],            #O
     [5, 5]],
    [[8, 8, 8],         #T
     [0, 8, 0]],
    [[7, 7, 7],         #L
     [7, 0, 0]],
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
