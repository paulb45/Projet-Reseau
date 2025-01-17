import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import *

from logic.item import Item

class Food(Item):
    def __init__(self, energy=Config.energy_food, local=True, player_id=0):
        super().__init__(local_item=True, player_id=player_id)
        self.energy=energy
        
    """ GETTERS """
        
    def get_energy(self): return self.energy
    
    
    """ SETTERS """
    
    def set_energy(self,eng): self.energy=eng
    
    def is_dead(self):
        """ fonction qui verifie si la nourriture est consommee
        """ 
        return  self.energy<=0
       