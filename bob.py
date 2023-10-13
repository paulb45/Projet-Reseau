from Food import FOOD
import random as rd 
class BOB():
    Emax=200
    Emother=150
    Echild=50
    def __init__(self,speed,mass,E,speed_buff):
        self.speed=speed
        self.mass=mass
        self.memory=None
        self.E=E
        self.last_move=None
        self.speed_buff=speed_buff
    #getter
    def get_speed(self):
        return self.speed
    def get_mass(self):
        return self.mass
    def  get_memory(self):
        return self.memory
    def get_Emax(self):
        return self.Emax
    def get_E(self):
        return self.E
    def get_Emother(self):
        return self.Emother
    
    def get_last_move(self):
        return self.last_move
    def get_Echild(self):
        return self.Echild
    #setter
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
        
    def set_Emother(self,E):
        self.Emother=E    
    def set_Echild(self,E):
        self.Echild=E    
    def move(self,dict)->tuple:
        choix=rd.choice(['horizontal','vertical'])
        if(choix=='horizontal'):
            coord=(rd.randint(-self.speed,self.speed+1),0)
        else:
            coord=(0,rd.randint(-self.speed,self.speed+1))    
        self.last_move[0]+=coord[0]
        self.last_move[1]+=coord[1]
        for i in dict[self.last_move]:
            if(isinstance(BOB,i)):self.attack(i)
            if(isinstance(FOOD,i)):self.eat(i)
        return coord
        
    def eat(self,food: FOOD)->None:       
        self.E+=food.energy
        if(self.E>self.Emax):
            food.energy=self.E-self.Emax
            self.E=self.Emax
    def is_dead(self)->bool:
        self.E <=0
    def parthenogenesis():pass
    def attack(self,target):
        if(self.E==self.Emax):
            self.E=self.Emax-self.Emother
            bebe_bob= BOB(self.speed,self.mass,self.Echild,self.speed_buff)
            bebe_bob.last_move=self.last_move                                   