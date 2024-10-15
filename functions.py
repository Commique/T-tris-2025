from pygame import *
from pygame.locals import *
from variables import *

#Toutes nos fonctions

def update_window(width, height):
    if height <= 2.2*width:
        pixel = height//22
    elif height > 2.2*width:
        pixel = width//10
    return pixel