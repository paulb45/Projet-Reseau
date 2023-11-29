import pygame
import graphic.isometric as isometric

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import *

class Interface(pygame.Surface):
    """
        Interface est une surface contenant l'ensemble des éléments graphiques (l'ensemble des sprites) qui 
        concerne l'affichage du jeu.
        Elle est entièrement indépendante de la fenêtre !        
    """
    def __init__(self, size, flags=0):
        super().__init__(size, flags)
        self._images = {}
        self.load_images()
        
        self.generate_ground(self.grass_tile)

    # --- Chargement des sprites ---
    def load_images(self):
        """
            Charge les images nécessaires au jeu
        """
        self.tileset = self.load_image('Tileset.png')
        self.grass_tile = self.cut_in_image('Tileset.png', (0,0))

        self.bob = self.load_sprite('crusader_idle_00000.png')
        self.apple = self.load_sprite('apple.png')
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

    def cut_in_image(self, image_path: str, pos: tuple) -> pygame.Surface:
        # Retourne l'image à la i ème ligne, j ème colonne  -> pos = (i, j)
        return self._images[image_path].subsurface(
                [
                    pos[0]*tile_size + tileset_x_offset, 
                    pos[1]*tile_size + tileset_y_offset, 
                    (pos[0]+1)*tile_size + tileset_x_offset,
                    (pos[1]+1)*tile_size + tileset_y_offset
                ]
            )

    # --- Placement des sprites ---
    def place_top_position(self, pos: tuple) -> tuple:
        pos[0] -= tile_size/2
        return pos

    def place_bottom_position(self, image: pygame.image, pos: tuple) -> tuple:
        pos = self.place_top_position(pos)
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
        
    def move_sprite(self, sprite, old_map, new_map):
        # Chercher la position du bob sur l'old map
        # Chercher la position de ce même bob sur la new map
        # Calcul des coordonées en iso pour les deux
        # Calcul de l'écart
        # En déduire la vitesse sur x et sur y pour l'incrémenter
        # Faire le déplacement

        # Utiliser une fonction qui calcule les positions intermédiaires pour avoir toutes les entités qui se déplacent "en même temps"
        pass        

    def place_tile(self, tile: pygame.image, pos: tuple):
        pos_iso = isometric.cart_to_iso(pos)
        self.blit(tile, self.place_top_position(isometric.iso_to_print(pos_iso)))
        
    def generate_ground(self, tile: pygame.image):
        for i in range(N):
            for j in range(M):
                self.place_tile(tile, (i,j))

    def render_game(self):
        self.place_entity(self.bob, (5,0))
        self.place_entity(self.apple, (6,0))
    
    # --- ??? ---

    def place_interface_in_middle(self, window):
        """
            Place le centre de la carte sur la fenêtre
        """
        window_center = (window_size[0] // 2, window_size[1] // 2)
        interface_center = (screen_size[0] //2, screen_size[1] // 2)
        offset_to_place = (window_center[0] - interface_center[0], window_center[1] - interface_center[1])
        window.blit(self, offset_to_place)
