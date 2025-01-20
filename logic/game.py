import sys, os
from threading import Thread
from random import randint
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import *

from logic.bob import Bob
from logic.food import Food
from logic.grid import Grid

from network.listener import startlisten
from network.action_buffer import ActionBuffer
from network.pytoc_sender import send_bob
from network.network_property import Network_property

class Game():
    def __init__(self):
        # TODO prévoir la cohérence en cas de deux id identiques
        self.player_id = randint(0, 100000)

        self.grid = Grid(player_id=self.player_id)

        if not Config.singleplayer: # TODO si on est en solo / multi ?
            # Initialisation de l'écoute réseau
            self.network_thread = Thread(target=startlisten)
            self.network_thread.start()

        self.init_bobs()
        self.spawn_food()

        if Config.hosting : #Si on host, on doit setup toutes les cases des networks-property comme étant à nous.
                Network_property.init_np_grid(self.grid)

    
    def init_bobs(self):
        """init bob
            initialisation des P0 bobs dans exactement P0 places
        """
        for _ in range(Config.P0):
            is_spawn = False
            while not is_spawn :
                pos = self.grid.choose_random_tile()
                if not self.grid.has_bob(pos):
                    is_spawn = True
            self.grid.create_bob(pos)
          
    def spawn_food(self):
        """generer la nouritures
        """
        for _ in range(Config.quantity_food):
            pos = self.grid.choose_random_tile()
            self.grid.map[pos].append(Food(local=True, player_id=self.player_id))

    def bob_play_tick(self, bob: Bob, pos=None):
        if pos == None:
            pos = self.grid.get_position(bob)
        if bob.get_E() == Bob.get_Emax():
            self.grid.place_child(bob.parthenogenesis(), pos)          
        elif (food := self.grid.has_food(pos)):
            if bob.eat(food):
                self.grid.destroy_object(food, pos)
            
        else:
            mouv = bob.move()
            new_pos = pos[0] + mouv[0], pos[1] + mouv[1]
            if self.grid.is_pos_in_map(new_pos):
                self.grid.map[new_pos].append(bob)
                self.grid.destroy_object(bob, pos)
                if (food := self.grid.has_food(new_pos)):
                    bob.E += 0.5 # Compence l'effet de manger juste après
                    if bob.eat(food):
                        self.grid.destroy_object(food, new_pos)
                if bob.is_dead():
                    self.grid.destroy_object(bob, new_pos)
                else:
                    bobs=self.grid.bobs_in_case(new_pos)
                    for target in bobs :
                        if bob.attack(target):
                            self.grid.destroy_object(target,new_pos)
                            break
            else: self.grid.destroy_object(bob, pos)

    def reset_bobs_last_move(self):
        bobs_map = self.grid.get_all_bobs()
        for _, bobs in bobs_map.items():
            for bob in bobs:
                bob.reset_last_move()

    def bobs_play_day(self):
        bobs_map = self.grid.get_all_bobs()
        for pos, bobs in bobs_map.items():
            for bob in bobs:
                if bob.is_local():
                    self.bob_play_tick(bob, pos)
                    send_bob(pos, bob)


    def network_day(self):
        """Toutes les actions sur le jeu pour les items du réseau
        """
        # Déplacement des Bobs
        network_buffer = ActionBuffer.get_buffer_move()
        for item_id, pos in network_buffer.items():
            # vérifier si le bob n'est pas local
            if self.player_id != int(item_id // 10**10):
                info = self.grid.get_item_by_id(item_id)

                # le Bob n'est pas connu en local
                if info is None: 
                    print(f"Création de Bob -> {item_id}")
                    bob = Bob(local=False, bob_id=item_id)
                    bob.set_last_move((pos[0][0] - pos[1][0], pos[0][1] - pos[1][1])) # TODO à vérif
                    self.grid.map[pos[1]].append(bob)

                # le Bob est connu en local
                else:
                    local_pos, bob = info
                    bob.set_last_move((local_pos[0] - pos[1][0], local_pos[1] - pos[1][1])) # TODO à vérif
                    self.grid.map[pos[1]].append(bob)
                    self.grid.destroy_object(bob, local_pos)
                    

    def day_play(self):
        self.reset_bobs_last_move()
        self.bobs_play_day()
        self.grid.destroy_all_foods()
        self.spawn_food()

        if not Config.singleplayer:
            self.network_day()