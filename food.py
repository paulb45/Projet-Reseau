class Food():
    def __init__(self,energy):
        self.energy=energy
        
    """ GETTERS """
        
    def get_energy(self):return self.energy
    
    
    """ SETTERS """
    
    def set_energy(self,eng):self.energy=eng
    """ fonction qui verifie si la nourriture est consommee
    """ 
    def is_dead(self):
        return  self.energy<=0
       