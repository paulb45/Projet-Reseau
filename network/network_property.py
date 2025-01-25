from collections import defaultdict
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from logic.bob import Bob
from logic.food import Food
from config import Config




class Network_property:
    """
    Propriétés réseaux : 

    Les propriétés réseaux représente l'appartenance à un joueur d'une case de la grille. 
    Si la case [x,y] appartiens au joueur, le dictionnaire np_grid aura pour valeur 1
    Sinon, le dictionnaire aura une valeur par défaut (0).
    """

    #network_property_grid : contient l'information d'appartenance des cases de la grilles. 
    np_grid = defaultdict(lambda: int())
    wait_anp_grid = {lambda: list()}

    @staticmethod
    def init_np_grid(grid):
        """Initialise np_grid when you host the game. All cases have to be initialized when hosting

        Returns:
            void
        """
        #Je vois pas d'autre moyen de parcourir toute la map pour l'initalisation au début malheuresement. 
        for x in range(Config.height_map):
            for y in range (Config.width_map):
               Network_property.add_appartenance(x,y)
    
    @staticmethod
    def get_np_grid():
        """Obtenir le contenu de np_grid

        Returns:
            defaultdict
        """
        return Network_property.np_grid
    
    @staticmethod
    def add_appartenance(x,y):
        """Ajouter une appartenance sur la case de coordonnée x,y

        Returns:
            void
        """
        Network_property.np_grid[(x,y)] = 1

    @staticmethod
    def remove_appartenance(x,y):
        """Enlève l'appartenance sur la case de coordonnée x,y

        Returns:
            void
        """
        del Network_property.np_grid[(x,y)]
    
    @staticmethod
    def get_appartenance(x,y):
        """Demande le status d'appartenance de la case. 
        Returns:
            boolean
        """
        return not Network_property.np_grid[(x,y)] == 0

if __name__ == '__main__':
    #test
    print(Network_property.np_grid)
    Network_property.add_appartenance(5,6)
    Network_property.add_appartenance(2,3)
    print(Network_property.get_np_grid())
    print(Network_property.get_appartenance(3,4))
    print(Network_property.get_appartenance(2,3))