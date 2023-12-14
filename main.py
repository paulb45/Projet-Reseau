import threading

from graphic.mainSurface import MainSurface
from config import *
from logic.game import Game

window = MainSurface()

while not window.menu.game_is_on:
    window.run()

# Initilisation de la logique
global game
game = Game(Config.quantity_food,Config.energy_food,Config.nb_tick_day,Config.P0,Config.nb_day)

window.start_game()

while True:
    map = game.grid.map.copy()

    logic_thread = threading.Thread(target=game.day_play)

    logic_thread.start()
    
    window.run(map)

    logic_thread.join()