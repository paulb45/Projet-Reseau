from collections import defaultdict
import pygame
from config import *
from isometric import Isometric

class GameView():

    @staticmethod
    def place_tile(surface: pygame.Surface, tile: pygame.image, pos: tuple):
        pos_iso = Isometric.cart_to_iso(pos)
        pos_iso[0] -= tile_size/2 # Applique un offset pour placer le bloc avec "l'origine du bloc" sur le coin supérieur
        surface.blit(tile, pos_iso)

    @staticmethod
    def generate_ground(surface: pygame.Surface, tile: pygame.image):
        # Ne prend pas en compte ce qui ne doit pas être affiché
        for i in range(N):
            for j in range(M):
                GameView.place_tile(surface, tile, (i,j))
    

