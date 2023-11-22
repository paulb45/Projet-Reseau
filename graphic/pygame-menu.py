import pygame
import pygame_menu

pygame.init()
surface = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
myfont=pygame_menu.font.FONT_MUNRO
myfontsize = 30
window_size = surface.get_size()

def launch_simulation():
    pass

mytheme = pygame_menu.themes.THEME_ORANGE.copy()
mytheme.background_color=(0, 0, 0 ,0)
mytheme.widget_alignment = pygame_menu.locals.ALIGN_RIGHT
mytheme.widget_font =myfont
mytheme.widget_font_size = myfontsize
mytheme.widget_title_font = myfont
pygame_menu.themes.THEME_BLUE.widget_font_size = myfontsize
pygame_menu.themes.THEME_BLUE.widget_font = myfont

game_screen = pygame_menu.Menu('Gaming',window_size[0],window_size[1],theme=mytheme)
game_screen.add.button('Quit', pygame_menu.events.EXIT)

start = pygame_menu.Menu('New Game',window_size[0],window_size[1],theme=pygame_menu.themes.THEME_GREEN)
start.add.text_input('Population de départ :', default='100')
start.add.text_input('Nouriture de départ :', default='100')
start.add.text_input('movement de bob :', default='1')
start.add.button('Quit', pygame_menu.events.EXIT)
start.add.button('start', game_screen)
start.center_content()

load = pygame_menu.Menu('New Game',window_size[0],window_size[1],theme=pygame_menu.themes.THEME_SOLARIZED)
load.add.vertical_margin(50)
quitbutton = load.add.button('Quit', pygame_menu.events.EXIT)
startbutton = load.add.button('Start',game_screen)

main_menu = pygame_menu.Menu('EVOlution',window_size[0],window_size[1],theme=pygame_menu.themes.THEME_BLUE)

main_menu.add.button('new game', start)
main_menu.add.button('load game', load)
main_menu.add.button('Option', start)
main_menu.add.button('Quit', pygame_menu.events.EXIT)



    
if __name__ == '__main__':
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                break

        # Draw the menu
        surface.fill((75, 0, 50))

        main_menu.update(events)
        main_menu.draw(surface)

        pygame.display.flip()
