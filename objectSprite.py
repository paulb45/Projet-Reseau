import pygame
from config import *

class SpritesGestion():
    def __init__(self):
        self.sprite_path = "graphic/sprites/"
        self.tile_size = 16
        self.y_offset = 1
        self.load_sprites()

    def load_sprites(self):
        self.tileset = pygame.image.load(f"{self.sprite_path}Tileset.png").convert_alpha()
        self.grass_tile = pygame.transform.scale_by(self.tileset.subsurface([0, self.y_offset, self.tile_size, self.tile_size + self.y_offset]), 10)

if __name__ == '__main__':
    print()