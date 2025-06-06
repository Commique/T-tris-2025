from pygame import *
from pygame.locals import *
from random import shuffle as sh

#Toutes nos variables
running = True
game_on = True
is_on_start = True
is_game_over = False
last_update = 0
good_screen_resolution = [1366, 745]
show_parameters = True
current_theme = 1
number_of_lines_to_be_cleared = 10
scaling = 15
is_dark = False
mouse_click = False

start_up_held_down = 0
start_left_held_down = 0
start_right_held_down = 0
time_up_held_down = 0
time_left_held_down = 0
time_right_held_down = 0

#Le standard du jeu pour plus de facilité
pixel = 30

#Vitesse (en milisecondes)
base_speed = 350
vitesse = base_speed

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
    [(0, 0, 0),         #Black
    (255, 255, 255),    #White
    (142, 202, 230),    #Light Blue
    (33, 150, 243),     #Blue
    (255, 183, 3),      #Yellow
    (251, 133, 0),      #Orange
    (2, 48, 71),        #Dark Blue
    (199, 172, 146),    #Khaki
    (148, 168, 154),    #Campbrige Blue
    (156, 179, 128),    #Olivine
    (212, 224, 155),    #Vanilla
    (164, 74, 63),      #Chestnut
    (0,25,40)],         #Dark Blue
    #Thème 1
    [(255, 0, 0),       #Red
    (0, 255, 0),        #Green
    (0, 0, 255),        #Blue
    (255, 255, 0),      #Yellow
    (0, 255, 255),      #Cyan
    (255, 165, 0),      #Orange
    (255, 0, 255)],     #Magenta
    #Thème 2
    [(128, 0, 128),     #Purple
    (255, 105, 180),    #Hot Pink
    (128, 128, 0),      #Olive
    (0, 128, 128),      #Teal
    (60, 179, 113),     #Medium Sea Green
    (123, 104, 238),    #Medium Slate Blue
    (255, 99, 71)],     #Tomato
    #Thème 3
    [(75, 0, 130),      #Indigo
    (120, 115, 70),     #Khaki
    (0, 0, 139),        #Dark Blue
    (0, 100, 0),        #Dark Green
    (255, 20, 147),     #Deep Pink
    (233, 150, 122),    #Dark Salmon
    (218, 112, 214)],   #Orchid
    #Thème 4
    [(255, 215, 0),     #Gold
    (0, 191, 255),      #Deep Sky Blue
    (255, 69, 0),       #Orange Red
    (70, 130, 180),     #Steel Blue
    (32, 178, 170),     #Light Sea Green
    (147, 112, 219),    #Medium Purple
    (170, 0, 255)],     #Purple
    #Thème 5
    [(139, 0, 0),       #Dark Red
    (0, 100, 0),        #Dark Green
    (0, 0, 139),        #Dark Blue
    (184, 134, 11),     #Dark Goldenrod
    (0, 139, 139),      #Dark Cyan
    (255, 140, 0),      #Dark Orange
    (139, 0, 139)]      #Dark Magenta
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
playlist = ["Musics/music_1.mp3",
            "Musics/music_2.mp3",
            "Musics/music_3.mp3",
            "Musics/music_4.mp3",
            "Musics/music_5.mp3"]

musique_ambiance = ["Musics/music_menu.mp3"]

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
sh(bloc_list)
counting_list = [0, bloc_list]
moving_bloc = blocs[counting_list[1][counting_list[0]]]
counting_list[0] += 1
moving_bloc_position = [0, 3]   #y, x
if moving_bloc == blocs[1]:
    moving_bloc_position = [0, 4]    

bloc_bundle = [moving_bloc, moving_bloc_position, counting_list]

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