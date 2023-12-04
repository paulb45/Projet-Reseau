# FAITE DES TESTS POUR VOIR SI CA FONCTIONNE ICI... SVP...
# On a vraiment besoin d'avoir la certitude que tout fonctionne dès qu'on va l'implémenter sur notre interface graphique
# Donc utilisez ce qu'il y a dans affichage term (comme avec l'exemple dessous)

from affichage_term import *
from game import Game
import time
quantity_food = 70
init_energy_food = 10
nb_tick_day = 5
P0 = 4
grid = Grid(10,10)
nb_day = 1

game = Game(quantity_food,init_energy_food,nb_tick_day,P0,grid,nb_day)
game.init_bobs()    #Initialisation des bobs
game.spawn_food()   #generation de la nourriture
    
while nb_tick_day>0:
    game.bob_play()
    nb_tick_day-=1
    time.sleep(1)
    affiche_map(game.grid.map)
copy_dict=dict(game.grid.map)
for coords ,foods in copy_dict.items():
    for food in foods:
        if isinstance(food,Food):
            game.destroy_object(food)
affiche_map(game.grid.map)