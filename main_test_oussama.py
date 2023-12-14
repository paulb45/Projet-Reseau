
from affichage_term import *
from game import Game
import time

quantity_food = 10
init_energy_food = 100
nb_tick_day = 5
P0 = 1000
grid = Grid(100,100)
nb_day = 100
########################## Foncction pour faciliter les testes##############################
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
"""
game.init_bobs()    #Initialisation des bobs
game.spawn_food()   #generation de la nourriture
affiche_map(game.grid.map)
#print("nombre des foods  a l'initialisation est "+str(count_obj(game.grid, "Foods")))
#print("nombre des bobs a l'initialisation est "+str(count_obj(game.grid, "Bobs")))
    
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
""" 
game.partie()
bob2=Bob(100)


