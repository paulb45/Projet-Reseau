from logic.bob import Bob
from logic.food import Food
from logic.grid import Grid
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import *

class Game():
    def __init__(self):
        self.grid=Grid()
        self.init_bobs()
        self.spawn_food()
        
    
    def init_bobs(self):
        """init bob
            initialisation des P0 bobs dans exactement P0 places
        """
        for _ in range(Config.P0):
            is_spawn = False
            while not is_spawn :
                pos = self.grid.choose_random_tile()
                if not self.grid.has_bob(pos):
                    is_spawn = True
            self.grid.create_bob(pos)
          
    def spawn_food(self):
        """generer la nouritures
        """
        for _ in range(Config.quantity_food):
            pos = self.grid.choose_random_tile()
            self.grid.map[pos].append(Food())

    def bob_play_tick(self, bob: Bob, pos=None):
        if pos == None:
            pos = self.grid.get_position(bob)
        if bob.get_E() == Bob.get_Emax():
            self.grid.place_child(bob.parthenogenesis(), pos)          
        elif (food := self.grid.has_food(pos)):
            if bob.eat(food):
                self.grid.destroy_object(food, pos)
            
        else:
            mouv = bob.move()
            new_pos = pos[0] + mouv[0], pos[1] + mouv[1]
            if self.grid.is_pos_in_map(new_pos):
                self.grid.map[new_pos].append(bob)
                self.grid.destroy_object(bob, pos)
                if (food := self.grid.has_food(new_pos)):
                    bob.E += 0.5 # Compence l'effet de manger juste après
                    if bob.eat(food):
                        self.grid.destroy_object(food, new_pos)
                if bob.is_dead():
                    self.grid.destroy_object(bob, new_pos)
                else:
                    bobs=self.grid.bobs_in_case(new_pos)
                    for target in bobs :
                        if bob.attack(target):
                            self.grid.destroy_object(target,new_pos)
                            break
            else: self.grid.destroy_object(bob, pos)

    def reset_bobs_last_move(self):
        bobs_map = self.grid.get_all_bobs()
        for _, bobs in bobs_map.items():
            for bob in bobs:
                bob.reset_last_move()

    def bobs_play_tick(self):
        bobs_map = self.grid.get_all_bobs()
        for pos, bobs in bobs_map.items():
            for bob in bobs:
                self.bob_play_tick(bob, pos)
    
    def bobs_play_day(self):
        for _ in range(nb_ticks_day):
            self.bobs_play_tick()
                
    def day_play(self):
        self.reset_bobs_last_move()
        self.bobs_play_day()
        self.grid.destroy_all_foods()
        self.spawn_food()