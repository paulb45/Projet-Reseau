from turtle import width
import pygame
import pygame_menu
from pygame_menu import sound
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import *

class GameMenu(pygame.Surface):

    def __init__(self, surface):
        super().__init__(pygame.display.get_surface().get_size())
        self.engine=sound.Sound()
        self.engine.set_sound(sound.SOUND_TYPE_CLICK_MOUSE,music_path +'mixkit-cool-interface-click-tone-2568.ogg')
        #self.engine.set_sound(sound.SOUND_TYPE_OPEN_MENU, '/home/me/open.ogg')
        self.surface = surface
        self.myfont=pygame_menu.font.FONT_MUNRO
        self.myfontsize = 30
        self.mytheme1 = pygame_menu.themes.THEME_SOLARIZED.copy()
        self.mytheme1.background_color=(0, 0, 0 ,0)
        self.mytheme1.widget_alignment = pygame_menu.locals.ALIGN_RIGHT
        self.mytheme1.widget_font = self.myfont
        self.mytheme1.widget_font_size = self.myfontsize
        self.mytheme1.widget_title_font = self.myfont
        self.mytheme1.title = False
        self.mytheme2 = pygame_menu.themes.THEME_SOLARIZED.copy()
        self.mytheme2.background_color=(15,20,50)
        self.mytheme2.widget_alignment = pygame_menu.locals.ALIGN_CENTER
        self.mytheme2.widget_font = self.myfont
        self.mytheme2.widget_font_size = self.myfontsize
        self.mytheme2.widget_title_font = self.myfont
        self.mytheme2.widget_alignment = pygame_menu.locals.ALIGN_LEFT
        self.mytheme2.title = False
        pygame_menu.themes.THEME_BLUE.widget_font_size = self.myfontsize
        pygame_menu.themes.THEME_BLUE.widget_font = self.myfont
        
        self.main_menu = pygame_menu.Menu('EVOlution',pygame.display.get_surface().get_width(), pygame.display.get_surface().get_height(),theme=self.mytheme2)
        self.game_screen = pygame_menu.Menu('Gaming',pygame.display.get_surface().get_width(), pygame.display.get_surface().get_height(),theme=self.mytheme1)
        self.new_game = pygame_menu.Menu('New Game', pygame.display.get_surface().get_width(), pygame.display.get_surface().get_height(),theme=self.mytheme2)
        
        #self.load_new_game()
        #self.load_main_menu()
        #self.load_game_screen_menu()
        
        self.main_menu.set_sound(self.engine,recursive=True)
        self.main_menu.add.label('Evolutionnary game of life',font_size=self.myfontsize*2,align=pygame_menu.locals.ALIGN_CENTER)
        self.main_menu.add.vertical_margin(50)
        self.main_menu.add.button('new game', self.new_game,align=pygame_menu.locals.ALIGN_CENTER)
        self.main_menu.add.vertical_margin(10)
        self.main_menu.add.button('Quit', pygame.QUIT,align=pygame_menu.locals.ALIGN_CENTER)
        self.main_menu.draw(self.surface)

        self.game_screen.add.button('Quit', pygame_menu.events.EXIT)

        self.new_game.add.vertical_margin(30)
        self.new_game.add.text_input('largeur de la carte :', default=str(N),textinput_id='map_width',input_type=pygame_menu.locals.INPUT_INT)
        self.new_game.add.text_input('hauteur de la carte :', default=str(M),textinput_id='map_height',input_type=pygame_menu.locals.INPUT_INT)
        self.new_game.add.text_input('Population de départ :', default=str(pop_init),textinput_id='population_bob',input_type=pygame_menu.locals.INPUT_INT)
        self.new_game.add.text_input('Nouriture de départ :', default=str(init_quantity_food),textinput_id='population_food',input_type=pygame_menu.locals.INPUT_INT)
        self.new_game.add.text_input('nouriture par jour :', default='1',textinput_id='daily_food',input_type=pygame_menu.locals.INPUT_INT)
        self.new_game.add.text_input('Mouvement de bob :', default='1',textinput_id='movement_bob',input_type=pygame_menu.locals.INPUT_INT)
        self.new_game.add.text_input('vision de bob :', default='1',textinput_id='vision_bob',input_type=pygame_menu.locals.INPUT_INT)
        self.new_game.add.text_input('masse de bob :', default='1',textinput_id='mass_bob',input_type=pygame_menu.locals.INPUT_INT)
        self.new_game.add.text_input('Energie de la nourriture', default=str(init_energy_food),textinput_id='energy_to_mate',input_type=pygame_menu.locals.INPUT_INT)
        self.new_game.add.text_input('energy des parent apres reproduction', default='100',textinput_id='energy_after_mating',input_type=pygame_menu.locals.INPUT_INT)
        self.new_game.add.text_input('energie necessaire pour ce cloner :', default='200',textinput_id='energy_to_clone',input_type=pygame_menu.locals.INPUT_INT)
        self.new_game.add.text_input('energie du bob enfant :', default='100',textinput_id='bob_child_energy',input_type=pygame_menu.locals.INPUT_INT)
        self.new_game.add.button('Quit', pygame.QUIT)
        self.new_game.add.button('start', self.game_screen)

        def data_fun() -> None:
            """
            Print data of the menu.
            """
            print('Settings data:')
            data = self.new_game.get_input_data()
            for k in data.keys():
                print(f'\t{k}\t=>\t{data[k]}')
            Config.width_map = data['map_width']
            Config.height_map = data['map_height']
            print(f"map: ({Config.width_map},{Config.height_map})")
        self.new_game.add.button('Store data', data_fun, button_id='store')
        self.new_game.add.button('Restore original values', self.new_game.reset_value)
        self.new_game.add.button('Return to main menu', pygame_menu.events.BACK)
        self.new_game.add.vertical_margin(10)

        def on_resize() -> None:
            """
            Function checked if the window is resized.
            """
            window_size = surface.get_size()
            new_w, new_h = 0.75 * window_size[0], 0.7 * window_size[1]
            menu.resize(new_w, new_h)
            print(f'New menu size: {menu.get_size()}')

    # def to_print(self, menu_name: str):
    #     match menu_name:
    #         case "main_menu":
    #             events =  pygame.event.get()
    #             self.main_menu.update(events)
    #             self.main_menu.draw(self.surface)
    #             #self.main_menu.mainloop(self.surface)
    #         case "game_screen":
    #             self.game_screen.draw(self.subsurface)
    #             #self.game_screen.mainloop(self.surface)
    #         case "new_game":
    #             self.new_game.draw(self.surface)
    #             #self.new_game.mainloop(self.subsurface)
                
if __name__ == '__main__':
    pygame.init()
    surface = pygame.display.set_mode((720,480))
    menu=GameMenu(surface)
    #menu.load_main_menu()
    while True:   
        events = pygame.event.get()  
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
        if menu.main_menu.is_enabled():
            menu.main_menu.update(events)
            menu.main_menu.draw(surface)

        if menu.main_menu.get_current() == menu.game_screen:
            surface.fill('black')
            menu.game_screen.draw(surface)
            #menu.game_screen.force_surface_cache_update()
            #menu.game_screen.force_surface_update()

        pygame.display.flip()
        pygame.display.update()