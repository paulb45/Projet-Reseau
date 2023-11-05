import pygame
import sys
import time

from graphic.interface import Interface
from graphic.cameraController import CameraController
from config import *

pygame.init()

# Création de la fenêtre
window = pygame.display.set_mode(window_size)
window.fill("black")
pygame.display.set_caption("Game Of Life")

clock = pygame.time.Clock()

screen = Interface(window_size)

camera = CameraController(screen)

move_mouse_timer = time.time()

while True:
    # Faire une fonction event_handler ?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                camera.move_left()
            elif event.key == pygame.K_RIGHT:
                camera.move_right()
            elif event.key == pygame.K_UP:
                camera.move_up()
            elif event.key == pygame.K_DOWN:
                camera.move_down()
            elif event.key == pygame.K_p:
                camera.zoom_in()
            elif event.key == pygame.K_m:
                camera.zoom_out()

    # réduire la vitesse de déplacement avec la souris
    if (time.time() - move_mouse_timer) >= .02:
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # voir où est le curseur de la souris
        if (mouse_x < 10):
            camera.move_left()
        if (mouse_x > (window_size[0] - 10)):
            camera.move_right()
        if (mouse_y < 10):
            camera.move_up()
        if (mouse_y > (window_size[1] - 10)):
            camera.move_down()

        move_mouse_timer = time.time()
    
    # RENDER YOUR GAME HERE
    screen.render_game()
    window.blit(camera.get_viewpoint(), (0,0))

    pygame.display.flip()
    clock.tick(max_framerate)
