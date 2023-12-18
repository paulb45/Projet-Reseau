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
bob = Bob(speed=10)
game.grid.map[(10,10)].append(bob)
for _ in range(3):
    print(bob.move())

print(bob.last_move)