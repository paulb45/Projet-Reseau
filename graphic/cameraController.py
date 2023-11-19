from pygame import Surface, Rect, transform

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import config

# TODO A IMPLEMENTER
def is_coordinate_in_map(x, y) -> bool:
    return True
# TODO A IMPLEMENTER

class CameraController:

    def __init__(self, main_surface:Surface):
        self.main_surface = main_surface # surface du jeu
        # self.window_width = window_width
        # self.window_height = window_height
        # taille de l'écran dans config.py

        self.viewpoint = None

        self.zoom_max = 0
        self.zoom_min = 0

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
        self.modify_size_window()
        
        # calcul du zoom initial
        # on va partir par défaut sur l'affichage de 20 cases sur la largeur
        if (config.N > 20):
            self.zoom_map_width = config.tile_size * 20
        else:
            self.zoom_map_width = config.tile_size * config.N

        self.zoom_map_height = int(self.zoom_map_width * self.aspect_ratio)

        # calcul de la posistion du point de vu, au milieu par défaut
        self.position_camera_x = (self.main_surface.get_width() // 2) - (self.zoom_map_width // 2)
        self.position_camera_y = (self.main_surface.get_height() // 2) - (self.zoom_map_height // 2)
         

    def get_viewpoint(self) -> Surface:
        """Obtenir et calculer le ponit de vu

        Returns:
            Surface: surface à afficher à l'écran
        """
        # on prend la sous surface
        subview = self.main_surface.subsurface(Rect(self.position_camera_x, 
                                                    self.position_camera_y, 
                                                    self.zoom_map_width, 
                                                    self.zoom_map_height))

        # on adapte la sous-surface à la taille de la fenetre
        self.viewpoint = transform.scale(subview, config.window_size)

        return self.viewpoint


    def modify_size_window(self):
        """Méthode à appeler s'il y a redimenssion de la taille de la fenetre
        """
        self.aspect_ratio = config.window_size[1] / config.window_size[0]


    # TODO implémenter la vérif de sorti de map
    def zoom_in(self):
        """zoom vers l'avant de la caméra, de 2 cases. On ne peux pas zoomer sur plus petit que 4 cases de large
        """
        # rétressiement de la zone affiché
        zoom_map_width_next = self.zoom_map_width - config.tile_size * 2

        if not (zoom_map_width_next <= (config.tile_size * 4)):
            self.zoom_map_width = zoom_map_width_next
            self.zoom_map_height -= config.tile_size

            # le zoom se fait au milieu par rapport au zoom précédent
            self.move_right()
            self.move_down()


    def zoom_out(self):
        """zoom vers l'arrière de la caméra, de 2 cases
        """
        # le dezoom est un poil plus complex au niveau des vérifications
        zoom_map_width_next = self.zoom_map_width + config.tile_size * 2
        zoom_map_height_next = self.zoom_map_height + config.tile_size
        position_camera_x_next = self.position_camera_x - config.tile_size
        position_camera_y_next = self.position_camera_y - (config.tile_size // 2)

        if  ((position_camera_x_next >= 0) and (position_camera_y_next >= 0)
            and (position_camera_x_next + zoom_map_width_next <= self.main_surface.get_width()) 
            and (position_camera_y_next + zoom_map_height_next <= self.main_surface.get_height())):
            # agrandissement de la zone affiché
            self.zoom_map_width = zoom_map_width_next
            self.zoom_map_height = zoom_map_height_next

            # le dezoom se replace sur le milieu du zoom précédent
            self.position_camera_x = position_camera_x_next
            self.position_camera_y = position_camera_y_next


    def move_right(self):
        """mouvement de la caméra d'une case vers la droite
        """
        position_camera_x_next = self.position_camera_x + config.tile_size

        if (((position_camera_x_next + self.zoom_map_width) < self.main_surface.get_width()) 
            and (is_coordinate_in_map(position_camera_x_next, self.position_camera_y)
                or is_coordinate_in_map(position_camera_x_next, self.position_camera_y + self.zoom_map_height))):
            self.position_camera_x = position_camera_x_next


    def move_left(self):
        """mouvement de la caméra d'une case vers la gauche
        """
        position_camera_x_next = self.position_camera_x - config.tile_size

        if ((position_camera_x_next >= 0)
            and (is_coordinate_in_map(position_camera_x_next + self.zoom_map_width, self.position_camera_y)
                or is_coordinate_in_map(position_camera_x_next + self.zoom_map_width, self.position_camera_y + self.zoom_map_height))):
            self.position_camera_x = position_camera_x_next


    def move_up(self):
        """mouvement de la caméra d'une case vers le haut
        """
        position_camera_y_next = self.position_camera_y - (config.tile_size // 2)

        if ((position_camera_y_next >= 0)
            and (is_coordinate_in_map(self.position_camera_x, position_camera_y_next)
                or is_coordinate_in_map(self.position_camera_x + self.zoom_map_width, position_camera_y_next))):
            self.position_camera_y = position_camera_y_next


    def move_down(self):
        """mouvement de la caméra d'une case vers le bas
        """
        position_camera_y_next = self.position_camera_y + (config.tile_size // 2)

        if (((position_camera_y_next + self.zoom_map_height) < self.main_surface.get_height())
            and (is_coordinate_in_map(self.position_camera_x, position_camera_y_next + self.zoom_map_height)
                or is_coordinate_in_map(self.position_camera_x + self.zoom_map_width, position_camera_y_next + self.zoom_map_height))):
            self.position_camera_y = position_camera_y_next



if __name__ == '__main__':
    import pygame
    import time

    from interface import Interface

    pygame.init()

    # Création de la fenêtre
    window = pygame.display.set_mode(config.window_size)

    clock = pygame.time.Clock()

    screen = Interface(config.screen_size)

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
            if (mouse_x > (config.window_size[0] - 10)):
                camera.move_right()
            if (mouse_y < 10):
                camera.move_up()
            if (mouse_y > (config.window_size[1] - 10)):
                camera.move_down()

            move_mouse_timer = time.time()

        window.fill("black")

        window.blit(camera.get_viewpoint(), (0,0))


        pygame.display.flip()
        clock.tick(config.max_framerate)