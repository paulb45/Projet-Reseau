import pygame

from graphic.interface import Interface
from graphic.gameView import GameView
from graphic.cameraController import CameraController
from graphic.eventController import EventController
from config import *

pygame.init()

# Création de la fenêtre
window = pygame.display.set_mode(window_size, pygame.RESIZABLE)
window.fill("black")
pygame.display.set_caption("Game Of Life")

clock = pygame.time.Clock()

screen = Interface(screen_size)

camera = CameraController(screen)

eventController = EventController(camera)

GameView.place_interface_in_middle(screen, window)
while True:
    eventController.run_events()
    
    # RENDER YOUR GAME HERE
    screen.render_game()
    window.blit(camera.get_viewpoint(), (0,0))

    pygame.display.flip()
    clock.tick(max_framerate)
