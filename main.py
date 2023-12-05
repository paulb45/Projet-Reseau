# FAITE DES TESTS POUR VOIR SI CA FONCTIONNE ICI... SVP...
# On a vraiment besoin d'avoir la certitude que tout fonctionne dès qu'on va l'implémenter sur notre interface graphique
# Donc utilisez ce qu'il y a dans affichage term (comme avec l'exemple dessous)

from affichage_term import *
from game import Game
import time

quantity_food = 300
init_energy_food = 10
nb_tick_day = 20
P0 = 10
grid = Grid(10,10)
nb_day = 1
#************************* Foncction pour faciliter les testes ****************************#
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
game = Game(quantity_food,init_energy_food,nb_tick_day,P0,grid,nb_day)
#game.init_bobs()    #Initialisation des bobs
#game.spawn_food()   #generation de la nourriture
#affiche_map(game.grid.map)
#print("nombre des foods  a l'initialisation est "+str(count_obj(game.grid, "Foods")))
#print("nombre des bobs a l'initialisation est "+str(count_obj(game.grid, "Bobs")))
    
"""while nb_tick_day>0:
    game.bob_play()
    nb_tick_day-=1
    time.sleep(1)
    affiche_map(game.grid.map)
    
copy_dict=dict(game.grid.map)
for coords ,bobs in copy_dict.items():
    for bob in bobs:
        if isinstance(bob,Bob):
            print("l'energie du bobs est"+str(bob.E))
for coords ,foods in copy_dict.items():
    for food in foods:
        if isinstance(food,Food):
            game.destroy_object(food)
affiche_map(game.grid.map)"""
game.day_play()
affiche_map(game.grid.map)