from logic.game import Game
from logic.bob import Bob
from logic.food import Food
from logic.grid import Grid

def print_bobs_stat():
    bobs = game.grid.get_all_bobs()
    for _, elements in bobs.items():
        for bob in elements:
            print(bob.get_stats())
            
game = Game()

print(game.grid.map)
game.bobs_play()
print("\n\n")
print(game.grid.map)
