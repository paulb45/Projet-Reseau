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
from network.pytoc_sender import send_DPL, send_PLC, send_DSP, send_ATK
from network.network_property import Network_property

class Game():
    def __init__(self, listen_port=None, sending_port=None):
        self.sending_port = sending_port
        # TODO prévoir la cohérence en cas de deux id identiques
        self.player_id = randint(0, 100000)

        self.grid = Grid(player_id=self.player_id)

        if not Config.singleplayer: # TODO si on est en solo / multi ?
            # Initialisation de l'écoute réseau
            self.network_thread = Thread(target=startlisten, args=["127.0.0.1", listen_port])
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
            bob = self.grid.create_bob(pos)
            send_PLC(pos, bob, self.sending_port)

    def spawn_food(self):
        """generer la nouritures
        """
        for _ in range(Config.quantity_food):
            pos = self.grid.choose_random_tile()
            food = Food(local=True, player_id=self.player_id)
            self.grid.map[pos].append(food)
            send_PLC(pos, food, self.sending_port)

    def bob_play_tick(self, bob: Bob, pos=None):
        if pos == None:
            pos = self.grid.get_position(bob)
        if bob.get_E() == Bob.get_Emax():
            child = bob.parthenogenesis()
            self.grid.place_child(child, pos)
            send_PLC(pos, bob, self.sending_port)
        elif (food := self.grid.has_food(pos)):
            if bob.eat(food):
                self.grid.destroy_object(food, pos)
                send_DSP(food, pos, self.sending_port)
            
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
                        send_DSP(food, new_pos, self.sending_port)
                if bob.is_dead():
                    self.grid.destroy_object(bob, new_pos)
                    send_DSP(bob, new_pos, self.sending_port)
                else:
                    bobs=self.grid.bobs_in_case(new_pos)
                    for target in bobs :
                        if bob.attack(target):
                            self.grid.destroy_object(target,new_pos)
                            send_ATK(bob, new_pos, target, self.sending_port)
                            send_DSP(target, new_pos, self.sending_port)
                            break
            else: 
                self.grid.destroy_object(bob, pos)
                send_DSP(bob, pos, self.sending_port)

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
                    send_DPL(pos, bob, self.sending_port)
                else:
                    # si le bob n'a pas été vu depuis plus de 10 jours local, on le vire
                    if bob.get_nb_day_not_view() >= 10:
                        self.grid.destroy_object(bob, pos)
                    else:
                        bob.add_nb_day_not_view(1)


    def network_day(self):
        """Toutes les actions sur le jeu pour les items du réseau
        """
        # Placement des items
        for item_id, infos in ActionBuffer.get_buffer_placement().items():
            # vérifier si l'item n'est pas local
            if self.player_id != int(item_id // 10**10):
                # si bob
                if infos[1] == 'B':
                    bob = Bob(E=infos[2], speed=infos[4], mass=infos[3], local=False, bob_id=item_id)
                    self.grid.map[infos[0]].append(bob)

                # si food
                elif infos[1] == 'F':
                    food = Food(energy=infos[2], local=False, food_id=item_id)
                    self.grid.map[infos[0]].append(food)

        # Déplacement des Bobs
        for item_id, pos in ActionBuffer.get_buffer_move().items():
            # vérifier si le bob n'est pas local
            if self.player_id != int(item_id // 10**10):
                info = self.grid.get_item_by_id(item_id, pos)
                bob = None

                # le Bob n'est pas connu en local
                if info is None: 
                    bob = Bob(local=False, bob_id=item_id)
                    bob.set_last_move((pos[1][0] - pos[0][0], pos[1][1] - pos[0][1]))
                    self.grid.map[pos[1]].append(bob)

                # le Bob est connu en local
                else:
                    local_pos, bob = info
                    bob.set_last_move((pos[1][0] - local_pos[0], pos[1][1] - local_pos[1]))
                    self.grid.map[pos[1]].append(bob)
                    self.grid.destroy_object(bob, local_pos)
                    bob.reset_nb_day_not_view()

                # consommation du bob
                bob.add_E(-0.5 * bob.get_mass() * bob.get_speed()**2)

                # vérification de l'énergie du bob (est-il mort ?)
                if bob.is_dead():
                    self.grid.destroy_object(bob, pos[1])

        # Manger
        for item_id, info in ActionBuffer.get_buffer_eat().items():
            bob = self.map.get_item_by_id(item_id, info[0])

            if bob is not None:
                bob.add_E(info[1])
                bob.reset_nb_day_not_view()

                food = self.map.get_item_by_id(item_id, info[2])
                if food is not None: 
                    food.set_energy(food.get_energy - info[0])

        # Attaque
        for item_id, info in ActionBuffer.get_buffer_attack().items():
            item_attack = self.grid.get_item_by_id(item_id, info[0])
            item_target = self.grid.get_item_by_id(info[1], info[0])

            if (item_attack is not None) and (item_target is not None):
                item_attack[1].attack(item_target[1])

        # Disparition d'un item
        for item_id, pos in ActionBuffer.get_buffer_dead().items():
            # Récupération de l'instance de notre item
            # 1 - avec la position
            items = [item for item in self.grid.get_items(pos) if item.get_id() == item_id]
            if items != []:
                self.grid.destroy_object(items[0], pos)
            # 2 - sans la position
            else:
                item = self.grid.get_item_by_id(item_id)
                if item is not None:
                    self.grid.destroy_object(item[1], item[0])


    def day_play(self):
        self.reset_bobs_last_move()
        self.bobs_play_day()
        self.grid.destroy_all_foods()
        self.spawn_food()

        if not Config.singleplayer:
            self.network_day()