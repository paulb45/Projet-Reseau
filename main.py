import pygame
import sys
from interface import Interface
from config import *

pygame.init()

# Création de la fenêtre
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Game Of Life")

clock = pygame.time.Clock()

screen = Interface(window_size)

while True:
    # Faire une fonction event_handler ?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    window.fill("black")
    
    # RENDER YOUR GAME HERE
    screen.render_game(screen.grass_tile)
    window.blit(screen, (0,0))


    pygame.display.flip()
    clock.tick(max_framerate)
