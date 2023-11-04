import pygame
import pygame_menu

pygame.init()
surface = pygame.display.set_mode((1200, 800))

#main.mainloop(surface)

def launch_simulation():
    pass

def start_new_game():
    start = pygame_menu.Menu('New Game',800,600,theme=pygame_menu.themes.THEME_GREEN)
    start.add.text_input('Population de départ :', default='100')
    start.add.text_input('Nouriture de départ :', default='100')
    start.add.text_input('movement de bob :', default='1')
    start.add.button('back to main menue',main_menu)
    start.add.button('Quit', pygame_menu.events.EXIT)
    start.add.button('start',launch_simulation)
    start.center_content()
    start.mainloop(surface)

def load_old_game():
    load = pygame_menu.Menu('New Game',800,600,theme=pygame_menu.themes.THEME_SOLARIZED)
    load.add.button('back to main menue',main_menu, align=pygame_menu.locals.ALIGN_RIGHT)
    load.add.vertical_margin(50)
    quitbutton = load.add.button('Quit', pygame_menu.events.EXIT)
    startbutton = load.add.button('Start',launch_simulation)
    load.mainloop(surface)

def main_menu():
    main = pygame_menu.Menu('EVOlution', 800, 600,theme=pygame_menu.themes.THEME_BLUE)
    main.add.button('new game', start_new_game)
    main.add.button('load game', load_old_game)
    main.add.button('Option', start_new_game)
    main.add.button('Quit', pygame_menu.events.EXIT)
    main.mainloop(surface)
    
main_menu()
