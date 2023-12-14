import threading

from graphic.mainSurface import MainSurface
from config import *
from logic.game import Game
window = MainSurface()

# Initilisation de la logique
global game
game = Game(get_value_int("quantity_food"),get_value_int("energy_food"),get_value_int("nb_ticks_day"),get_value_int("pop_init"),get_value_int("nb_days"))

map = game.grid.map

while True:
    map = game.grid.map.copy()

    logic_thread = threading.Thread(target=game.day_play)

    logic_thread.start()
    
    window.run(map)

    logic_thread.join()