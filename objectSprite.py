import pygame
from config import *

class SpritesGestion():
    def __init__(self):
        self.sprite_path = "graphic/sprites/"
        self.y_offset = 1
        self.load_sprites()

    def load_sprites(self):
        self.tileset = pygame.image.load(f"{self.sprite_path}Tileset.png").convert_alpha()
        self.grass_tile = self.tileset.subsurface([0, self.y_offset, tile_size, tile_size + self.y_offset])


if __name__ == '__main__':
    pass