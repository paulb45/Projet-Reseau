from turtle import width
import pygame
import pygame_menu
from pygame_menu import sound
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import *
#from graphic.interface import Interface

class GameMenu(pygame.Surface):

    def __init__(self, surface):
        super().__init__(pygame.display.get_surface().get_size())
        #self.interface = Interface
        #self.interface.load_images()
        # True si on est sur le jeu et false sinon
        self.game_is_on = False
        
        self.zoom_slider_event = pygame.event.Event(pygame.USEREVENT+1,message= 'zoommustchange')
        self.volume_change_event = pygame.event.Event(pygame.USEREVENT+2,message= 'volumemustchange')
        #self.engine=sound.Sound()
        #self.engine.set_sound(sound.SOUND_TYPE_CLICK_MOUSE,music_path +'mixkit-cool-interface-click-tone-2568.ogg')
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
        #self.mytheme2.widget_alignment = pygame_menu.locals.ALIGN_LEFT
        self.mytheme2.title = False
        pygame_menu.themes.THEME_BLUE.widget_font_size = self.myfontsize
        pygame_menu.themes.THEME_BLUE.widget_font = self.myfont
        
        self.main_menu = pygame_menu.Menu('EVOlution',pygame.display.get_surface().get_width(), pygame.display.get_surface().get_height(),theme=self.mytheme2)
        self.game_screen = pygame_menu.Menu('Gaming',pygame.display.get_surface().get_width(), pygame.display.get_surface().get_height(),theme=self.mytheme1)
        self.new_game = pygame_menu.Menu('New Game', pygame.display.get_surface().get_width(), pygame.display.get_surface().get_height(),theme=self.mytheme2)

        #self.load_new_game()
        #self.load_main_menu()
        #self.load_game_screen_menu()
        
        #self.main_menu.set_sound(self.engine,recursive=True)
        self.main_menu.add.label('Evolutionnary game of life',font_size=self.myfontsize*2,align=pygame_menu.locals.ALIGN_CENTER)
        self.main_menu.add.vertical_margin(50)
        self.main_menu.add.button('new game', self.new_game,align=pygame_menu.locals.ALIGN_CENTER)
        self.main_menu.add.vertical_margin(10)
        self.main_menu.add.button('Quit', pygame.QUIT,align=pygame_menu.locals.ALIGN_CENTER)
        self.main_menu.draw(self.surface)
        #self.main_menu.resize(pygame.display.get_surface().get_width(), pygame.display.get_surface().get_height())

        def zoom_changer(n):
            #print('the function was called')
            pygame.event.post(self.zoom_slider_event)
            
        def change_volume(n):
            pygame.mixer.music.set_volume( n /100)
        
        
        self.daydisplay = self.game_screen.add.label(' day : 0')
        self.daydisplay.translate(-20,0 )
        self.game_screen.add.vertical_margin(25)
        self.tickdisplay = self.game_screen.add.label('tick : 0')
        self.tickdisplay.translate(-20,0)
        self.game_screen.add.vertical_margin(25)
        self.quitbutton = self.game_screen.add.button('Quit', pygame_menu.events.EXIT,background_color=(200,200,200,25))
        self.quitbutton.translate(-20,0 )
        self.quitbutton.set_controls(keyboard=False)
        self.game_screen.add.vertical_margin(25)
        # self.optionbtn=self.game_screen.add.button('option', self.change_game_is_on, align=pygame_menu.locals.ALIGN_RIGHT,background_color=(200,200,200,25))
        # self.optionbtn.translate(-20,0)
        # self.optionbtn.set_controls(keyboard=False)
        self.game_screen.add.vertical_margin(pygame.display.get_surface().get_height()/3 +50)
        self.zoom_slider=self.game_screen.add.range_slider('zoom', 50, (0, 100), 1,rangeslider_id='zoom_slider',onchange= zoom_changer,value_format=lambda x: str(int(x)),background_color=(200,200,200,25))
        self.zoom_slider.translate(-20,0 )
        self.zoom_slider.set_controls(keyboard=False)
        self.game_screen.add.vertical_margin(25)
        self.volume_slider =self.game_screen.add.range_slider('volume',5, (0, 100), 1,rangeslider_id='volume_slider',onchange = change_volume ,value_format=lambda x: str(int(x)), background_color=(200,200,200,25))
        self.volume_slider.translate(-20,0 )
        self.volume_slider.set_controls(keyboard=False)
 

        #self.game_screen.resize(pygame.display.get_surface().get_width(), pygame.display.get_surface().get_height())
        # erreur en cas de récursion
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
        # self.new_game.add.button('start', self.game_screen)
        self.new_game.add.button('start', self.change_game_is_on)

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
            # Variables d'interface
            Config.screen_size = [ np.ceil(tile_size*(Config.width_map+Config.height_map)/2 / i) for i in range(1,3)]
            Config.screen_size[0] += 2*Config.interface_x_offset
            Config.screen_size[1] += 2*Config.interface_y_offset
            print(f"map: ({Config.width_map},{Config.height_map})")
        self.new_game.add.button('Store data', data_fun, button_id='store')
        self.new_game.add.button('Restore original values', self.new_game.reset_value)
        self.new_game.add.button('Return to main menu', pygame_menu.events.BACK)
        self.new_game.add.vertical_margin(10)
        #self.new_game.resize(pygame.display.get_surface().get_width(), pygame.display.get_surface().get_height())
        
    def change_game_is_on(self):
        if self.main_menu.get_current() == self.game_screen:
            pygame_menu.events.BACK

        self.game_is_on = not self.game_is_on
        
        #self.interface.generate_ground(self.interface.cut_in_image('Tileset.png', (pos_x_tile,pos_y_tile), (tileset_x_offset, tileset_y_offset)))
        #print("size change bich")

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