import grid, food, bob
import random

class Game():
    def __init__(self,quantity_food,nb_tick_day,P0,grid,nb_day):
        self.quantity_food=quantity_food
        self.nb_tick_day=nb_tick_day
        self.P0=P0 #nombre des bobs a initialiser
        self.grid=grid
        self.nb_day=nb_day
    def get_quantity_food(self):
        return self.quantity_food
    def get_nb_tick_day(self):
        return self.nb_tick_day
    def get_P0(self):
        return self.P0
    def get_grid(self):
        return self.grid
    def get_nb_day(self):
        return self.nb_day
    def set_quantity_food(self, nv_quantity_food):
        self.quantity_food = nv_quantity_food
    def set_nb_tick_day(self, nv_nb_tick_day):
        self.nb_tick_day = nv_nb_tick_day
    def set_P0(self, nv_P0):
        self.P0 = nv_P0
    def set_grid(self, nv_grid):
        self.grid = nv_grid
    def set_nb_day(self, nv_nb_day):
        self.nb_day = nv_nb_day 
    def init_bobs(self):
        for i in range(self.P0):
            x, y = random.randint(0, self.grid.N-1), random.randint(0, self.grid.M-1) 
            name = f"Bob{i + 1}" #nommer "Bob1" "Bob2" ...
            name= bob()
            self.grid.tiles[(x,y)].append(name)    
    def spawn_food(self, position):
        x,y = position
        if 0 <= x < self.N and 0 <= y < self.M:
            food = food.Food()
            self.grid.tiles[(x,y)].append(food)
    def bob_paly():
        pass
    def destroy_object(obj):
        pass
    def day_play():
        pass
    def create_bob(self,Bob, x,y):
        self.grid.tiles[(x,y)].append(Bob)