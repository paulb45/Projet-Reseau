import threading

from graphic.mainSurface import MainSurface
from config import *
from logic.game import Game
window = MainSurface()

# Initilisation de la logique
global game
game = Game(int(get_value("quantity_food")),int(get_value("energy_food")),int(get_value("nb_ticks_day")),int(get_value("pop_init")),int(get_value("nb_days")))

map = game.grid.map

while True:
    map = game.grid.map.copy()

    logic_thread = threading.Thread(target=game.day_play)

    logic_thread.start()
    
    window.run(map)

    logic_thread.join()