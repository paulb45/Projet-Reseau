import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import *

class Food():
    def __init__(self,energy=Config.energy_food):
        self.energy=energy
        
    """ GETTERS """
        
    def get_energy(self): return self.energy
    
    
    """ SETTERS """
    
    def set_energy(self,eng): self.energy=eng
    
    def is_dead(self):
        """ fonction qui verifie si la nourriture est consommee
        """ 
        return  self.energy<=0
       