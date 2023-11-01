import pygame
from config import *

class SpritesGestion():
    def __init__(self):
        self.images = {}
        
    def __init__(self):
        self.images = {}

    def load_image(self, image_path: str):
        try:
            image = pygame.image.load(f"{sprite_path}{image_path}").convert_alpha()
            self.images[image_path] = image
        except pygame.error as e:
            print(f"Impossible de charger l'image '{image_path}': {e}")
            return None

    def get_image(self, image_path: str) -> pygame.image:
        if image_path in self.images:
            return self.images[image_path]
        else:
            return self.load_image(image_path)
        
    def cut_in_image(self, image_path: str, pos: tuple) -> pygame.Surface:
        # Retourne l'image à la i ème ligne, j ème colonne  -> pos = (i, j)
        return self.images[image_path].subsurface(
                [
                    pos[0]*tile_size + tileset_x_offset, 
                    pos[1]*tile_size + tileset_y_offset, 
                    (pos[0]+1)*tile_size + tileset_x_offset,
                    (pos[1]+1)*tile_size + tileset_y_offset
                ]
            )
        
    


if __name__ == '__main__':
    pass