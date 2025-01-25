import threading, sys
from copy import deepcopy

from graphic.mainSurface import MainSurface
from config import *
from logic.game import Game

if sys.argv != None:
    listen_port = int(sys.argv[1])
    sending_port = int(sys.argv[2])
else:
    listen_port = 55005
    sending_port = 55006

   

# initialisation de la fenetre principale
window = MainSurface()

# boucle menu post jeu
while not window.menu.game_is_on:
    window.run_menu()

# Initilisation de la logique
window.start_game()
game = Game(listen_port, sending_port)

while True:
    grid_copy = deepcopy(game.grid)

    logic_thread = threading.Thread(target=game.day_play)

    logic_thread.start()
    
    window.run(grid_copy)

    logic_thread.join()

