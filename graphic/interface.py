import pygame
import graphic.objectSprite as objectSprite
import graphic.isometric as isometric

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import *

class Interface(pygame.Surface):
    """
        Interface est une surface contenant l'ensemble des éléments graphiques (l'ensemble des sprites) qui 
        concerne l'affichage du jeu.
        Elle est entièrement indépendante de la fenêtre !        
    """
    def __init__(self, size, flags=0):
        super().__init__(size, flags)
        self.load_images()

    def load_images(self):
        self.tileset = objectSprite.load_image('Tileset.png')
        self.grass_tile = objectSprite.cut_in_image('Tileset.png', (0,0))

        # Import et mise en dimension de Bob
        self.bob = objectSprite.load_image('crusader_idle_00000.png')
        self.bob = pygame.transform.scale(self.bob, (h:=tile_size, int(h * self.bob.get_height() / self.bob.get_width() )))

    def render_game(self):
        self.generate_ground(self.grass_tile)
        self.place_entity(self.bob, (80,0))
        
    def place_tile(self, tile: pygame.image, pos: tuple):
        pos_iso = isometric.cart_to_iso(pos)
        self.blit(tile, objectSprite.place_top_position(isometric.iso_to_print(pos_iso)))

    def generate_ground(self, tile: pygame.image):
        for i in range(N):
            for j in range(M):
                self.place_tile(tile, (i,j))

    def place_entity(self, sprite: pygame.sprite, pos: tuple):
        pos_iso = isometric.cart_to_iso(pos)
        foot_pos = objectSprite.place_bottom_position(sprite, pos_iso)
        self.blit(sprite, isometric.iso_to_print(foot_pos))


    def place_interface_in_middle(self, window):
        window_center = (window_size[0] // 2, window_size[1] // 2)
        interface_center = (screen_size[0] //2, screen_size[1] // 2)
        offset_to_place = (window_center[0] - interface_center[0], window_center[1] - interface_center[1])
        window.blit(self, offset_to_place)

    def move_sprite(self, sprite, old_map, new_map):
        # Chercher la position du bob sur l'old map
        # Chercher la position de ce même bob sur la new map
        # Calcul des coordonées en iso pour les deux
        # Calcul de l'écart
        # En déduire la vitesse sur x et sur y pour l'incrémenter
        # Faire le déplacement

        # Utiliser une fonction qui calcule les positions intermédiaires pour avoir toutes les entités qui se déplacent "en même temps"
        pass
