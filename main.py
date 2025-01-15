import threading
from copy import deepcopy

from graphic.mainSurface import MainSurface
from config import *
from logic.game import Game

from pytoc_sender import send_grid
from socket_listen import startlisten
from action_buffer import ActionBuffer

# initialisation de la fenetre principale
window = MainSurface()

# boucle menu post jeu
while not window.menu.game_is_on:
    window.run_menu()

# Initilisation de la logique
window.start_game()
game = Game()

# Initialisaiton de l'écoute réseau
network_thread = threading.Thread(target=startlisten)
network_thread.start()

while True:
    grid_copy = deepcopy(game.grid)

    send_grid(grid_copy)

    grid_copy.fusion(ActionBuffer.get_buffer())

    logic_thread = threading.Thread(target=game.day_play)

    logic_thread.start()
    
    window.run(grid_copy)

    logic_thread.join()

