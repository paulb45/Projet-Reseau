import pygame
import pygame_menu
from typing import Tuple, Optional

class Menu(pygame.Surface):

    def __init__(self):
        super().__init__(pygame.display.get_surface().get_size())
        myfont=pygame_menu.font.FONT_MUNRO
        myfontsize = 30
        window_size = pygame.display.get_surface().get_size()
        mytheme1 = pygame_menu.themes.THEME_SOLARIZED.copy()
        mytheme1.background_color=(0, 0, 0 ,0)
        mytheme1.widget_alignment = pygame_menu.locals.ALIGN_RIGHT
        mytheme1.widget_font =myfont
        mytheme1.widget_font_size = myfontsize
        mytheme1.widget_title_font = myfont
        mytheme2 = pygame_menu.themes.THEME_SOLARIZED.copy()
        mytheme2.background_color=(15,20,50)
        mytheme2.widget_alignment = pygame_menu.locals.ALIGN_CENTER
        mytheme2.widget_font =myfont
        mytheme2.widget_font_size = myfontsize
        mytheme2.widget_title_font = myfont
        pygame_menu.themes.THEME_BLUE.widget_font_size = myfontsize
        pygame_menu.themes.THEME_BLUE.widget_font = myfont

        def games_creen_menu(self):
            self.game_screen = pygame_menu.Menu('Gaming',window_size[0],window_size[1],theme=mytheme1)
            self.game_screen.add.button('Quit', pygame_menu.events.EXIT)

        def start_menu(self):
            self.start = pygame_menu.Menu('New Game',window_size[0],window_size[1],theme= mytheme2)
            self.start.add.text_input('largeur de la carte :', default='100',textinput_id='map_width',input_type=pygame_menu.locals.INPUT_INT)
            self.start.add.text_input('hauteur de la carte :', default='100',textinput_id='map_height',input_type=pygame_menu.locals.INPUT_INT)
            self.start.add.text_input('Population de départ :', default='100',textinput_id='population_bob',input_type=pygame_menu.locals.INPUT_INT)
            self.start.add.text_input('Nouriture de départ :', default='100',textinput_id='population_food',input_type=pygame_menu.locals.INPUT_INT)
            self.start.add.text_input('movement de bob :', default='1',textinput_id='movement_bob',input_type=pygame_menu.locals.INPUT_INT)
            self.start.add.button('Quit', pygame_menu.events.EXIT)
            self.start.add.button('start',self.game_screen)
            #mainloop ?
            def data_fun() -> None:
                """
                Print data of the menu.
                """
                print('Settings data:')
                data = self.start.get_input_data()
                for k in data.keys():
                    print(f'\t{k}\t=>\t{data[k]}')

            self.start.add.button('Store data', data_fun, button_id='store')
            self.start.add.buttonsettings_menu.add.button('Restore original values', self.start.reset_value)
            self.start.add.button('Return to main menu', pygame_menu.events.BACK)
        #def load_menu(self):
        #   load = pygame_menu.Menu('New Game',window_size[0],window_size[1],theme=mytheme2)
        #   load.add.vertical_margin(50)
        #   load.add.button('Quit', pygame_menu.events.EXIT)
        #   load.add.button('self.start',games_creen_menu)
        #   load.draw(surface)

        def principal_menu(self):
            self.main_menu = pygame_menu.Menu('EVOlution',window_size[0],window_size[1],theme=mytheme2)
            self.main_menu.add.button('new game', start_menu)
            #self.main_menu.add.button('load game', load_menu)
            self.main_menu.add.button('Quit', pygame_menu.events.EXIT)

if __name__ == '__main__':
    pygame.init()
    surface = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
    menu=Menu()
    while True:
        events = pygame.event.get()
        #menu.event_menu(events)
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                break
        #main_menu.update(events)
        #surface.blit(menu,(0,0))
        pygame.display.flip()