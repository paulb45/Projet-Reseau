from collections import defaultdict
import numpy as np
N=100
M=100
map = defaultdict(lambda:0)

window_size = (1280, 720)
max_framerate = 60

# Variables pour les sprites
sprite_path = "sprites/"
tileset_x_offset, tileset_y_offset = 0, 1
tile_size = 16

# activation ou non du déplacement avec le curseur de la souris sur les bords de la fenètre
move_with_mouse = False

# taille sur les bords de l'écran pour le déplacement au curseur
size_move_border = 50

# Variables d'interface
screen_size = [ np.ceil(tile_size*(N+M)/2 / i) for i in range(1,3)]
interface_y_offset = 50 # Valeur de l'offset sur chaque côté
interface_x_offset = 2*interface_y_offset
screen_size[0] += interface_x_offset
screen_size[1] += interface_y_offset