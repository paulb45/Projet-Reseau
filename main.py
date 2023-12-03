# FAITE DES TESTS POUR VOIR SI CA FONCTIONNE ICI... SVP...
# On a vraiment besoin d'avoir la certitude que tout fonctionne dès qu'on va l'implémenter sur notre interface graphique
# Donc utilisez ce qu'il y a dans affichage term (comme avec l'exemple dessous)

from affichage_term import *
from game import Game

quantity_food = 3
init_energy_food = 10
nb_tick_day = 5
P0 = 3
grid = Grid(10,10)
nb_day = 1

game = Game(quantity_food,init_energy_food,nb_tick_day,P0,grid,nb_day)
#game.init_bobs()
bob=Bob(1,1,100,0)
game.create_bob(bob, 1,1)
affiche_map(game.grid.map)
game.destroy_object(bob)
affiche_map(game.grid.map)

"""for i in range(3):
    game.day_play()
    affiche_map(game.grid.map)
    #game.day_play()"""
    


#game.create_bob(Bob(1,1,100,0), 1,1)
#affiche_map(game.grid.map)


#affiche_map(game.grid.map)
#game.bob_play()
#affiche_map(game.grid.map)
#game.bob_play()

#affiche_map(game.grid.map)