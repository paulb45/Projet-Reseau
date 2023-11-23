import pygame
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import *

    
_images = {}

@staticmethod
def place_top_position(pos: tuple) -> tuple:
    pos[0] -= tile_size/2
    return pos

@staticmethod
def place_bottom_position(image: pygame.image, pos: tuple) -> tuple:
    pos = place_top_position(pos)
    pos[1] += tile_size/4 - image.get_height()
    return pos

@staticmethod
def get_middle_of_tile(pos: tuple) -> tuple:
    # Retourne le milieu de la face supérieur, pas le milieu géométrique de l'image !
    pos += tile_size/2, tile_size/4
    return pos

@staticmethod
def load_image(image_path: str) -> pygame.image:
    if image_path in _images:
        return _images[image_path]
    try:
        image = pygame.image.load(f"{sprite_path}{image_path}").convert_alpha()
        _images[image_path] = image
        return image
    except pygame.error as e:
        print(f"Impossible de charger l'image '{image_path}': {e}")
        return None

@staticmethod 
def cut_in_image(image_path: str, pos: tuple) -> pygame.Surface:
    # Retourne l'image à la i ème ligne, j ème colonne  -> pos = (i, j)
    return _images[image_path].subsurface(
            [
                pos[0]*tile_size + tileset_x_offset, 
                pos[1]*tile_size + tileset_y_offset, 
                (pos[0]+1)*tile_size + tileset_x_offset,
                (pos[1]+1)*tile_size + tileset_y_offset
            ]
        )
        
    


if __name__ == '__main__':
    pass