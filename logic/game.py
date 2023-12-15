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

    def bob_play(self, bob: Bob, pos=None):
        can_eat = False
        if pos == None:
            pos = self.grid.get_position(bob)
        if bob.get_E() == Bob.get_Emax():
            self.grid.place_child(bob.parthenogenesis(), pos)          
        elif (food := self.grid.has_food(pos)):
            can_eat = True
            """
        elif (bob := self.grid.has_bob(pos)):
            # Mettre l'attaque ici
            pass 
            """
        else:
            mouv = bob.move()
            new_pos = pos[0] + mouv[0], pos[1] + mouv[1]
            if self.grid.is_pos_in_map(new_pos):
                self.grid.map[new_pos].append(bob)
                if (food := self.grid.has_food(new_pos)):
                    can_eat = True
                    bob.E += 0.5 # Compence l'effet de manger juste après
            self.grid.destroy_object(bob, pos)
            pos = new_pos
            
        if can_eat:
            if bob.eat(food):
                self.grid.destroy_object(food, pos)
        
        if bob.is_dead():
            self.grid.destroy_object(bob, pos)
        
    def bobs_play(self):
        bobs_map = self.grid.get_all_bobs()
        for pos, bobs in bobs_map.items():
            for bob in bobs:
                self.bob_play(bob, pos)
                
    def day_play(self):
        """chaque jour d=100 ticks
           chaque jours f=200 points de nourriture
           Ef=100 energie de la nourriture
        """
        self.bobs_play()
        self.grid.destroy_all_foods()
        self.spawn_food()