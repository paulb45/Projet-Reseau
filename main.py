# FAITE DES TESTS POUR VOIR SI CA FONCTIONNE ICI... SVP...
# On a vraiment besoin d'avoir la certitude que tout fonctionne dès qu'on va l'implémenter sur notre interface graphique
# Donc utilisez ce qu'il y a dans affichage term (comme avec l'exemple dessous)

from affichage_term import *
from game import Game
import time
n=500
quantity_food = 200
init_energy_food = 100
nb_tick_day = 5
P0 = 100
grid = Grid(10,10)
nb_day = 1
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
bob1=Bob(100)
bob2=Bob(200)
game.create_bob(bob1, 5,5)
bob1.move()
bob3=(bob2.parthenogenesis())
game.create_bob(bob3, 5,5)

while n:
    bob3.move()
    n-=1



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
#game.partie()

    

for coords ,bobs in game.grid.map.items():
    for bob in bobs:
        if isinstance(bob,Bob):
            print("la velocity de ce bob est :"+str(bob.speed))
            print("le buffer est "+str(bob.speed_buff))
            
print("nombre des bobs a la fin est "+str(count_obj(game.grid, "Bobs")))