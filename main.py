from graphic.mainSurface import MainSurface
from config import *
from logic.game import Game
window = MainSurface()



game = Game(int(get_value("quantity_food")),int(get_value("energy_food")),int(get_value("nb_ticks_day")),int(get_value("pop_init")),int(get_value("nb_days")))
# Gestion du menu ? -> où dans main surface

while True:
    # Jouer la journée de logic
    game.day_play()
    # Gestion graphique
    window.run(game.grid.map)
