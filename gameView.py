import pygame
from config import *
from isometric import Isometric
from objectSprite import SpritesGestion

class GameView():

    @staticmethod
    def place_tile(surface: pygame.Surface, tile: pygame.image, pos: tuple):
        pos_iso = Isometric.cart_to_iso(pos)
        surface.blit(tile, SpritesGestion.place_top_position(tile, pos_iso))

    @staticmethod
    def generate_ground(surface: pygame.Surface, tile: pygame.image):
        # Ne prend pas en compte ce qui ne doit pas être affiché
        for i in range(N):
            for j in range(M):
                GameView.place_tile(surface, tile, (i,j))
    

