from collections import defaultdict
from logic.bob import Bob
from logic.food import Food
from logic.grid import Grid
from logic.game import Game
from config import N, M

#N est la largeur (taille de l'axe x de la grille)
#M est la hauteur (taille de l'axe y de la grille)
speed = 1
mass = 10
E = 100
speed_buff=1
"""
test_grid = defaultdict(lambda:0, {
        (1,1): Bob(speed, mass, E, speed_buff), (2,2): Food(E), 
        (3,3): [Bob(speed, mass, E, speed_buff), Food(E)],
        (7,5):[Bob(speed, mass, E, speed_buff),Bob(speed, mass, E, speed_buff),Food(E),Bob(speed, mass, E, speed_buff)],
        (5,5):[Food(E),Food(E)]
      }
                        )
"""

def affiche_map(grid):
    space = 5
    split_line_h = "-"*((space+1)*N)
  
    # Affichage des coordonnées sur x
    print("    ", end="")
    for x in range(N):
      if x%5 == 0:
        print(f"{x:^5} ", end="")
      else:
        print(" "*(space+1), end='')
  
    print(f"\n   {split_line_h}-")
  
    for x in range(M):
        # Affiche des coordonnées sur y
        if x%5 == 0:
          print(f"{x:^3}|", end="")
        else:
          print("   |", end='')

      
        for y in range(N):
          # Gestion de l'affichage de chaque case
            to_print =""
            try:
              match grid[y,x]:
                case 0: to_print = " "
                case Bob(): to_print = "B"
                case Food(): to_print = "F"
                case list(): 
                  bob_count = 0
                  food_count = 0
                  for elem in grid[y,x]:
                    if isinstance(elem, Bob):
                      bob_count += 1
                    else: 
                      food_count += 1               
                  to_print = f"{bob_count}:{food_count}"

                case _:   to_print = " "
            except:
              pass
                
            print(f"{to_print:^5}|", end='')
        print(f"\n   {split_line_h}-") # Affichage fin de ligne

     

#test
"""
grd=Grid(10,10)
Game=Game(3,100,10,3,grd,3)

Game.bob_play()
"""

"""
_________Grid_________

scan_around()  test OK
get_position() test OK
get_items()    test OK


________Game__________

init_bob()       test OK
spawn_food()     test OK
bob_play()       test OK
destroy_object() test OK
day_play()       test OK
create_bob()     test OK
count()          test OK

_______Bob___________

move()            test OK
eat()             test OK
is_dead()         test OK
parthenogenesis() test OK

______Food____________
is_dead()         test OK
"""
