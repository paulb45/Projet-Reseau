from collections import defaultdict
import random

import logic.bob
import logic.food

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import *

class Grid():
    def __init__(self):
        self.map=defaultdict(lambda:[])
    
    def get_position(self,obj) -> tuple:
        """ la fonction get_position permet de donner la position dans la grille d'un objet passe en parametres
        """
        for key, itms in self.map.items():
            for itm in itms:
                if id(itm) == id(obj):
                    return key  # Retourne les coordonnées (x, y) d'objet recherché
    
    def get_items(self,pos) -> list:
        """ Retourne la liste des objets à la clé (x, y), ou une liste vide s'il n'y a pas d'objet à cet endroit
        """
        return self.map[pos]
    
    def has_object(self, obj, pos):
        for item in self.get_items(pos):
            if isinstance(item, type(obj)):
                return item
        return False
        
    def has_bob(self, pos) -> bool:
        return self.has_object(logic.bob.Bob(), pos)
    
    def has_food(self, pos) -> bool:
        return self.has_object(logic.food.Food(), pos)
    
    def choose_random_tile(self):
        return random.randint(0, Config.width_map-1), random.randint(0, Config.height_map-1)
    
    def destroy_object(self,obj, pos=None):
        """_Destroys the given object.__

        Args:
            obj (food / bob): 
        """
        if pos == None :
            pos = self.get_position(obj)
        if obj in self.map[pos]:
            self.map[pos].remove(obj)
            if self.map[pos] == []:
                del self.map[pos]
    
    def get_all_object_in_map(self, obj) -> dict:
        obj_dict=defaultdict(lambda:[])
        for pos, items in self.map.items():
            for item in items:
                if isinstance(item,type(obj)):
                    obj_dict[pos].append(item)
        return obj_dict
    
    def get_all_bobs(self):
        return self.get_all_object_in_map(logic.bob.Bob())
    
    def get_all_foods(self):
        return self.get_all_object_in_map(logic.food.Food())
    
    def is_pos_in_map(self, pos: tuple) -> bool:
        if 0<=pos[0]<=Config.width_map-1 and 0<=pos[1]<=Config.height_map-1:
            return True
        return False
    
    def destroy_all_foods(self):
        for coord, foods in self.get_all_foods().items():
            for food in foods:
                self.destroy_object(food, coord)

    def create_bob(self, pos: tuple, stats=None):
        if stats == None: bob = logic.bob.Bob()
        else: bob = logic.bob.Bob(*stats)
        self.map[pos].append(bob)
    
    def place_child(self, bob, pos: tuple):
        if self.is_pos_in_map(new_pos :=(pos[0]+1,pos[1])):
            self.map[new_pos].append(bob)
        else: self.map[(pos[0]-1, pos[1])].append(bob)
        
    def bobs_in_case(self, coord: tuple) -> list:
        if coord in self.map:
            return [i for i in self.map[coord] if isinstance(i, logic.bob.Bob)]
        else:
            return []  # or handle the case when coord is not in self.map

