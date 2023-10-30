from collections import defaultdict
import pygame
from config import *
from isometric import Isometric

class GameView():
    @staticmethod
    def generate_ground(surface: pygame.Surface, tile: pygame.image):
        # Ne prend pas en compte ce qui ne doit pas être affiché
        for i in range(N):
            for j in range(M):
                surface.blit(tile, Isometric.cart_to_iso((i,j)))