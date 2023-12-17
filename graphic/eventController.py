import pygame
import sys
import time
from config import *

class EventController:
    """
        Classe pour gérer les évènements pygame
    """

    def __init__(self, camera, menu):
        """
            Constructeur de EventController

        Args:
            camera (CameraController): camera du jeu
        """
        self.camera = camera

        self.menu = menu

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
            self.menu.zoom_slider.set_value(self.camera.get_zoom_ratio())
        if keystate[pygame.K_m]:
            self.camera.zoom_out()
            self.menu.zoom_slider.set_value(self.camera.get_zoom_ratio())


    def run_events(self):
        """
            Méthode pour vérifier la présente de chaque évènement, et appeler les actions qui leurs sont associés
        """
    
        events = pygame.event.get()

        if self.camera == None:
            self.menu.main_menu.update(events)
            for event in events:
                if event.type == pygame.VIDEORESIZE:  
                    self.menu.main_menu.resize(pygame.display.get_surface().get_width(),pygame.display.get_surface().get_height())
                    self.menu.game_screen.resize(pygame.display.get_surface().get_width(),pygame.display.get_surface().get_height())
                    self.menu.new_game.resize(pygame.display.get_surface().get_width(), pygame.display.get_surface().get_height())
        else:
            for event in events:
                
                if event.type == pygame.VIDEORESIZE:               
                    self.camera.modify_size_window()
                    self.menu.main_menu.resize(pygame.display.get_surface().get_width(),pygame.display.get_surface().get_height())
                    self.menu.game_screen.resize(pygame.display.get_surface().get_width(),pygame.display.get_surface().get_height())
                    self.menu.new_game.resize(pygame.display.get_surface().get_width(), pygame.display.get_surface().get_height())

                if event.type == pygame.QUIT:
                    self.quit()

                if event.type == pygame.USEREVENT+1:
                    self.camera.change_zoom_with_slider(self.menu.zoom_slider.get_value())
                
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 4:
                        self.camera.zoom_in()
                    elif event.button == 5:
                        self.camera.zoom_out()
                    self.menu.zoom_slider.set_value(self.camera.get_zoom_ratio())
    
                
            self.keyboard_pressed()

            if Config.move_with_cursor:
                self.move_map_with_mouse_on_border()

            
            
            if self.menu.game_is_on:
                # events = [e for e in events if e.type != 768]
                self.menu.game_screen.update([e for e in events if e.type != 768])
            else:    
                self.menu.main_menu.update(events)

