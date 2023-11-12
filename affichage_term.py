from collections import defaultdict
from bob import Bob
from food import Food
from grid import Grid
from config import N, M

#N est la largeur (taille de l'axe x de la grille)
#M est la hauteur (taille de l'axe y de la grille)

grid = defaultdict(lambda:0, {
        (1,1): Bob(), (2,2): Food(), (3,3): [Bob(), Food()],
      (7,5):[Bob(),Bob(),Food(),Bob()],(5,5):[Food(),Food()]})


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
            print(f"{to_print:^5}|", end='')
        print(f"\n   {split_line_h}-") # Affichage fin de ligne