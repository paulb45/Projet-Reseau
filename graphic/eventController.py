import pygame
import sys
import time
from config import *

class EventController:
    """
        Classe pour gérer les évènements pygame
    """

    def __init__(self, camera):
        """
            Constructeur de EventController

        Args:
            camera (CameraController): camera du jeu
        """
        self.camera = camera

        self.move_mouse_timer = time.time()

    def quit(self):
        pygame.quit()
        sys.exit()

    def move_map_with_mouse_on_border(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # réduire la vitesse de déplacement avec la souris
        if (time.time() - self.move_mouse_timer) >= .02:
            # voir où est le curseur de la souris
            if (mouse_x < size_move_border):
                self.camera.move_left()
            if (mouse_x > (pygame.display.get_surface().get_width() - size_move_border)):
                self.camera.move_right()
            if (mouse_y < size_move_border):
                self.camera.move_up()
            if (mouse_y > (pygame.display.get_surface().get_height() - size_move_border)):
                    self.camera.move_down()

            self.move_mouse_timer = time.time()
    
    def keyboard_pressed(self):
        keystate = pygame.key.get_pressed()

        if keystate[pygame.K_LEFT]:
            self.camera.move_left()
        if keystate[pygame.K_RIGHT]:
            self.camera.move_right()
        if keystate[pygame.K_UP]:
            self.camera.move_up()
        if keystate[pygame.K_DOWN]:
            self.camera.move_down()
        if keystate[pygame.K_p]:
            self.camera.zoom_in()
        if keystate[pygame.K_m]:
            self.camera.zoom_out()


    def run_events(self):
        """
            Méthode pour vérifier la présente de chaque évènement, et appeler les actions qui leurs sont associés
        """
        for event in pygame.event.get():

            if event.type == pygame.VIDEORESIZE:
                # A METTRE DANS UNE FONCTION A PART
                # NE FONCTIONNE PAS
                
                self.camera.modify_size_window()

            if event.type == pygame.QUIT:
                self.quit()

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 4:
                    self.camera.zoom_in()
                elif event.button == 5:
                    self.camera.zoom_out()

        self.keyboard_pressed()

        if move_with_mouse:
            self.move_map_with_mouse_on_border()
            