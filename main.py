import threading

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
    #map = game.grid.map.copy()

    logic_thread = threading.Thread(target=game.day_play)

    logic_thread.start()
    
    window.run(game.grid.map)

    logic_thread.join()
