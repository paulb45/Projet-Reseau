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
        self.game_is_on = False
        self.zoom_slider_event = pygame.event.Event(pygame.USEREVENT+1,message= 'zoommustchange')
        self.volume_change_event = pygame.event.Event(pygame.USEREVENT+2,message= 'volumemustchange')
        self.surface = surface
        self.myfont=pygame_menu.font.FONT_MUNRO
        self.myfontsize = 30
        self.mytheme1 = pygame_menu.themes.THEME_SOLARIZED.copy()
        self.mytheme1.background_color=(0, 0, 0 ,0)
        self.mytheme1.widget_alignment = pygame_menu.locals.ALIGN_RIGHT
        self.mytheme1.widget_font = self.myfont
        self.mytheme1.widget_font_color = "Cyan"
        self.mytheme1.widget_font_size = self.myfontsize
        self.mytheme1.widget_title_font = self.myfont
        self.mytheme1.title = False
        self.mytheme2 = pygame_menu.themes.THEME_SOLARIZED.copy()
        self.mytheme2.background_color=(15,20,50)
        self.mytheme2.widget_alignment = pygame_menu.locals.ALIGN_CENTER
        self.mytheme2.widget_font = self.myfont
        self.mytheme2.widget_font_size = self.myfontsize
        self.mytheme2.widget_title_font = self.myfont
        self.mytheme2.title = False
        pygame_menu.themes.THEME_BLUE.widget_font_size = self.myfontsize
        pygame_menu.themes.THEME_BLUE.widget_font = self.myfont
        # pygame_menu.themes.THEME_BLUE.widget_font_color = (0,0,0)
       
        #CONSTANT FOR MULTIPLAYER MENU :
        self.credit_max = 100

        #CONSTANT FOR SKINS
        #BUG : Le skin christmas n'apparait pas, je l'enlève et je le remettrais quand j'aurais trouvé le problème
        #self.skins = [ ('default', ''), ('christmas', ''), ('pirate', ''), ('space', ''), ('halloween', '')]
        self.skins = [ ('default', ''), ('pirate', ''), ('space', ''), ('halloween', '')]
        self.main_menu = pygame_menu.Menu('EVOlution',pygame.display.get_surface().get_width(), pygame.display.get_surface().get_height(),theme=self.mytheme2)
        self.game_screen = pygame_menu.Menu('Gaming',pygame.display.get_surface().get_width(), pygame.display.get_surface().get_height(),theme=self.mytheme1)
        self.new_game = pygame_menu.Menu('New Game', pygame.display.get_surface().get_width(), pygame.display.get_surface().get_height(),theme=self.mytheme2)
        self.host_or_client_menu = pygame_menu.Menu('host_or_client_menu', pygame.display.get_surface().get_width(), pygame.display.get_surface().get_height(),theme=self.mytheme2)

        self.main_menu.add.label('Evolutionnary game of life',font_size=self.myfontsize*2,align=pygame_menu.locals.ALIGN_CENTER)
        self.main_menu.add.vertical_margin(50)
        self.main_menu.add.button('SinglePlayer', self.new_game,align=pygame_menu.locals.ALIGN_CENTER)
        self.main_menu.add.button('Multiplayer', self.host_or_client_menu,align=pygame_menu.locals.ALIGN_CENTER)
        self.main_menu.add.button('Quitter', pygame.QUIT,align=pygame_menu.locals.ALIGN_CENTER)

        self.main_menu.draw(self.surface)

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
        self.quitbutton = self.game_screen.add.button('Quitter', pygame_menu.events.EXIT,background_color=(200,200,200,25))
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
 
        self.new_game.add.vertical_margin(30)
        self.new_game.add.text_input('Largeur de la carte :', default=str(N),textinput_id='map_width',input_type=pygame_menu.locals.INPUT_INT)
        self.new_game.add.text_input('Hauteur de la carte :', default=str(M),textinput_id='map_height',input_type=pygame_menu.locals.INPUT_INT)
        self.new_game.add.text_input('Population de depart :', default=str(pop_init),textinput_id='population_bob',input_type=pygame_menu.locals.INPUT_INT)
        self.new_game.add.text_input('Nouriture par jour :', default=Config.quantity_food,textinput_id='daily_food',input_type=pygame_menu.locals.INPUT_INT)
        self.new_game.add.text_input('Mouvement de bob :', default='1',textinput_id='movement_bob',input_type=pygame_menu.locals.INPUT_INT)
        # self.new_game.add.text_input('Vision de bob :', default='1',textinput_id='vision_bob',input_type=pygame_menu.locals.INPUT_INT)
        self.new_game.add.text_input('Masse de bob :', default='1',textinput_id='mass_bob',input_type=pygame_menu.locals.INPUT_INT)
        self.new_game.add.text_input('Energie de la nourriture :', default=str(init_energy_food),textinput_id='energy_food',input_type=pygame_menu.locals.INPUT_INT)
        # self.new_game.add.text_input('Energy des parent apres reproduction :', default='100',textinput_id='energy_after_mating',input_type=pygame_menu.locals.INPUT_INT)
        # self.new_game.add.text_input('Energie necessaire pour ce cloner :', default='200',textinput_id='energy_to_clone',input_type=pygame_menu.locals.INPUT_INT)
        # self.new_game.add.text_input('Energie du bob enfant :', default='100',textinput_id='bob_child_energy',input_type=pygame_menu.locals.INPUT_INT)
        self.new_game.add.toggle_switch('Bouger avec la souris ? :', False, toggleswitch_id='move_with_mouse')
        self.new_game.add.selector('Skin :', self.skins, selector_id='theme_selector')
        self.new_game.add.button('Jouer', lambda : self.change_game_is_on("singleplayer"))
        self.new_game.add.vertical_margin(10)
        self.new_game.add.button("Restaurer les valeurs d'origine", self.new_game.reset_value)
        self.new_game.add.button('Retourner au menu principal', pygame_menu.events.BACK)
        self.new_game.add.button('Quitter', pygame.QUIT)
        self.new_game.add.vertical_margin(10)

        #Menu multi 
        self.caracteristic_selector_host = pygame_menu.Menu('caracteristic_selector', pygame.display.get_surface().get_width(), pygame.display.get_surface().get_height(),theme=self.mytheme2)
        self.caracteristic_selector_client = pygame_menu.Menu('caracteristic_selector', pygame.display.get_surface().get_width(), pygame.display.get_surface().get_height(),theme=self.mytheme2)

        #Menu pour choisir si on host ou pas :
        self.host_or_client_menu.add.button("Hosting Game", self.create_caracteristic_selector(self.caracteristic_selector_host, True))
        self.host_or_client_menu.add.button("Joining Game", self.create_caracteristic_selector(self.caracteristic_selector_client, False))
        self.host_or_client_menu.add.button('Retour au menu principal', pygame_menu.events.BACK)
        
        

    #Fonction pour récupérer les données sélectionnées dans les menus. 
    #Arg : str "singleplayer" ou "multiplayer"
    def data_fun(self, game_type) -> None:
        """
        Register game options
        """
        match game_type:
            case "singleplayer":
                data = self.new_game.get_input_data()
                print("DATA SINGLEPLAYER : " + str(data))
                Config.width_map = data['map_width']
                Config.height_map = data['map_height']
                Config.hosting = True
                Config.singleplayer = True
            case "multiplayer/hosting":
                data = self.caracteristic_selector_host.get_input_data()
                Config.width_map = data['map_width']
                Config.height_map = data['map_height']
                Config.hosting = True
                print("DATA MULTIPLAYER HOSTING : " + str(data))

            case "multiplayer/joining":
                data = self.caracteristic_selector_client.get_input_data()
                print("DATA MULTIPLAYER JOINING : " + str(data))
                Config.host_ip = data['host_ip']
                Config.hosting = False
        Config.sprite_path = f"sprites/{data['theme_selector'][0][0]}/"
        Config.P0 = int(round(data['population_bob']))
        Config.quantity_food = int(round(data['daily_food']))
        Config.energy_food = int(round(data['energy_food']))
        Config.bob_speed = int(round(data['movement_bob']))
        Config.move_with_cursor = data['move_with_mouse']
        # Variables d'interface
        Config.screen_size = [ np.ceil(tile_size*(Config.width_map+Config.height_map)/2 / i) for i in range(1,3)]
        Config.screen_size[0] += 2*Config.interface_x_offset
        Config.screen_size[1] += 2*Config.interface_y_offset
        print(data)

    #Méthode qui wrap la méthode change_game_is_on et dont le but est de checker si les valeurs des sliders dépassent le seuil autorisé. 
    def check_and_change_game_is_on(self, game_type: str):
        if game_type == "multiplayer/hosting":
            sliders = {
            'population_bob': self.caracteristic_selector_host.get_widget('population_bob'),
            'daily_food': self.caracteristic_selector_host.get_widget('daily_food'),
            'movement_bob': self.caracteristic_selector_host.get_widget('movement_bob'),
            'masse_slider': self.caracteristic_selector_host.get_widget('masse_slider'),
            'energy_food': self.caracteristic_selector_host.get_widget('energy_food')
            }
            selector = self.caracteristic_selector_host

        else :
            sliders = {
            'population_bob': self.caracteristic_selector_client.get_widget('population_bob'),
            'daily_food': self.caracteristic_selector_client.get_widget('daily_food'),
            'movement_bob': self.caracteristic_selector_client.get_widget('movement_bob'),
            'masse_slider': self.caracteristic_selector_client.get_widget('masse_slider'),
            'energy_food': self.caracteristic_selector_client.get_widget('energy_food')
            }
            selector = self.caracteristic_selector_client
       
        total = sum(int(slider.get_value()) for slider in sliders.values())
        if not (total <= self.credit_max):
            print("ERREUR : Le crédit maximal autorisé est dépassé")
            selector.add.label(
                f"La somme des sliders ({total}) dépasse la limite ({self.credit_max}) !", 
                font_size=20, 
                margin=(0, 20),
                selectable=False
            )
            return '' #peut-être mettre un retour d'erreur quand on aura une vrai gestion d'erreur.
        else : 
            print ("Credit max respecté")
            self.change_game_is_on(game_type)


    #gametype : soit singleplayer soit multiplayer
    def change_game_is_on(self, game_type: str):
        self.data_fun(game_type)
        if self.main_menu.get_current() == self.game_screen:
            pygame_menu.events.BACK

        self.game_is_on = not self.game_is_on

    #méthode pour récupérer le type de sélecteur de caractéristique en fonction du boolean hosting
    def create_caracteristic_selector(self, caracteristic_selector, hosting : bool):
        #MENU POUR CHOISIR LES CARACTERISTIQUE DE SA TRIBUT EN MULTIJOUEUR, AVEC UNE LIMITE DE CREDIT credit_max

        caracteristic_selector.add.label('Credits : ' + str(self.credit_max))
        caracteristic_selector.add.vertical_margin(30)
        if hosting: #L'hote a la possibilité de changer la taille de la carte, contrairement aux clients. 
            game_status = "hosting"
            caracteristic_selector.add.text_input('Largeur de la carte :', default=str(N),textinput_id='map_width',input_type=pygame_menu.locals.INPUT_INT)
            caracteristic_selector.add.text_input('Hauteur de la carte :', default=str(M),textinput_id='map_height',input_type=pygame_menu.locals.INPUT_INT)
        else :
            game_status = "joining"
            caracteristic_selector.add.text_input("IP de l'host :", default=str("127.0.0.1"),textinput_id='host_ip')
        caracteristic_selector.add.range_slider(
        'Population de depart :',
        rangeslider_id = 'population_bob',
        default=20,
        range_values= (1,100),
        range_box_enabled= False,
        increment=1,
        onchange=lambda value: int(round(value)),
        value_format=lambda x: str(int(round(x)))
        )
        caracteristic_selector.add.range_slider(
        'Nourriture par jour :',
        rangeslider_id = 'daily_food',
        default=28,
        range_values= (1,100),
        range_box_enabled= False,
        increment=1,
        onchange=lambda value: int(round(value)),
        value_format=lambda x: str(int(round(x)))
        )
        caracteristic_selector.add.range_slider(
        'Mouvement des bobs :',
        rangeslider_id = 'movement_bob',
        default=1,
        range_values= (1,100),
        range_box_enabled= False,
        increment=1,
        onchange=lambda value: int(round(value)),
        value_format=lambda x: str(int(round(x)))
        )
        caracteristic_selector.add.range_slider(
        'Masse des bobs :',
        rangeslider_id = 'masse_slider',
        default=1,
        range_values= (1,100),
        range_box_enabled= False,
        increment=1,
        onchange=lambda value: int(round(value)),
        value_format=lambda x: str(int(round(x)))
        )
        caracteristic_selector.add.range_slider(
        'Energie de la nourriture :',
        rangeslider_id = 'energy_food',
        default=30,
        range_values= (1,100),
        range_box_enabled= False,
        increment=1,
        onchange=lambda value: int(round(value)),
        value_format=lambda x: str(int(round(x)))
        )
        caracteristic_selector.add.toggle_switch('Bouger avec la souris ? :', False, toggleswitch_id='move_with_mouse')
        caracteristic_selector.add.selector('Skin :', self.skins, selector_id='theme_selector')
        caracteristic_selector.add.button('Jouer', lambda : self.check_and_change_game_is_on("multiplayer/" + game_status))
        caracteristic_selector.add.vertical_margin(10)
        caracteristic_selector.add.button("Restaurer les valeurs d'origine", self.new_game.reset_value)
        caracteristic_selector.add.button('Retour', pygame_menu.events.BACK)
        caracteristic_selector.add.button('Quitter', pygame.QUIT)
        caracteristic_selector.add.vertical_margin(10)
        return caracteristic_selector



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
        
