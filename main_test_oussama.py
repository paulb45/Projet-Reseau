# FAITE DES TESTS POUR VOIR SI CA FONCTIONNE ICI... SVP...
# On a vraiment besoin d'avoir la certitude que tout fonctionne dès qu'on va l'implémenter sur notre interface graphique
# Donc utilisez ce qu'il y a dans affichage term (comme avec l'exemple dessous)

from affichage_term import *
from game import Game

quantity_food = 70
init_energy_food = 10
nb_tick_day = 60
P0 = 5
grid = Grid(10,10)
nb_day = 1

game = Game(quantity_food,init_energy_food,nb_tick_day,P0,grid,nb_day)
bob=Bob(1,10,100,10)
grid.map[0,0]=[bob]
#affiche_map(grid.map)
print(bob.last_move)
bob.move(2)
print(bob.last_move)
#affiche_map(grid.map)
