import time
import  Grid ,Food
from bob import Bob
from Food import Food
import random
#var test bob 
speed = 1
mass = 10
E = 100
speed_buff=1

class GAME():
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
            name = f"Bob{i + 1}" #nommer "Bob1" "Bob2" ...
            name= Bob( speed, mass, E, speed_buff)
            name.set_last_move((x,y))
            self.grid.tiles[(x,y)].append(name)
               
    
    def spawn_food(self):
        """generer la nouritures

        Args:
            position (_type_): _description_
        """
        for i in range(self.get_quantity_food):
            x, y = random.randint(0, self.grid.N-1), random.randint(0, self.grid.M-1)  
            self.grid.tiles[(x,y)].append(Food(self.init_energy_food)) 
        
    def bob_play(self):
        for bobs in self.grid.tiles.items():
            for bob in bobs: 
                if isinstance(bob,Bob): #Vérification si bob est une instance de la classe BOB
                    position = self.grid.get_position(bob)
                    available_positions = self.grid.scan_around(position, bob.speed) #les places disponibles pour se déplacer 
                if available_positions:
                    new_position = bob.move(self.grid.tiles)
                    self.grid.tiles[position].remove(bob) #suppression de la dernière position
                    self.grid.tiles[new_position].append(bob) #ajouter le bob pour la nouvelle position
                    bob.set_last_move(new_position) #MAJ du dernier mouvement du bob
        
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
        
        for nourriture in self.get_quantity_food():
            #deposer l'objet dans la grille
            #plusieur nourriture peuvent se trouver dans la meme case 
            pos_x=random.randint(self.grid.get_M)
            pos_y=random.randint(self.grid.get_N)
            self.spawn_food((pos_x,pos_y)) 
        while tick>0:
            
            tick-=1
            time.sleep(1)
    def create_bob(self,Bob, x,y):
        self.grid.tiles[(x,y)].append(Bob)