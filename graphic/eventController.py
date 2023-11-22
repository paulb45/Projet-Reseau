import pygame
import sys
import time
import config

class EventController:
    """Classe pour gérer les évènements pygame
    """

    def __init__(self, camera):
        """Constructeur de EventController

        Args:
            camera (CameraController): camera du jeu
        """
        self.camera = camera

        self.move_mouse_timer = time.time()


    def run_events(self):
        """Méthode pour vérifier la présente de chaque évènement, et appeler les actions qui leurs sont associés
        """
        for event in pygame.event.get():

            if event.type == pygame.VIDEORESIZE:
                pass
                #surface = pygame.display.set_mode((event.w, event.h),pygame.RESIZABLE)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.camera.zoom_in()
                elif event.key == pygame.K_m:
                    self.camera.zoom_out()

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 4:
                    self.camera.zoom_in()
                elif event.button == 5:
                    self.camera.zoom_out()

        keystate = pygame.key.get_pressed()

        if keystate[pygame.K_LEFT]:
            self.camera.move_left()
        if keystate[pygame.K_RIGHT]:
            self.camera.move_right()
        if keystate[pygame.K_UP]:
            self.camera.move_up()
        if keystate[pygame.K_DOWN]:
            self.camera.move_down()

        if config.move_with_mouse:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # réduire la vitesse de déplacement avec la souris
            if (time.time() - self.move_mouse_timer) >= .02:
                # voir où est le curseur de la souris
                if (mouse_x < config.size_move_border):
                    self.camera.move_left()
                if (mouse_x > (config.window_size[0] - config.size_move_border)):
                    self.camera.move_right()
                if (mouse_y < config.size_move_border):
                    self.camera.move_up()
                if (mouse_y > (config.window_size[1] - config.size_move_border)):
                    self.camera.move_down()

                self.move_mouse_timer = time.time()