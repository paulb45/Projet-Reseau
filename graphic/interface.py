import pygame
import graphic.isometric as isometric

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import *
import logic.bob
import logic.food

class Interface(pygame.Surface):
    """
        Interface est une surface contenant l'ensemble des éléments graphiques (l'ensemble des sprites) qui 
        concerne l'affichage du jeu.
        Elle est entièrement indépendante de la fenêtre !        
    """
    def __init__(self, size, flags=0):
        super().__init__(size, flags)
        self.font = pygame.font.SysFont('chalkduster.ttf', 40)
        self._images = {}
        self.ground = pygame.Surface(size)
        self.load_images()
        self.bob_border_thinkness = 2
        self.bob_image_border = self.calc_border_sprite(self.bob,self.bob_border_thinkness)
        
        self.generate_ground(self.grass_tile)

    # --- Chargement des sprites ---
    def load_images(self):
        """
            Charge les images nécessaires au jeu
        """
        self.tileset = self.load_image('Tileset.png')
        self.grass_tile = self.cut_in_image('Tileset.png', (pos_x_tile,pos_y_tile), (tileset_x_offset, tileset_y_offset))

        self.bob = self.load_sprite('bob.png')
        self.apple = self.load_sprite('food.png')
        self.apple = pygame.transform.scale_by(self.apple, 0.5)
    
    def scale_sprite(self, image: pygame.image) -> pygame.image:
        return pygame.transform.scale(image, (tile_size, int(tile_size * image.get_height() / image.get_width() )))

    def load_sprite(self, path: str) -> pygame.image:
        img = self.load_image(path)
        img = self.scale_sprite(img)
        return img

    def load_image(self, image_path: str) -> pygame.image:
        if image_path in self._images:
            return self._images[image_path]
        try:
            image = pygame.image.load(f"{sprite_path}{image_path}").convert_alpha()
            self._images[image_path] = image
            return image
        except pygame.error as e:
            print(f"Impossible de charger l'image '{image_path}': {e}")
            return None

    def cut_in_image(self, image_path: str, pos: tuple, offset: tuple) -> pygame.Surface:
        # Retourne l'image à la i ème ligne, j ème colonne  -> pos = (i, j)
        return self._images[image_path].subsurface(
                [
                    pos[0]*tile_size + offset[0], 
                    pos[1]*tile_size + offset[1], 
                    tile_size,
                    tile_size
                ]
            )

    # --- Placement des sprites ---
    
    def place_top_position(self, image: pygame.image, pos: tuple) -> tuple:
        pos[0] -= image.get_width()//2
        return pos

    def place_bottom_position(self, image: pygame.image, pos: tuple) -> tuple:
        pos = self.place_top_position(image, pos)
        pos[1] += tile_size/4 - image.get_height()
        return pos

    def get_middle_of_tile(self, pos: tuple) -> tuple:
        # Retourne le milieu de la face supérieur, pas le milieu géométrique de l'image !
        pos += tile_size/2, tile_size/4
        return pos
    
    def place_entity(self, sprite: pygame.sprite, pos: tuple):
        """
            Place une entité à partir des coordonnées cartésiens sur la case adéquat.
            Place le bas sur le milieu de la tile.
        """
        pos_iso = isometric.cart_to_iso(pos)
        foot_pos = self.place_bottom_position(sprite, pos_iso)
        self.blit(sprite, isometric.iso_to_print(foot_pos))

    def place_tile(self, tile: pygame.image, pos: tuple):
        pos_iso = isometric.cart_to_iso(pos)
        self.ground.blit(tile, self.place_top_position(tile, isometric.iso_to_print(pos_iso)))
    
    def print_ground(self):
        self.blit(self.ground, (0,0))

    def print_food(self, map):
        for key, l in map.items():
            for item in l:
                if isinstance(item, logic.food.Food):
                    self.place_entity(self.apple, key)
    
    def print_bobs(self):
        for bob_info in self._bobs_infos:
            incremente_dep = [0,0]
            for i in range(len(bob_info["buffer_dep"])):
                bob_info["buffer_dep"][i] += bob_info["unit_dep"][i]
                if abs(bob_info["buffer_dep"][i])>=1:
                    # Update des buffers
                    incremente_dep[i] = int(bob_info["buffer_dep"][i])
                    bob_info["buffer_dep"][i] -= incremente_dep[i]
                    
                    bob_info["start_coords"][i] += incremente_dep[i]
            self.place_entity(bob_info["image"], (bob_info["start_coords"][0], bob_info["start_coords"][1]))
    
    """
    def move_bobs(self, map, current_tick):
        bobs_list = self.get_all_bobs(map)      
        for key, bob in bobs_list:
            # Calcul de l'incrément de déplacement sur le prochain tick
            new_x_tick = int(bob.last_move[0] * (1- current_tick/ max_framerate))
            new_y_tick = int(bob.last_move[1] * (1- current_tick/ max_framerate))
            new_pos = (key[0] - new_x_tick, key[1] - new_y_tick)
            #bob_with_border = self.apply_bob_border(bob)
            self.place_entity(self.bob, new_pos) 
    """    
    
    # --- Génération ---
    
    def generate_ground(self, tile: pygame.image):
        print(Config.width_map, Config.height_map)
        for i in range(Config.width_map):
            for j in range(Config.height_map):
                self.place_tile(tile, (i,j))
        self.print_ground()
        
    def bob_tick_unit(self, bob):
        return [bob.last_move[0] * 1/ max_framerate,
                bob.last_move[1] * 1/ max_framerate]

    def generate_map(self, map): # Renommer en add_text et arrêter la regénération de la map dedans ?
        for key, l in map.items():
            # Setup du comptage
            food_count = 0
            bob_count = 0
            for item in l:
                if isinstance(item, logic.bob.Bob): bob_count += 1
                else: food_count += 1
            if bob_count: self.place_entity(self.bob, key)
            if food_count: self.place_entity(self.apple, key)
            # Ajoue du texte
            """
            if (bob_count > 1) or (food_count > 1):
                text_count = self.font.render(f'[{bob_count};{food_count}]', True, (0, 255, 0))
                text_count.get_rect().center = (0,0)
            """

    def render_game(self, map):
        self.print_ground()
        self.print_food(map)
        self.print_bobs()
        #self.generate_map(map)
    
    # --- Gestion du liseré ---
    
    def calc_border_sprite(self, image: pygame.image, border_thickness) -> list:
        border_coords = []
        #pixels = pygame.PixelArray(image_copy)
        for x in range(image.get_width()):
            for y in range(image.get_height()):
                pixel = image.get_at((x,y))
                # Vérifiez si le pixel est transparent et s'il a un voisin non transparent
                if pixel == (0, 0, 0, 0) and any(
                        0 <= i < image.get_width() and 0 <= j < image.get_height() and image.get_at((i,j)) != (0, 0, 0, 0)
                        for i in range(x - border_thickness, x + border_thickness + 1)
                        for j in range(y - border_thickness, y + border_thickness + 1)
                    ):
                    border_coords.append((x,y))
        return border_coords
    
    def apply_border(self, image: pygame.image, color: tuple, coords: tuple, border_thickness) -> pygame.image :
        """
        Applique un liserai de couleur à une image
        """
        image_copy = image.copy()
        # Appliquez le liseré bleu autour du personnage avec l'épaisseur spécifiée
        for coord in coords:
            x,y = coord[0], coord[1]
            for i in range(max(0, x - border_thickness), min(image_copy.get_width(), x + border_thickness + 1)):
                for j in range(max(0, y - border_thickness), min(image_copy.get_height(), y + border_thickness + 1)):
                    image_copy.set_at((x, y), pygame.Color(color[0], color[1], color[2]))
        return image_copy

    def apply_bob_border(self, bob) -> pygame.image:
        health_ratio = abs( bob.get_E() / bob.get_Emax())
        red = int((1 - health_ratio) * 255)
        green = int(health_ratio * 255)
        blue = 0
        #print( red, green, abs(green), blue , bob.get_E(), bob.get_Emax() , health_ratio)
        #bob.get_E afin d'avoir une interface fonctionnelle pour l'instant je passe les valeurs absolu mais il faudra voir a corriger get_E
        bob_with_border = self.apply_border(self.bob, (red, green, blue), self.bob_image_border, self.bob_border_thinkness)
        return bob_with_border
    
    # --- Autre ---

    def place_interface_in_middle(self, window):
        """
            Place le centre de la carte au centre de la fenêtre
        """
        window_center = (window_size[0] // 2, window_size[1] // 2)
        interface_center = (screen_size[0] // 2, screen_size[1] // 2)
        offset_to_place = (window_center[0] - interface_center[0], window_center[1] - interface_center[1])
        window.blit(self, offset_to_place)       
    
    
    def get_all_bobs(self, map) -> list:
        bobs_list = []
        for key, l in map.items():
            for item in l:
                if isinstance(item, logic.bob.Bob):
                    bobs_list.append([key, item])
        return bobs_list
    
    def init_values_bob_day(self, coord, bob):
        bob_attribs = {}
        bob_attribs["start_coords"] = [coord[0]-bob.last_move[0], coord[1]-bob.last_move[1]]
        bob_attribs["unit_dep"] = self.bob_tick_unit(bob)
        bob_attribs["image"] = self.apply_bob_border(bob)
        bob_attribs["buffer_dep"] = [0,0]
        return bob_attribs
        
    def init_values_bobs_day(self, map):
        self._bobs_infos = []
        for coord, bob in self.get_all_bobs(map):
            self._bobs_infos.append(self.init_values_bob_day(coord, bob))
            
