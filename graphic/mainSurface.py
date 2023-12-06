import pygame
import pygame_menu
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import *

from graphic.interface import Interface
from graphic.cameraController import CameraController
from graphic.eventController import EventController
from graphic.test_menu import Menu

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

        self.menu=Menu(self.window)
        #self.menu.to_print("main_menu")

    def run(self, map):           
        self.event_controller.run_events()
        # rendu du jeu
        self.game_surface.render_game(map)
        
        self.window.blit(self.camera.get_viewpoint(), (0,0))

        pygame.display.flip()
        self.clock.tick(max_framerate)


if __name__ == '__main__':
    MainSurface().run()