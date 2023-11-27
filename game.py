import time, random

from bob import Bob
from food import Food
from config import *

#var test bob 
speed = 1
mass = 10
E = 100
speed_buff=1

class Game():
    def __init__(self,quantity_food,init_energy_food,nb_tick_day,P0,grid,nb_day): # METTRE DES VALEURS PAR DEFAUTS, nb_day ??? c'est quoi
        self.init_quantity_food=quantity_food
        self.init_energy_food=init_energy_food
        self.init_nb_tick_day=nb_tick_day
        self.P0=P0 # nombre des bobs a initialiser -> CHANGER LE NOM DE LA VARIABLE SI C'EST PAS CLAIR POUR VOUS !!!
        self.grid=grid
        self.nb_day=nb_day

        # APPELER LES METHODES QUI SERONT LANCEES A LA CREATION DU JEU (init_bobs, ...)
        
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
            x, y = random.randint(0, N-1), random.randint(0, M-1) # La borne supérieur est comprise avec randint ?
            
            name= Bob( speed, mass, E, speed_buff)
            name.set_last_move((x,y))
            #f grid drtiha comme une liste ohna drtiha comme un dict
            # !!! POURQUOI ON A UNE FONCTION CREATE BOB ET ON NE L'APPEL PAS !!!
            if (x, y) not in self.grid.grid:
                self.grid.grid[(x, y)] = []
            self.grid.grid[(x,y)].append(name)
               
    
    def spawn_food(self):
        """generer la nouritures

        Args:
            position (_type_): _description_
        """
        for i in range(self.get_quantity_food()):
            x, y = random.randint(0, N-1), random.randint(0, M-1) # Meme remarque que à init_bobs
            if (x, y) not in self.grid.grid:
                self.grid.grid[(x, y)] = []
            self.grid.grid[x,y].append(Food(self.init_energy_food)) 
        
    def bob_play(self):
        # FONCTIONNE PAS
        # tuer le bob si n as pas de l'energie sinon move
        for bobs in self.grid.grid.items():
            for bob in bobs: 
                if isinstance(bob,Bob): #Vérification si bob est une instance de la classe BOB
                    # Pourquoi l'appeler bob avant de savoir si c'est un bob ?
                    position = self.grid.get_position(bob)
                    available_positions = self.grid.scan_around(position, bob.speed) #les places disponibles pour se déplacer 
                if available_positions: # Bizarre ça
                    # POURQUOI BOB PEUT FAIRE TOUTE LES ACTIONS ?! IL DOIT EN FAIRE QU'UNE SEULE
                    new_position = bob.move(self.grid.grid)
                    self.grid.grid[position].remove(bob) #suppression de la dernière position
                    self.grid.grid[new_position].append(bob) #ajouter le bob pour la nouvelle position
                    bob.set_last_move(new_position) #MAJ du dernier mouvement du bob

                    # bob.parthenogenesis()
                    
        
    def destroy_object(obj):
        """_Destroys the given object.__

        Args:
            obj (food / bob): 
        """
        del obj
        
    def day_play(self):
        # A IMPLEMENTER
        """chaque jour d=100 ticks
           chaque jours f=200 points de nourriture
           Ef=100 energie de la nourriture
        """
        tick=self.set_nb_tick_day(self.nb_tick_day) # pourquoi cette variable ? Pourquoi lui faire prendre exactement la même valeur qu'un truc qui existe déjà ?
        fd_quantity=self.set_quantity_food(self.get_quantity_food) # Pareil qu'au dessus
        
        
        while tick>0:
            
            tick-=1
            time.sleep(1) # A supprimer à la fin, sinon l'affichage graphique va pas aimer

    def create_bob(self,Bob, x,y):
        # FONCTIONNE PAS, KEYERROR quelque soit les valeurs x,y
        self.grid.grid[(x,y)].append(Bob)