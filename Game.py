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
            
            name= Bob( speed, mass, E, speed_buff)
            name.set_last_move((x,y))
            #f grid drtiha comme une liste ohna drtiha comme un dict
            if (x, y) not in self.grid.grid:
                self.grid.grid[(x, y)] = []
            self.grid.grid[(x,y)].append(name)
               
    
    def spawn_food(self):
        """generer la nouritures

        Args:
            position (_type_): _description_
        """
        for i in range(self.get_quantity_food()):
            x, y = random.randint(0, self.grid.N-1), random.randint(0, self.grid.M-1)
            if (x, y) not in self.grid.grid:
                self.grid.grid[(x, y)] = []
            self.grid.grid[x,y].append(Food(self.init_energy_food)) 
        
    def bob_play(self):
        for bobs in self.grid.grid.items():
            for bob in bobs: 
                if isinstance(bob,Bob):
                    position = self.grid.get_position(bob)
                    ## tuer le bob si n as pas de l'energie sinon move
                    if (bob.is_dead()):
                        self.grid.grid[position].remove(bob)
                        
                    else:
                        nb_bobs,nb_foods,bobs,foods=self.count(position[0],position[1])
                        #s'il y a encore de la nourriture bob reste immobile
                        if(nb_foods>0):
                            bob.set_E(bob.get_E()-0.5)
                        #sinon il se déplace    
                        else:
                            #bob choisi aléaroirement un mouvement parmis les mouvement dispo
                            available_positions = self.grid.scan_around(position, bob.speed)
                            mouvement=bob.move()
                            while mouvement not in available_positions:
                                mouvement=bob.move()
                            self.grid.grid[position].remove(bob) #suppression de la dernière position
                            self.grid.grid[mouvement].append(bob) #ajouter le bob pour la nouvelle position 
                            #ici bob il a bien reussi son mouve
                            #s'il y a plus qu'un bob dans la nouvelle case un seul qui va manger la nourriture
                            if(nb_bobs==1 and nb_foods>0):
                                eat=bob.eat()
                    """" 
                if available_positions:
                    new_position = bob.move(self.grid.grid)
                    bob.parthenogenesis()
                    self.grid.grid[position].remove(bob) #suppression de la dernière position
                    self.grid.grid[new_position].append(bob) #ajouter le bob pour la nouvelle position
                    bob.set_last_move(new_position) #MAJ du dernier mouvement du bob
        """
                #if(count())
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
        self.grid.grid[(x,y)].append(Bob)
    
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
        if (x, y) not in self.grid.grid: return [0,0]
        for elt in self.grid.grid[(x,y)]:
            for e in elt:
                if(isinstance(elt,Bob)):
                    nb_bobs+=1
                    bobs.append(elt)
                elif(isinstance(elt,Food)): 
                    nb_foods+=1
                    foods.append(elt)
        return [nb_bobs,nb_foods,bobs,foods]            
