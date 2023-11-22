import pygame
from graphic.isometric import Isometric
from graphic.objectSprite import SpritesGestion

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import *

class GameView():

    @staticmethod
    def place_tile(surface: pygame.Surface, tile: pygame.image, pos: tuple):
        pos_iso = Isometric.cart_to_iso(pos)
        surface.blit(tile, SpritesGestion.place_top_position(Isometric.iso_to_print(pos_iso)))

    @staticmethod
    def generate_ground(surface: pygame.Surface, tile: pygame.image):
        # Ne prend pas en compte ce qui ne doit pas être affiché
        for i in range(N):
            for j in range(M):
                GameView.place_tile(surface, tile, (i,j))
    
    @staticmethod
    def place_entity(surface: pygame.Surface, sprite: pygame.sprite, pos: tuple):
        # Fonctionne pas encore
        pos_iso = Isometric.cart_to_iso(pos)
        foot_pos = SpritesGestion.place_bottom_position(sprite, pos_iso)
        surface.blit(sprite, Isometric.iso_to_print(foot_pos))

    @staticmethod
    def place_interface_in_middle(interface, window):
        window_center = (window_size[0] // 2, window_size[1] // 2)
        interface_center = (screen_size[0] //2, screen_size[1] // 2)
        offset_to_place = (window_center[0] - interface_center[0], window_center[1] - interface_center[1])
        window.blit(interface, offset_to_place)

    @staticmethod
    def move_sprite(sprite, old_map, new_map):
        # Chercher la position du bob sur l'old map
        # Chercher la position de ce même bob sur la new map
        # Calcul des coordonées en iso pour les deux
        # Calcul de l'écart
        # En déduire la vitesse sur x et sur y pour l'incrémenter
        # Faire le déplacement

        # Utiliser une fonction qui calcule les positions intermédiaires pour avoir toutes les entités qui se déplacent "en même temps"
        pass