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
        self.bob_border_thinkness = 1
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
        self.bob_with_border = self.load_sprite_with_halo(self.bob, 10)
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

    def print_food(self, grid):
        for key, foods in grid.get_all_foods().items():
            for food in foods:
                self.place_entity(self.apple, key)
    """
    def print_bobs(self):
        for bob_info in self._bobs_infos:
            incremente_dep = [0,0]
            for i in range(len(bob_info["buffer_dep"])):
                bob_info["buffer_dep"][i] += bob_info["unit_dep"][i]
                #print(bob_info["buffer_dep"][i])
                if abs(bob_info["buffer_dep"][i]) - 0.999 >= 0: # Check comparaison proche de 0
                    # Update des buffers
                    incremente_dep[i] = int(bob_info["buffer_dep"][i])
                    bob_info["buffer_dep"][i] -= incremente_dep[i]
                    
                    bob_info["start_coords"][i] += incremente_dep[i]
            self.place_entity(bob_info["image"], (bob_info["start_coords"][0], bob_info["start_coords"][1]))
    """
    
    def move_bob(self, end_coord, last_move, bob_sprite, current_tick):
        # Calcul de l'incrément de déplacement sur le prochain tick
        new_x_tick = last_move[0] * (1- current_tick/ max_framerate)
        new_y_tick = last_move[1] * (1- current_tick/ max_framerate)
        new_pos = (end_coord[0] - new_x_tick, end_coord[1] - new_y_tick)
        self.place_entity(bob_sprite, new_pos) 
    
    def move_bobs(self, current_tick):
        for bob_info in self._bobs_infos:
            self.move_bob(bob_info["end_coords"], bob_info["last_move"], bob_info["image"], current_tick)

       
    
    # --- Génération ---
    
    def generate_ground(self, tile: pygame.image):
        for i in range(Config.width_map):
            for j in range(Config.height_map):
                self.place_tile(tile, (i,j))
        self.print_ground()
        
    def bob_tick_unit(self, bob):
        x_tick = round(bob.last_move[0] * 1/ max_framerate, 3) + 0.001
        y_tick = round(bob.last_move[1] * 1/ max_framerate, 3) + 0.001
        return [x_tick, y_tick]

    """
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
            
            if (bob_count > 1) or (food_count > 1):
                text_count = self.font.render(f'[{bob_count};{food_count}]', True, (0, 255, 0))
                text_count.get_rect().center = (0,0)
            
    """

    def render_game(self, grid, current_tick):
        self.print_ground()
        self.print_food(grid)
        self.move_bobs(current_tick)
        
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

    def choose_bob_border(self, bob) -> pygame.image:
        health_ratio = bob.get_E() / bob.get_Emax() * 100
        if health_ratio <= 20: return self.bob_with_border["20%"]
        elif health_ratio <= 40: return self.bob_with_border["40%"]
        elif health_ratio <= 60: return self.bob_with_border["60%"]
        elif health_ratio <= 80: return self.bob_with_border["80%"]
        else: return self.bob_with_border["100%"] 
    
    def load_sprite_with_halo(self, image: pygame.image, border_thickness):
        sprite_border = self.calc_border_sprite(self.bob, border_thickness)
        return {
            "100%" : self.apply_border(image, (0,255,0), sprite_border, border_thickness),
            "80%" : self.apply_border(image, (55,200,0), sprite_border, border_thickness),
            "60%" : self.apply_border(image, (128,127,0), sprite_border, border_thickness),
            "40%" : self.apply_border(image, (200,50,0), sprite_border, border_thickness),
            "20%" : self.apply_border(image, (255,0,0), sprite_border, border_thickness)
        }
    
    # --- Autre ---

    def place_interface_in_middle(self, window):
        """
            Place le centre de la carte au centre de la fenêtre
        """
        window_center = (window_size[0] // 2, window_size[1] // 2)
        interface_center = (Config.screen_size[0] // 2, Config.screen_size[1] // 2)
        offset_to_place = (window_center[0] - interface_center[0], window_center[1] - interface_center[1])
        window.blit(self, offset_to_place)       
    
    """
    def init_values_bob_day(self, coord, bob):
        bob_attribs = {}
        bob_attribs["start_coords"] = [coord[0]-bob.last_move[0], coord[1]-bob.last_move[1]]
        bob_attribs["unit_dep"] = self.bob_tick_unit(bob)
        bob_attribs["image"] = self.choose_bob_border(bob)
        bob_attribs["buffer_dep"] = [0,0]
        return bob_attribs
    """
    def init_values_bob_day(self, coord, bob):
        bob_attribs = {}
        bob_attribs["end_coords"] = coord
        bob_attribs["last_move"] = bob.last_move
        bob_attribs["image"] = self.choose_bob_border(bob)
        return bob_attribs


        
    def init_values_bobs_day(self, grid):
        self._bobs_infos = []
        for coord, bobs in grid.get_all_bobs().items():
            for bob in bobs:
                self._bobs_infos.append(self.init_values_bob_day(coord, bob))
