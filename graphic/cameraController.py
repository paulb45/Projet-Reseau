import pygame

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import *

# TODO A IMPLEMENTER
def is_coordinate_in_map(x, y) -> bool:
    return True
# TODO A IMPLEMENTER

class CameraController:

    def __init__(self, main_surface: pygame.Surface):
        self.main_surface = main_surface # surface du jeu
        # self.window_width = window_width
        # self.window_height = window_height
        # taille de l'écran dans config.py

        self.window_size = pygame.display.get_surface().get_size()

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
        
        # calcul du zoom initial
        # on va partir par défaut sur l'affichage de 20 cases sur la largeur
        if (N > 20):
            self.zoom_map_width = tile_size * 20
        else:
            self.zoom_map_width = tile_size * N

        self.aspect_ratio = pygame.display.get_surface().get_height() / pygame.display.get_surface().get_width()
        self.zoom_map_height = int(self.zoom_map_width * self.aspect_ratio)


        # calcul de la position du point de vue, au milieu par défaut
        self.position_camera_x = (self.main_surface.get_width() // 2) - (self.zoom_map_width // 2)
        self.position_camera_y = (self.main_surface.get_height() // 2) - (self.zoom_map_height // 2)
         

    def get_viewpoint(self) -> pygame.Surface:
        """Obtenir et calculer le ponit de vu

        Returns:
            Surface: surface à afficher à l'écran
        """
        # on prend la sous surface
        subview = self.main_surface.subsurface(pygame.Rect(self.position_camera_x, 
                                                    self.position_camera_y, 
                                                    self.zoom_map_width, 
                                                    self.zoom_map_height))

        # on adapte la sous-surface à la taille de la fenetre
        viewpoint = pygame.transform.scale(subview, pygame.display.get_surface().get_size())

        return viewpoint


    def modify_size_window(self):
        """Méthode à appeler s'il y a redimension de la taille de la fenetre
        """
        range_width = pygame.display.get_surface().get_width() - self.window_size[0]
        range_height = pygame.display.get_surface().get_height() - self.window_size[1]
        zoom_map_width_next = self.zoom_map_width + range_width
        zoom_map_height_next = self.zoom_map_height + range_height

        if self.position_camera_x + zoom_map_width_next > self.main_surface.get_width():
            if self.position_camera_x - range_width < 0:
                pass
            else:
                print(self.position_camera_x)
                self.position_camera_x -= range_width

        if self.position_camera_y + zoom_map_height_next > self.main_surface.get_height():
            pass 

        self.zoom_map_width = zoom_map_width_next
        self.zoom_map_height = zoom_map_height_next   

        self.window_size = pygame.display.get_surface().get_size()




    # TODO implémenter la vérif de sorti de map
    def zoom_in(self):
        """zoom vers l'avant de la caméra, de 2 cases. On ne peux pas zoomer sur plus petit que 4 cases de large
        """
        # rétrecissement de la zone affichée
        zoom_map_width_next = self.zoom_map_width - tile_size * 2

        if not (zoom_map_width_next <= (tile_size * zoom_min)):
            self.zoom_map_width = zoom_map_width_next
            self.zoom_map_height -= tile_size

            # le zoom se fait au milieu par rapport au zoom précédent
            self.move_right()
            self.move_down()


    def zoom_out(self):
        """zoom vers l'arrière de la caméra, de 2 cases
        """
        # le dezoom est un poil plus complex au niveau des vérifications
        zoom_map_width_next = self.zoom_map_width + tile_size * 2
        zoom_map_height_next = self.zoom_map_height + tile_size
        position_camera_x_next = self.position_camera_x - tile_size
        position_camera_y_next = self.position_camera_y - (tile_size // 2)

        if (zoom_map_width_next <= min((tile_size * zoom_max), self.main_surface.get_width())):
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
            
            # agrandissement de la zone affiché
            self.zoom_map_width = zoom_map_width_next
            self.zoom_map_height = zoom_map_height_next

            # le dezoom se replace sur le milieu du zoom précédent
            self.position_camera_x = position_camera_x_next
            self.position_camera_y = position_camera_y_next


    def move_right(self):
        """mouvement de la caméra d'une case vers la droite
        """
        position_camera_x_next = self.position_camera_x + tile_size

        if (position_camera_x_next + self.zoom_map_width) > self.main_surface.get_width():
            position_camera_x_next = self.main_surface.get_width() - self.zoom_map_width

        if (((position_camera_x_next + self.zoom_map_width) <= self.main_surface.get_width()) 
            and (is_coordinate_in_map(position_camera_x_next, self.position_camera_y)
                or is_coordinate_in_map(position_camera_x_next, self.position_camera_y + self.zoom_map_height))):
            self.position_camera_x = position_camera_x_next


    def move_left(self):
        """mouvement de la caméra d'une case vers la gauche
        """
        position_camera_x_next = self.position_camera_x - tile_size

        if position_camera_x_next < 0:
            position_camera_x_next = 0

        if ((is_coordinate_in_map(position_camera_x_next + self.zoom_map_width, self.position_camera_y)
                or is_coordinate_in_map(position_camera_x_next + self.zoom_map_width, self.position_camera_y))):
            self.position_camera_x = position_camera_x_next


    def move_up(self):
        """mouvement de la caméra d'une case vers le haut
        """
        position_camera_y_next = self.position_camera_y - (tile_size // 2)

        if (position_camera_y_next < 0):
            position_camera_y_next = 0

        if ((is_coordinate_in_map(self.position_camera_x, position_camera_y_next + self.zoom_map_height)
                or is_coordinate_in_map(self.position_camera_x + self.zoom_map_width, position_camera_y_next + self.zoom_map_height))):
            self.position_camera_y = position_camera_y_next


    def move_down(self):
        """mouvement de la caméra d'une case vers le bas
        """
        position_camera_y_next = self.position_camera_y + (tile_size // 2)   

        if (position_camera_y_next + self.zoom_map_height) > self.main_surface.get_height():
            position_camera_y_next = self.main_surface.get_height() - self.zoom_map_height

        if ((is_coordinate_in_map(self.position_camera_x, position_camera_y_next)
                or is_coordinate_in_map(self.position_camera_x + self.zoom_map_width, position_camera_y_next))):
            self.position_camera_y = position_camera_y_next



if __name__ == '__main__':
    import pygame
    import time

    from interface import Interface

    pygame.init()

    # Création de la fenêtre
    window = pygame.display.set_mode(window_size)

    clock = pygame.time.Clock()

    screen = Interface(screen_size)

    screen.render_game()

    camera = CameraController(screen)

    move_mouse_timer = time.time()

    while True:
        # Faire une fonction event_handler ?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    camera.zoom_in()
                elif event.key == pygame.K_m:
                    camera.zoom_out()

        keystate = pygame.key.get_pressed()

        if keystate[pygame.K_LEFT]:
            camera.move_left()
        if keystate[pygame.K_RIGHT]:
            camera.move_right()
        if keystate[pygame.K_UP]:
            camera.move_up()
        if keystate[pygame.K_DOWN]:
            camera.move_down()

        mouse_x, mouse_y = pygame.mouse.get_pos()

        # réduire la vitesse de déplacement avec la souris
        if (time.time() - move_mouse_timer) >= .02:
            # voir où est le curseur de la souris
            if (mouse_x < 10):
                camera.move_left()
            if (mouse_x > (window_size[0] - 10)):
                camera.move_right()
            if (mouse_y < 10):
                camera.move_up()
            if (mouse_y > (window_size[1] - 10)):
                camera.move_down()

            move_mouse_timer = time.time()

        window.fill("black")

        window.blit(camera.get_viewpoint(), (0,0))


        pygame.display.flip()
        clock.tick(max_framerate)