from graphic.mainSurface import MainSurface
from config import *
from logic.game import Game
window = MainSurface()



game = Game(get_value_int("quantity_food"),get_value_int("energy_food"),get_value_int("nb_ticks_day"),get_value_int("pop_init"),get_value_int("nb_days"))
# Gestion du menu ? -> où dans main surface

while True:
    # Jouer la journée de logic
    game.day_play()
    # Gestion graphique
    window.run(game.grid.map)
