import threading
from copy import deepcopy

from graphic.mainSurface import MainSurface
from config import *
from logic.game import Game

# initialisation de la fenetre principale
window = MainSurface()

# boucle menu post jeu
while not window.menu.game_is_on:
    window.run_menu()

# Initilisation de la logique
window.start_game()
game = Game()

while True:
    grid_copy = deepcopy(game.grid)

    logic_thread = threading.Thread(target=game.day_play)

    logic_thread.start()
    
    window.run(grid_copy)

    logic_thread.join()

