import random
import config
from logic.food import Food

class Bob():
    
    Emax=200
    Emother=150
    Echild=50
    
    
    def __init__(self,E=Emax//2, speed=1, mass=1, memory=0, perception=0):
        self.E=E
        self.speed=speed
        self.mass=mass
        self.memory=memory
        self.perception=perception
        self.stats = [self.speed, self.mass, self.memory, self.perception]
        self.last_move=[0,0]
        self.speed_buff = 0.0
        
    
    """ Getters """
    def get_speed(self):
        return self.speed
    def get_mass(self):
        return self.mass
    def  get_memory(self):
        return self.memory
    @classmethod
    def get_Emax(cls):
        return cls.Emax
    def get_E(self):
        return self.E
    @classmethod
    def get_Emother(cls):
        return cls.Emother
    def get_last_move(self):
        return self.last_move
    @classmethod
    def get_Echild(cls):
        return cls.Echild
    
    """ Setters """
    def set_speed(self,spd):
        self.speed=spd
    def set_mass(self,mass):
        self.mass=mass
    def set_memory(self,memory):
        self.memory=memory
    @classmethod    
    def set_Emax(cls,emax):
        cls.Emax=emax
    def set_E(self,E):
        self.E=E
    def set_last_move(self,lst_mv):
        self.last_move=lst_mv
    def set_speed_buff(self,spd_buff): # WTF
        self.speed_buff
    @classmethod    
    def set_Emother(cls,E):
        cls.Emother=E
    @classmethod        
    def set_Echild(cls,E):
        cls.Echild=E  
    
      
    def move(self) -> tuple:
        """Déplace Bob en choisissant aléatoirement une direction  
            la gestion ce fait dans la class Game
            return: les nouvelles coordonnées de bob 
        """
        #Version sans vision
        self.speed_buff += self.speed
        speed_mouvement= int(self.speed_buff)
        self.speed_buff -= speed_mouvement
        self.set_last_move((
                            x:=random.randint(0, speed_mouvement) * random.choice((1,-1)), 
                            (speed_mouvement - abs(x)) * random.choice((1,-1))
                           ))
        self.E -= 0.5 * self.mass * (self.speed**2)
        return self.get_last_move()

    def eat(self,food: Food) -> bool: 
        
        # cette fonction renvoie True la nourriture doit être détruite 
        """Fait en sorte que BOB mange la nourriture spécifiée et augmente son énergie.

        Args:
            food (FOOD): la nourriture que bob va manger
        Returns:
            true siginifie que Efood=0 donc il faut detruire food dans la class Game
            false -->Efood>0
            la gestion se fait dans la class Game
        """
        self.E -= 0.5
        self.E+=food.energy
        if(self.E>self.Emax):
            food.set_energy(self.E-self.Emax)
            self.E=self.Emax
        else:
            food.set_energy(0)
        return food.is_dead() 
     
    def is_dead(self) -> bool:
        """vérifie si Bob dead ou non

        Returns:
            bool: true si BOB est mort non sinon 
        """
        return self.E <=0
    
    def parthenogenesis(self) -> object:
        """si bob atteint l'energie maximal il aura un bebe
        Returns:
            BOB: si il ya une parthenogenesis
            -1 sinon
        """
        self.E=self.Emax-self.Emother
        child_stats = []
        for stat in self.stats:
            child_stat = stat + random.uniform(-config.mutation_rate, config.mutation_rate)
            if child_stat < 0:
                child_stat = 0
            child_stats.append(child_stat)
            
        return Bob(Bob.Echild, *child_stats)   
        
    def get_stats(self):
        return [self.E, self.speed, self.mass, self.memory, self.perception]
    # NE MARCHE PAS
    def attack(self,target) -> bool:
        """si bm/Bm<2/3 --> bob il peut attaqué target

        Args:
            target (Bob): bob qui se trouve dans la meme case que notre bob

        Returns:
            bool: True si bob il a bien attaqué
                  False sinon
                  ce retour sert dans game pour destroy target  
        """
        #big_boy,small_boy=self.get_E(),target.get_E()if self.get_E()>target.get_E()else target.get_E(),self.get_E()
        if(target.get_E()/self.get_E()<2/3):
            print("ei",self.get_E(),end="")
            E_gain=0.5*target.get_E()*(1-(target.get_E()/self.get_E()))
            self.set_E(self.get_E()+E_gain)
            print("ef",self.get_E())
            
            return True
        return False
        
            
            
                
        
