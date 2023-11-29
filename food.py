class Food():
    def __init__(self,energy):
        self.energy=energy
    
    def get_energy(self):return self.energy
    def set_energy(self,eng):self.energy=eng 
    def is_dead(self):
        return  self.energy<=0
       