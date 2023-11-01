import pygame
import sys
from objectSprite import SpritesGestion
from gameView import GameView

class Interface():
    def __init__(self, width, height):
        pygame.init()
        self.initialise_window(width, height)
        self.sprites = SpritesGestion()
        self.clock = pygame.time.Clock()
        self.max_framerate = 60

    def initialise_window(self, width, height):
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Game Of Life")


    def close_window(self):
        pygame.quit()
        sys.exit()


    def run(self):
        while True:
            # Faire une fonction event_handler ?
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close_window()

            self.screen.fill("black")
            GameView.generate_ground(self.screen, self.sprites.grass_tile)
            # RENDER YOUR GAME HERE

            # flip() the display to put your work on screen
            pygame.display.flip()

            self.clock.tick(self.max_framerate)  # limits FPS to 60



# Permet de lancer une instance uniquement si on exécute interface.py
# Ne l'éxecute pas lors d'un import ! (évite des tests douteux dans le main.py)
if __name__ == "__main__":
    Interface(1280, 720).run()