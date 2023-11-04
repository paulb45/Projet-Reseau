from pygame import Surface, Rect, transform

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import config

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


    def zoom_in(self) -> Surface:
        pass


    def zoom_out(self) -> Surface:
        pass


    def move_right(self):
        """mouvement de la caméra d'une case vers la droite
        """
        position_camera_x_next = self.position_camera_x + config.tile_size

        if not ((position_camera_x_next + self.zoom_map_width) >= self.main_surface.get_width()):
            self.position_camera_x = position_camera_x_next


    def move_left(self):
        """mouvement de la caméra d'une case vers la gauche
        """
        position_camera_x_next = self.position_camera_x - config.tile_size

        if not (position_camera_x_next < 0):
            self.position_camera_x = position_camera_x_next


    def move_up(self):
        """mouvement de la caméra d'une case vers le haut
        """
        position_camera_y_next = self.position_camera_y - (config.tile_size // 2)

        if not (position_camera_y_next < 0):
            self.position_camera_y = position_camera_y_next


    def move_down(self):
        """mouvement de la caméra d'une case vers le bas
        """
        position_camera_y_next = self.position_camera_y + (config.tile_size // 2)

        if not ((position_camera_y_next + self.zoom_map_height) >= self.main_surface.get_height()):
            self.position_camera_y = position_camera_y_next



if __name__ == '__main__':
    import pygame
    from interface import Interface

    pygame.init()

    # Création de la fenêtre
    window = pygame.display.set_mode(config.window_size)

    clock = pygame.time.Clock()

    screen = Interface(config.window_size)

    screen.render_game()

    camera = CameraController(screen)

    while True:
        # Faire une fonction event_handler ?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    camera.move_left()
                elif event.key == pygame.K_RIGHT:
                    camera.move_right()
                elif event.key == pygame.K_UP:
                    camera.move_up()
                elif event.key == pygame.K_DOWN:
                    camera.move_down()

        window.fill("black")

        window.blit(camera.get_viewpoint(), (0,0))


        pygame.display.flip()
        clock.tick(config.max_framerate)