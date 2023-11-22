from Food import Food
import random as rd 
class Bob():
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
    @classmethod    
    def set_Emother(cls,E):
        cls.Emother=E
    @classmethod        
    def set_Echild(cls,E):
        cls.Echild=E    
    def move(self,dict)->tuple:
        """Déplace Bob en choisissant aléatoirement une direction (horizontale ou verticale) pour éviter les mouvement en diagonal
           au moment du mouvement s'il trouve du food il va la manger s'il trouve un autre bob il va l'attaquer 

        Args:
            dict :"coord":les objets qui se trouvent dans ces coord (BOB,FOOD) 
        Returns:
            tuple: les nouveaux coordonnées(x,y)
        """
        choix=rd.choice(['horizontal','vertical'])
        if(choix=='horizontal'):
            coord=(rd.randint(-self.speed,self.speed+1),0)
        else:
            coord=(0,rd.randint(-self.speed,self.speed+1))    
        self.last_move[0]+=coord[0]
        self.last_move[1]+=coord[1]
        for i in dict[self.last_move]:
            if(isinstance(Bob,i)):self.attack(i)
            if(isinstance(Bob,i)):self.eat(i)
        return coord
        

    def eat(self,food: Food)->None:
        """Fait en sorte que BOB mange la nourriture spécifiée et augmente son énergie.

        Args:
            food (FOOD): la nourriture que bob va manger
        """
        self.E+=food.energy
        if(self.E>self.Emax):
            food.energy=self.E-self.Emax
            self.E=self.Emax
    def is_dead(self)->bool:
        """vérifie si Bob mort ou non

        Returns:
            bool: true si BOB est mort non sinon 
        """
        return self.E <=0
    def parthenogenesis(self):
        """_summary_
        """
        if(self.E>=self.Emax):
            self.E=self.Emax-self.Emother
            bebe_bob= Bob(self.speed,self.mass,self.Echild,self.speed_buff)
            bebe_bob.last_move=self.last_move 
    
    def attack(self,target)->None:pass
