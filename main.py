# FAITE DES TESTS POUR VOIR SI CA FONCTIONNE ICI... SVP...
# On a vraiment besoin d'avoir la certitude que tout fonctionne dès qu'on va l'implémenter sur notre interface graphique
# Donc utilisez ce qu'il y a dans affichage term (comme avec l'exemple dessous)

from affichage_term import *
from game import Game

quantity_food = 300
init_energy_food = 10
nb_tick_day = 60
P0 = 20
grid = Grid(10,10)
nb_day = 1

game = Game(quantity_food,init_energy_food,nb_tick_day,P0,grid,nb_day)
bob=Bob(1,10,1,10)
game.create_bob(bob,0,0)
def count_obj(grid, name):
    nb_bob = 0
    nb_food = 0
    for coords, bob_list in grid.map.items():
        for obj in bob_list:
            if isinstance(obj, Bob):
                nb_bob = nb_bob + 1
            else :
                nb_food = nb_food + 1 
    
    if (name=="Bobs"):
        return nb_bob
    elif(name=="Foods"):
        return nb_food
    
    
"""
game.init_bobs()
game.spawn_food()
affiche_map(grid.map)

#print("nombre des foods avant bob_play est "+str(count_obj(game.grid, "Foods")))
#print("nombre des bobs avant bob_play est "+str(count_obj(game.grid, "Bobs")))
game.day_play()
#affiche_map(game.grid.map)
affiche_map(grid.map)
#print("nombre des bobs vivant est "+str(count_obj(game.grid, "Bobs")))
#print("nombre des foods restant est "+str(count_obj(game.grid, "Foods")))
"""
for i in range(3):
    game.day_play()
    affiche_map(grid.map)