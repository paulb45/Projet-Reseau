from graphic.mainSurface import MainSurface
from logic.game import Game
from logic.grid import Grid
window = MainSurface()

# Gestion du menu ? -> où dans main surface


while True:
    # Jouer la journée de logic
    game.bob_play()
    
    # Gestion graphique
    window.run(game.grid.map)
