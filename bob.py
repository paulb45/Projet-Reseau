from food import Food
from grid import *
import random

class Bob():
    
    Emax=200
    Emother=150
    Echild=50
    
    def __init__(self,speed,mass,E,speed_buff):
        self.speed=speed
        self.mass=mass
        self.memory=None
        self.E=E
        self.last_move=[None,None]
        self.speed_buff=speed_buff
    
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
    def set_speed_buff(self,spd_buff):
        self.speed_buff
    @classmethod    
    def set_Emother(cls,E):
        cls.Emother=E
    @classmethod        
    def set_Echild(cls,E):
        cls.Echild=E  
    
      
    def move(self,speed)->tuple:
        """Déplace Bob en choisissant aléatoirement une direction   
            
        """
        last_move=self.get_last_move()
        for mov in range(speed):
            choices=["horizontal","vertical"]
            direction=random.choice(choices)
            if direction=="horizontal":
                last_move=[last_move[0]+random.choice([1,-1]),last_move[1]]
            else:
                last_move=[last_move[0],random.choice([1,-1] )+last_move[1]]
            self.set_last_move(last_move)
        return self.get_last_move()

    def eat(self,food: Food)->None: 
        
        # cette fonction renvoie True la nourriture doit être détruite 
        """Fait en sorte que BOB mange la nourriture spécifiée et augmente son énergie.

        Args:
            food (FOOD): la nourriture que bob va manger
        """
        self.E+=food.energy
        if(self.E>self.Emax):
            food.set_energy(self.E-self.Emax)
            self.E=self.Emax
        else:
            food.set_energy(0)    
        return food.is_dead() 
     
    def is_dead(self)->bool:
        """vérifie si Bob mort ou non

        Returns:
            bool: true si BOB est mort non sinon 
        """
        return self.E <=0
    def parthenogenesis(self):
        """si bob atteint l'energie maximal il aura un bebe
        Returns:
            BOB: si il ya une parthenogenesis
            -1 sinon
        """
        if(self.E>=self.Emax):
            self.E=self.Emax-self.Emother
            bebe_bob= Bob(self.speed,self.mass,self.Echild,self.speed_buff)
            bebe_bob.last_move=self.last_move
            return bebe_bob 
            #TODO dans game
            #ajouter le nouveau bob dans le dictionnaire
        else:
            return -1   
        
    def attack(self,target)->None:pass
