import pygame
import pygame_menu

class Menu(pygame.Surface):

    def __init__(self, surface):
        super().__init__(pygame.display.get_surface().get_size())
        self.surface = surface
        self.myfont=pygame_menu.font.FONT_MUNRO
        self.myfontsize = 30
        self.mytheme1 = pygame_menu.themes.THEME_SOLARIZED.copy()
        self.mytheme1.background_color=(0, 0, 0 ,0)
        self.mytheme1.widget_alignment = pygame_menu.locals.ALIGN_RIGHT
        self.mytheme1.widget_font = self.myfont
        self.mytheme1.widget_font_size = self.myfontsize
        self.mytheme1.widget_title_font = self.myfont
        self.mytheme2 = pygame_menu.themes.THEME_SOLARIZED.copy()
        self.mytheme2.background_color=(15,20,50)
        self.mytheme2.widget_alignment = pygame_menu.locals.ALIGN_CENTER
        self.mytheme2.widget_font = self.myfont
        self.mytheme2.widget_font_size = self.myfontsize
        self.mytheme2.widget_title_font = self.myfont
        pygame_menu.themes.THEME_BLUE.widget_font_size = self.myfontsize
        pygame_menu.themes.THEME_BLUE.widget_font = self.myfont
        
        self.main_menu = pygame_menu.Menu('EVOlution',pygame.display.get_surface().get_width(), pygame.display.get_surface().get_height(),theme=self.mytheme2)
        self.game_screen = pygame_menu.Menu('Gaming',pygame.display.get_surface().get_width(), pygame.display.get_surface().get_height(),theme=self.mytheme1)
        self.new_game = pygame_menu.Menu('New Game', pygame.display.get_surface().get_width(), pygame.display.get_surface().get_height(),theme=self.mytheme2)
        
        self.load_new_game()
        self.load_main_menu()
        self.load_game_screen_menu()
        

    def load_main_menu(self):
        self.main_menu.add.button('new game', self.new_game)
        self.main_menu.add.button('Quit', pygame.QUIT)
        
    def load_game_screen_menu(self):
        self.game_screen.add.button('Quit', pygame_menu.events.EXIT)

    def load_new_game(self):
        self.new_game.add.text_input('Population de départ :', default='100')
        self.new_game.add.text_input('Nouriture de départ :', default='100')
        self.new_game.add.text_input('movement de bob :', default='1')
        self.new_game.add.button('Quit', pygame.QUIT)
        self.new_game.add.button('start', self.game_screen)
        self.new_game.center_content()

    def to_print(self, menu_name: str):
        match menu_name:
            case "main_menu":
                events =  pygame.event.get()
                self.main_menu.update(events)
                self.main_menu.draw(self.surface)
            case "game_screen":
                self.game_screen.draw(self.surface)
            case "new_game":
                self.new_game.draw(self.surface)
                
                
    
if __name__ == '__main__':
    pygame.init()
    surface = pygame.display.set_mode((720,480))
    menu=Menu(surface)
    
    
    
    while True:       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        menu.to_print("main_menu")          
        pygame.display.flip()
        pygame.display.update()