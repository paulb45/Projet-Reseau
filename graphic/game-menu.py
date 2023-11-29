import pygame
import pygame_menu

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

        def gamescreenmenu(self):
            game_screen = pygame_menu.Menu('Gaming',window_size[0],window_size[1],theme=mytheme1)
            game_screen.add.button('Quit', pygame_menu.events.EXIT)
            game_screen.draw(surface)

        def startmenu(self):
            start = pygame_menu.Menu('New Game',window_size[0],window_size[1],theme= mytheme2)
            start.add.text_input('Population de départ :', default='100')
            start.add.text_input('Nouriture de départ :', default='100')
            start.add.text_input('movement de bob :', default='1')
            start.add.button('Quit', pygame_menu.events.EXIT)
            start.add.button('start', gamescreenmenu(surface))
            start.center_content()

        def loadmenu(self):
            load = pygame_menu.Menu('New Game',window_size[0],window_size[1],theme=mytheme2)
            load.add.vertical_margin(50)
            load.add.button('Quit', pygame_menu.events.EXIT)
            self.load.add.button('Start',gamescreenmenu(surface))

        def principal(self):
            self.main_menu = pygame_menu.Menu('EVOlution',window_size[0],window_size[1],theme=mytheme2)
            self.main_menu.add.button('new game', startmenu(surface))
            self.main_menu.add.button('load game', loadmenu)
            self.main_menu.add.button('Quit', pygame_menu.events.EXIT)
            self.main_menu.draw(surface)

    def event_menu(self,events):
        #self.main_menu.update(events)
        #self.main_menu.draw(surface)
    
if __name__ == '__main__':
    pygame.init()
    surface = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
    menu=Menu()
    while True:
        events = pygame.event.get()
        #menu.event_menu(events)
        #menu.main_menu.draw(surface)
        
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                break
        #main_menu.update(events)
        #surface.blit(menu,(0,0))
        pygame.display.flip()