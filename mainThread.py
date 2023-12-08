import threading

from graphic.mainSurface import MainSurface
from config import *
from logic.game import Game
window = MainSurface()

# Initilisation de la logique
quantity_food = 300
init_energy_food = 10
nb_tick_day = 5
P0 = 5
nb_day = 1

global game
game = Game(Config.quantity_food,Config.energy_food,Config.nb_tick_day,Config.P0,Config.nb_day)

map = game.grid.map

while True:
    map = game.grid.map.copy()

    logic_thread = threading.Thread(target=game.day_play)

    logic_thread.start()
    
    window.run(map)

    logic_thread.join()