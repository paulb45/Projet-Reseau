import pygame
import pygame_menu
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import *

from graphic.interface import Interface
from graphic.cameraController import CameraController
from graphic.eventController import EventController
from graphic.game_menu import GameMenu

from logic.game import Game

class MainSurface:

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(music_path + "2-15. Crossing the Iron Bridge.flac")
        pygame.mixer.music.play(-1,0.0)
        pygame.mixer.music.set_volume( 0.05)
        self.current_day =0

        # Création de la fenêtre
        self.window = pygame.display.set_mode(window_size, pygame.RESIZABLE)
        self.window.fill("black")

        pygame.display.set_caption("Game Of Life")

        # icone de l'application
        pygame.display.set_icon(pygame.image.load(assets_path + "icon.png"))

        # clock pour la gestion des FPS
        self.clock = pygame.time.Clock()

        # surface du jeu, toute la map
        self.game_surface = None

        self.camera = None

        self.menu = GameMenu(self.window)

        self.event_controller = EventController(None, self.menu)
        
        self.menu.main_menu.enable()
        #self.menu.to_print("main_menu")


    def start_game(self):
        self.game_surface = Interface(Config.screen_size)
        #print(Config.width_map,Config.height_map)
        self.camera = CameraController(self.game_surface)
        self.menu.zoom_slider.set_value(self.camera.get_zoom_ratio())
        self.event_controller.camera = self.camera

    def run(self, grid):
        current_tick = 1
        #current day ne sert qu'a l'affichage
        self.game_surface.init_values_bobs_day(grid)

        while(current_tick < max_framerate):
            self.event_controller.run_events()

            if self.menu.game_is_on:
                self.game_surface.render_game(grid, current_tick)
                self.window.blit(self.camera.get_viewpoint(), (0,0))
                self.menu.game_screen.draw(self.window)
                
            else:
                self.menu.main_menu.draw(self.window)
        
            pygame.display.flip()

            self.clock.tick(max_framerate)
            current_tick += 1
            if current_tick == max_framerate - 1:
                self.current_day += 1
                self.menu.daydisplay.set_title('day :' + str(self.current_day))
            self.menu.tickdisplay.set_title('tick :' + str(current_tick))
            


    def run_menu(self):
        self.event_controller.run_events()

        self.menu.main_menu.draw(self.window)

        pygame.display.flip()

        self.clock.tick(max_framerate)


if __name__ == '__main__':
    carte ={}
    MainSurface().run(carte)