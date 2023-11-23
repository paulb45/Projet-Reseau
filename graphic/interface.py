import pygame
import graphic.objectSprite as objectSprite
import graphic.gameView as gameView

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import *

class Interface(pygame.Surface):
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
        gameView.generate_ground(self, self.grass_tile)
        gameView.place_entity(self, self.bob, (80,0))


# Permet de lancer une instance uniquement si on exécute interface.py
# Ne l'éxecute pas lors d'un import ! (évite des tests douteux dans le main.py)
if __name__ == "__main__":
    pass