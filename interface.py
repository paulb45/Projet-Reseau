import pygame
from objectSprite import SpritesGestion
from gameView import GameView

class Interface(pygame.Surface):
    def __init__(self, size, flags=0):
        super().__init__(size, flags)
        self.load_images()

    def load_images(self):
        self.tileset = SpritesGestion.load_image('Tileset.png')
        self.grass_tile = SpritesGestion.cut_in_image('Tileset.png', (0,0))

    def render_game(self, tile):
        GameView.generate_ground(self, tile)


# Permet de lancer une instance uniquement si on exécute interface.py
# Ne l'éxecute pas lors d'un import ! (évite des tests douteux dans le main.py)
if __name__ == "__main__":
    Interface(1280, 720).run()