import time
import  grid ,food
from bob import Bob
from food import Food
import random

#var test bob 
speed = 1
mass = 10
E = 100
speed_buff=1

class Game():
    def __init__(self,quantity_food,init_energy_food,nb_tick_day,P0,grid,nb_day):
        self.init_quantity_food=quantity_food
        self.init_energy_food=init_energy_food
        self.init_nb_tick_day=nb_tick_day
        self.P0=P0 #nombre des bobs a initialiser
        self.grid=grid
        self.nb_day=nb_day
        
    def get_quantity_food(self):
        return self.init_quantity_food
    
    def get_nb_tick_day(self):
        return self.init_nb_tick_day
    
    def get_P0(self):
        return self.P0
    
    def get_grid(self):
        return self.grid
    
    def get_nb_day(self):
        return self.nb_day
    
    def set_quantity_food(self, nv_quantity_food):
        self.init_quantity_food = nv_quantity_food
    
    def set_nb_tick_day(self, nv_nb_tick_day):
        self.init_nb_tick_day = nv_nb_tick_day
    
    def set_P0(self, nv_P0):
        self.P0 = nv_P0
    
    def set_grid(self, nv_grid):
        self.grid = nv_grid
    
    def set_nb_day(self, nv_nb_day):
        self.nb_day = nv_nb_day 
    
    def init_bobs(self):
        """init bob
        
        """
        for i in range(self.P0):
            x, y = random.randint(0, self.grid.N-1), random.randint(0, self.grid.M-1) 
            
            name= Bob( speed, mass, E, speed_buff)
            name.set_last_move((x,y))
            #f grid drtiha comme une liste ohna drtiha comme un dict
            if (x, y) not in self.grid.map:
                self.grid.map[(x, y)] = []
            self.grid.map[(x,y)].append(name)
               
    
    def spawn_food(self):
        """generer la nouritures

        Args:
            position (_type_): _description_
        """
        for i in range(self.get_quantity_food()):
            x, y = random.randint(0, self.grid.N-1), random.randint(0, self.grid.M-1)
            if (x, y) not in self.grid.map:
                self.grid.map[(x, y)] = []
            self.grid.map[x,y].append(Food(self.init_energy_food)) 
        
    def bob_play(self):
        # tuer le bob si n as pas de l'energie sinon move
        copy_dict=dict(self.grid.map)
        for coords ,bobs in copy_dict.items():
            for bob in bobs:
                print(bob)
                if isinstance(bob,Bob):
                    print("hello") 
                    position = self.grid.get_position(bob)
                    
                    
                    nb_bobs,nb_foods,bobs,foods=self.count(position[0],position[1])
            #*******************deplacement section **********************#       
                    #s'il y a encore de la nourriture bob reste immobile
                    #Eb-=.5
                    print(nb_bobs)
                    if(nb_foods>0):
                        bob.set_E(bob.get_E()-0.5)
                    #sinon il se déplace    
                    else:
                        #bob choisi aléaroirement un mouvement parmis les mouvement dispo
                        available_positions = self.grid.scan_around(position, bob.speed)
                        mouvement=bob.move(available_positions)
                        print(mouvement)
                        self.grid.map[tuple(position)].remove(bob) #suppression de la dernière position
                        if tuple(mouvement) not in self.grid.map:
                            self.grid.map[tuple(mouvement)] = []
                        self.grid.map[tuple(mouvement)].append(bob) #ajouter le bob pour la nouvelle position 
                         #ici bob il a bien reussi son move
            #*********************eating section***************************#             
                        #s'il y a plus qu'un bob dans la nouvelle case un seul qui va manger la nourriture
                        """if(nb_bobs==1 and nb_foods>0):
                            eat=bob.eat()"""
                    
                
    def destroy_object(obj):
        """_Destroys the given object.__

        Args:
            obj (food / bob): 
        """
        del obj
        
    def day_play(self):
        """chaque jour d=100 ticks
           chaque jours f=200 points de nourriture
           Ef=100 energie de la nourriture
        """
        tick=self.set_nb_tick_day(self.nb_tick_day)
        fd_quantity=self.set_quantity_food(self.get_quantity_food)
        
        
        while tick>0:
            
            tick-=1
            time.sleep(1)
    def create_bob(self,Bob, x,y):
        self.grid.map[(x,y)].append(Bob)
    
    def count(self,x,y)->list:
        """count et return les bobs et les foods d'une case données _

        Args:
            x (int):coord x
            y (int):coord y

        Returns:
            list:nb_bobs,nb_foods,bobs,foods
        """
        nb_bobs,nb_foods=0,0
        bobs=[]
        foods=[]
        if (x, y) not in self.grid.map: return [0,0]
        
        for elt in self.grid.map[(x,y)]:
           
                if(isinstance(elt,Bob)):
                    nb_bobs+=1
                    bobs.append(elt)
                elif(isinstance(elt,Food)):
                    if(elt.get_energy()>0): 
                        nb_foods+=1
                        foods.append(elt)
        return [nb_bobs,nb_foods,bobs,foods]            
