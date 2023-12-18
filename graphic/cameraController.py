import pygame

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import *

# python3 -m pip install shapely
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

SPEED_MIN = 2
SPEED_MAX = 8

class CameraController:

    def __init__(self, main_surface: pygame.Surface):
        self.main_surface = main_surface # surface du jeu

        # taille de la fenetre windows considérée par CameraController (!= taille réelle de la fenetre)
        self.window_width = pygame.display.get_surface().get_width()
        self.window_height = pygame.display.get_surface().get_height()

        # en pixel sur la largeur
        self.move_step = 0

        # position dans le coin supérieur gauche de la caméra
        self.position_camera_x = 0
        self.position_camera_y = 0

        # taille en largeur et longueur que représente le zoom
        self.zoom_map_width = 0
        self.zoom_map_height = 0

        # rapport entre la hauteur et la largeur de l'écran
        self.aspect_ratio = 0

        # vitesse du déplacement (nombre de pixel)
        self.speed = 6
        
        # calcul du zoom initial
        # on va partir par défaut sur l'affichage de 20 cases sur la largeur
        if Config.width_map > 20:
            self.zoom_map_width = tile_size * 20
        else:
            self.zoom_map_width = tile_size * Config.width_map

        self.aspect_ratio = pygame.display.get_surface().get_height() / pygame.display.get_surface().get_width()
        self.zoom_map_height = int(self.zoom_map_width * self.aspect_ratio)


        # calcul de la position du point de vue, au milieu par défaut
        self.position_camera_x = (self.main_surface.get_width() // 2) - (self.zoom_map_width // 2)
        self.position_camera_y = (self.main_surface.get_height() // 2) - (self.zoom_map_height // 2)

        # forme de losange pour la vérification de sorti de map
        self.mathematic_map = Polygon((
            (self.main_surface.get_width() // 2, Config.interface_y_offset),
            (self.main_surface.get_width() - Config.interface_x_offset, self.main_surface.get_height() // 2),
            (self.main_surface.get_width() // 2, self.main_surface.get_height() - Config.interface_y_offset),
            (Config.interface_x_offset, self.main_surface.get_height() // 2)
        ))
         

    def get_viewpoint(self) -> pygame.Surface:
        """Obtenir et calculer le ponit de vu

        Returns:
            Surface: surface à afficher à l'écran
        """ 
        try:
            # on prend la sous surface
            subview = self.main_surface.subsurface(pygame.Rect(self.position_camera_x, 
                                                        self.position_camera_y, 
                                                        self.zoom_map_width, 
                                                        self.zoom_map_height))

            # on adapte la sous-surface à la taille de la fenetre
            viewpoint = pygame.transform.scale(subview, pygame.display.get_surface().get_size())

            return viewpoint

        except ValueError:
            print("Une erreur est survenu lors de l'affichage, nous sommes désolés de ce contretemps")
            exit()


    def modify_speed(self) -> None:
        # mise à l'echelle linéaire en fonction du zoom
        self.speed = SPEED_MIN + ((self.zoom_map_width - zoom_min*tile_size) * (SPEED_MAX - SPEED_MIN)) // (zoom_max*tile_size + zoom_min*tile_size)


    def get_zoom_ratio(self) -> int:
        """Obtenir la valeur actuel du zoom sur une échelle de 0 à 100

        Returns:
            int: taux de zoom entre 0 et 100
        """
        return int((1 - (self.zoom_map_width - zoom_min*tile_size) / (min(self.main_surface.get_width(), zoom_max*tile_size) - zoom_min*tile_size)) * 100)

    
    def change_zoom_with_slider(self, ratio:float) -> None:
        """Changer le zoom grace à la valeur du slider du menu du jeu

        Args:
            ratio (float): taux entre 0 et 100
        """
        new_zoom = int((min(self.main_surface.get_width(), zoom_max*tile_size) - zoom_min*tile_size) * (1-(ratio / 100)) + zoom_min*tile_size)

        if new_zoom < self.zoom_map_width:
            self.zoom_in(self.zoom_map_width - new_zoom)
        elif new_zoom > self.zoom_map_width:
            self.zoom_out(new_zoom - self.zoom_map_width)


    def modify_size_window(self):
        """Méthode à appeler s'il y a redimension de la taille de la fenetre
        """
        self.aspect_ratio = pygame.display.get_surface().get_height() / pygame.display.get_surface().get_width()
        # largeur du zoom multiplié par le ratio de la fenetre
        zoom_map_height_next = int(self.zoom_map_width * self.aspect_ratio)

        if zoom_map_height_next > self.main_surface.get_height():
            zoom_map_height_next = self.main_surface.get_height()
            self.zoom_map_width = int(self.zoom_map_height * pygame.display.get_surface().get_width() / pygame.display.get_surface().get_height())

        if (self.position_camera_y + zoom_map_height_next) > self.main_surface.get_height():
            self.position_camera_y = self.main_surface.get_height() - zoom_map_height_next
        
        self.zoom_map_height = zoom_map_height_next


    def zoom_in(self, _zoom_step = tile_size*2):
        """zoom vers l'avant de la caméra, de 2 cases. On ne peux pas zoomer sur plus petit que 4 cases de large

        Args:
            _zoom_step (int, optional): pas du zoom. Defaults to tile_size*2.
        """
        # rétrecissement de la zone affichée
        zoom_map_width_next = self.zoom_map_width - _zoom_step

        if (zoom_map_width_next <= (tile_size * zoom_min)):
            zoom_map_width_next = (tile_size * zoom_min)

        if (zoom_map_width_next != self.zoom_map_width):
            zoom_map_height_next = int(zoom_map_width_next * self.aspect_ratio)

            position_camera_x_next = self.position_camera_x + (self.zoom_map_width - zoom_map_width_next) // 2
            position_camera_y_next = self.position_camera_y + (self.zoom_map_height - zoom_map_height_next) // 2

            self.position_camera_x = position_camera_x_next
            self.position_camera_y = position_camera_y_next

            self.zoom_map_width = zoom_map_width_next
            self.zoom_map_height = zoom_map_height_next

            self.modify_speed()


    def zoom_out(self, _zoom_step = tile_size*2):
        """zoom vers l'arrière de la caméra, de 2 cases

        Args:
            _zoom_step (int, optional): pas du dezoom. Defaults to tile_size*2.
        """
        # si on est déjà au zoom max on ne fais rien
        if self.zoom_map_width < min((tile_size * zoom_max), self.main_surface.get_width()):
            # le dezoom est un poil plus complex au niveau des vérifications
            zoom_map_width_next = self.zoom_map_width + _zoom_step
            zoom_map_height_next = int(zoom_map_width_next * self.aspect_ratio)

            # si zoom suivant plus grand que le zoom max
            if zoom_map_width_next > min((tile_size * zoom_max), self.main_surface.get_width()):
                zoom_map_width_next = min((tile_size * zoom_max), self.main_surface.get_width())
                zoom_map_height_next = int(zoom_map_width_next * self.aspect_ratio)

            position_camera_y_next = 0
            position_camera_x_next = 0

            # la hauteur doit être inférieur ou égal à la hauteur de la surface principale
            if zoom_map_height_next > self.main_surface.get_height():
                zoom_map_height_next = self.main_surface.get_height()
                zoom_map_width_next = int(zoom_map_height_next / self.aspect_ratio)

                position_camera_x_next = self.position_camera_x - ((zoom_map_width_next - self.zoom_map_width) // 2)
            else:
                position_camera_y_next = self.position_camera_y - ((zoom_map_height_next - self.zoom_map_height) // 2)
                position_camera_x_next = self.position_camera_x - _zoom_step // 2

            # haut
            if position_camera_y_next < 0:
                position_camera_y_next = 0
            # bas
            if (position_camera_y_next + zoom_map_height_next) > self.main_surface.get_height():
                position_camera_y_next = self.main_surface.get_height() - zoom_map_height_next
            # gauche
            if position_camera_x_next < 0:
                position_camera_x_next = 0
            # droite
            if (position_camera_x_next + zoom_map_width_next) > self.main_surface.get_width():
                position_camera_x_next = self.main_surface.get_width() - zoom_map_width_next

            # le dezoom se replace sur le milieu du zoom précédent
            self.position_camera_x = position_camera_x_next
            self.position_camera_y = position_camera_y_next
            
            # agrandissement de la zone affiché
            self.zoom_map_width = zoom_map_width_next
            self.zoom_map_height = zoom_map_height_next   

            self.modify_speed()     


    def move_right(self):
        """mouvement de la caméra d'une case vers la droite
        """
        position_camera_x_next = self.position_camera_x + self.speed

        if (position_camera_x_next + self.zoom_map_width) > self.main_surface.get_width():
            position_camera_x_next = self.main_surface.get_width() - self.zoom_map_width

        if self._is_camera_in_map(
            top_right_corner = (position_camera_x_next + self.zoom_map_width, self.position_camera_y), 
            bottom_right_corner = (position_camera_x_next + self.zoom_map_width, self.position_camera_y + self.zoom_map_height)
        ):
            self.position_camera_x = position_camera_x_next


    def move_left(self):
        """mouvement de la caméra d'une case vers la gauche
        """
        position_camera_x_next = self.position_camera_x - self.speed

        if position_camera_x_next < 0:
            position_camera_x_next = 0

        if self._is_camera_in_map(
            top_left_corner = (position_camera_x_next, self.position_camera_y),
            bottom_left_corner = (position_camera_x_next, self.position_camera_y + self.zoom_map_height)
        ):
            self.position_camera_x = position_camera_x_next


    def move_up(self):
        """mouvement de la caméra d'une case vers le haut
        """
        position_camera_y_next = self.position_camera_y - (self.speed // 2)

        if (position_camera_y_next < 0):
            position_camera_y_next = 0

        if self._is_camera_in_map(
            top_left_corner = (self.position_camera_x, position_camera_y_next),
            top_right_corner = (self.position_camera_x + self.zoom_map_width, position_camera_y_next)
        ):
            self.position_camera_y = position_camera_y_next


    def move_down(self):
        """mouvement de la caméra d'une case vers le bas
        """
        position_camera_y_next = self.position_camera_y + (self.speed // 2)   

        if (position_camera_y_next + self.zoom_map_height) > self.main_surface.get_height():
            position_camera_y_next = self.main_surface.get_height() - self.zoom_map_height

        if self._is_camera_in_map(
            bottom_left_corner = (self.position_camera_x, position_camera_y_next + self.zoom_map_height),
            bottom_right_corner = (self.position_camera_x + self.zoom_map_width, position_camera_y_next + self.zoom_map_height)
        ):
            self.position_camera_y = position_camera_y_next


    def position_camera_to_game(self, x:int, y:int) -> (int, int):
        """Obtenir la position en pixel sur la carte du jeu, par rapport à une coordonnée sur la fenêtre

        Args:
            x (int): position en absisse sur la fenêtre
            y (int): position en ordonnée sur la fenêtre

        Returns:
            (int, int): coordonnée sur la carte du jeu
        """
        return self.position_camera_x + x, self.position_camera_y + y


    def _is_camera_in_map(self, number_corner = 2, /, top_left_corner = None, top_right_corner = None, bottom_right_corner = None, bottom_left_corner = None) -> bool:
        """ Prédicat pour savoir si le nombre de coins de la caméra indiqués est sur la map du jeu

        Args:
            number_corner (int, optional): nombre de coins qui doivent être sur la map. Defaults to 2.
            top_left_corner (tuple(int, int), optional): coin supérieur gauche de la caméra. Defaults to None.
            top_right_corner (tuple(int, int), optional): coin supérieur droit de la caméra. Defaults to None.
            bottom_right_corner (tuple(int, int), optional): coin inférieur droit de la caméra. Defaults to None.
            bottom_left_corner (tuple(int, int), optional): coin inférieur gauche de la caméra. Defaults to None.

        Returns:
            bool: Vrai si le nombre de coin requis sont bien sur la map, Faux sinon
        """
        if (self.zoom_map_width < self.main_surface.get_width() // 2) and (Config.width_map > zoom_max):
            # haut-gauche, haut-droite, bas-droite, bas-gauche
            points = (
                Point(top_left_corner if top_left_corner is not None else (self.position_camera_x, self.position_camera_y)),
                Point(top_right_corner if top_right_corner is not None else (self.position_camera_x + self.zoom_map_width, self.position_camera_y)),
                Point(bottom_right_corner if bottom_right_corner is not None else (self.position_camera_x + self.zoom_map_width, self.position_camera_y + self.zoom_map_height)),
                Point(bottom_left_corner if bottom_left_corner is not None else (self.position_camera_x, self.position_camera_y + self.zoom_map_height))
            )

            return sum(1 for p in points if p.within(self.mathematic_map)) >= number_corner
        else:
            return True


    def _debug(self):
        """Méthode pour afficher quelque information utils, pratique pour faire du debugage dans le terminal
        """
        print(
            f"main_surface.width = {self.main_surface.get_width()}\n",
            f"main_surface.height = {self.main_surface.get_height()}\n",
            f"zoom_map_width = {self.zoom_map_width}\n",
            f"zoom_map_height = {self.zoom_map_height}\n",
            f"position_camera_x = {self.position_camera_x}\n",
            f"position_camera_y = {self.position_camera_y}\n"
        )