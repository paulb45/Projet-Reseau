from graphic.mainSurface import MainSurface
from logic.game import Game
window = MainSurface()

# Initilisation de la logique
quantity_food = 300
init_energy_food = 10
nb_tick_day = 5
P0 = 5
nb_day = 1
game = Game(quantity_food,init_energy_food,nb_tick_day,P0,nb_day)

# Gestion du menu ? -> où dans main surface


while True:
    # Jouer la journée de logic
    game.day_play()
    
    # Gestion graphique
    window.run(game.grid.map)
