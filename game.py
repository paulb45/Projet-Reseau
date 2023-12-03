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
        positions_occupees=[] #pour stocker les positions qui sont deja occupées
        for i in range(self.P0):
            
            while True :
                x, y = random.randint(0, self.grid.N-1), random.randint(0, self.grid.M-1)
                if (x, y) not in positions_occupees:
                    break  # Sortez de la boucle si la position n'est pas occupée 
            bob= Bob( speed, mass, E, speed_buff)
            self.create_bob( bob, x, y)
            positions_occupees.append((x,y)) #ajouter la nouvelle position a la liste des positions occupees
               
    
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
                if isinstance(bob,Bob):
                    position = self.grid.get_position(bob)
                    nb_bobs,nb_foods,bobs,foods=self.count(position[0],position[1])
            #*******************deplacement section **********************#       
                    #s'il y a encore de la nourriture bob reste immobile
                    #Eb-=.5
                    if(nb_foods>0):
                        bob.set_E(bob.get_E()-0.5)
                    #sinon il se déplace    
                    else:
                        mouvement=bob.move(bob.speed)
                        #si bob sort de la grill, il meurt
                        if(mouvement[0]<0 or mouvement[0]>=self.grid.get_N() or mouvement[1]<0 or mouvement[1]>=self.grid.get_M()):
                            print("bob meur car il a sortie de la grille")
                            pass
                        self.grid.map[tuple(position)].remove(bob) #suppression de la dernière position
                        if tuple(mouvement) not in self.grid.map:
                            self.grid.map[tuple(mouvement)] = []
                        self.grid.map[tuple(mouvement)].append(bob) #ajouter le bob pour la nouvelle position 
                        print(position,mouvement)
                        #ici bob il a bien reussi son move
                         
            #*********************eating section***************************#             
                        #s'il y a plus qu'un bob dans la nouvelle case un seul qui va manger la nourriture
                        """if(nb_bobs==1 and nb_foods>0):
                            eat=bob.eat()"""
                                
                    if(len(foods)>0):

                        eating=bob.eat(foods[0])
                        print("eating: ",eating)
                        parthenogenesis=bob.parthenogenesis()
                        if(parthenogenesis!=-1):
                            self.grid.map[tuple(position)].append(parthenogenesis)
                        if(eating):
                            self.grid.map[self.grid.get_position(foods[0])].remove(foods[0])
                            foods.remove(foods[0])
                            
                            
    def destroy_object(self,obj):
        """_Destroys the given object.__

        Args:
            obj (food / bob): 
        """
        (x,y) = self.grid.get_position(obj)
        for element in self.grid.map[x,y]:
            if id(obj) == id(element) : 
                self.grid.map[(x, y)].remove(element)       
    def day_play(self):
        """chaque jour d=100 ticks
           chaque jours f=200 points de nourriture
           Ef=100 energie de la nourriture
        """
        tick = self.get_nb_tick_day()  #recupuration du nombre des ticks par jour
        fd_quantity = self.get_quantity_food()  #la quantite de la nourriture par jour
        self.init_bobs()    #Initialisation des bobs
        self.spawn_food()   #generation de la nourriture
        
        while tick>0:
            self.bob_play()
            tick-=1
            time.sleep(1)
        #supprimer tous les food qui restent
        copy_dict=dict(self.grid.map)
        for coords ,foods in copy_dict.items():
            for bob in foods:
                if isinstance(food,Food):
                    self.destroy_object(food)
    def create_bob(self,Bob, x,y):
        if (x, y) in self.grid.map:
            self.grid.map[(x, y)].append(Bob)
        else:
            self.grid.map[(x, y)] = [Bob]
        Bob.set_last_move([x,y])
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
