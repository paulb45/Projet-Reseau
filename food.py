class Food():
    def __init__(self,energy):
        self.energy=energy
     #ajouter une method comme is_dead()§§bob
    def get_energy(self):return self.energy
    def set_energy(self,eng):self.energy=eng 
    def energy_food(self):
        return  self.energy<=0
       