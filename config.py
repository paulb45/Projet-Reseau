import numpy as np
from configparser import ConfigParser


N=100
M=100
ticks = 100
window_size = (1280, 720)
max_framerate = 60

# Initilisation de la logique
init_quantity_food = 200
init_energy_food = 100
nb_ticks_day = 2
pop_init = 100
mutation_rate = 0.1

#varaibles pour la musique
music_path ="music/"

assets_path = "assets/"

# Variables pour les sprites
sprite_path = "sprites/"
tileset_x_offset, tileset_y_offset = 0, 0
pos_x_tile, pos_y_tile = 2,2
tile_size = 32

# activation ou non du déplacement avec le curseur de la souris sur les bords de la fenètre
move_with_mouse = False

# zoom min et max cen nombre de cellule
zoom_min = 4
zoom_max = 40

# taille sur les bords de l'écran pour le déplacement au curseur
size_move_border = 50

# Variable avec une configuration dynamique
class Config():
    width_map=N
    height_map=M
    move_with_cursor=move_with_mouse
    quantity_food = init_quantity_food
    energy_food = init_energy_food
    nb_tick_day = nb_ticks_day
    P0 = pop_init
    bob_speed=1
    bob_mass=1
    bob_memory=0
    bob_perception=0

    # Variables d'interface
    screen_size = [ np.ceil(tile_size*(N+M)/2 / i) for i in range(1,3)]
    interface_y_offset = 50 # Valeur de l'offset sur chaque côté
    interface_x_offset = interface_y_offset
    screen_size[0] += 2*interface_x_offset
    screen_size[1] += 2*interface_y_offset
