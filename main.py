from graphic.mainSurface import MainSurface
from config import *
from logic.game import Game
window = MainSurface()



game = Game(Config.quantity_food,Config.energy_food,Config.nb_tick_day,Config.P0,Config.nb_day)
# Gestion du menu ? -> où dans main surface

while True:
    # Jouer la journée de logic
    game.day_play()
    # Gestion graphique
    window.run(game.grid.map)
