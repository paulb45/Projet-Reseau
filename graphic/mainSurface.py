import pygame

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import *

from graphic.interface import Interface
from graphic.cameraController import CameraController
from graphic.eventController import EventController

from collections import defaultdict
class Bob:pass
class Food:pass
map = defaultdict(lambda: 0, {(1,1): [Bob()], (50,50) : [Food(), Bob()], (99,99) : [Food()]})

class MainSurface:

    def __init__(self):
        pygame.init()

        # Création de la fenêtre
        self.window = pygame.display.set_mode(window_size, pygame.RESIZABLE)
        self.window.fill("black")

        pygame.display.set_caption("Game Of Life")

        # clock pour la gestion des FPS
        self.clock = pygame.time.Clock()

        # surface du jeu, toute la map
        self.game_surface = Interface(screen_size)

        self.camera = CameraController(self.game_surface)

        self.event_controller = EventController(self.camera)

        self.menu = None # classe menu ?

        # screen.place_interface_in_middle(window)

    def run(self):
        while True:
            self.event_controller.run_events()
            
            # rendu du jeu
            self.game_surface.render_game(map)
        
            self.window.blit(self.camera.get_viewpoint(), (0,0))

            pygame.display.flip()
            self.clock.tick(max_framerate)


if __name__ == '__main__':
    MainSurface().run()