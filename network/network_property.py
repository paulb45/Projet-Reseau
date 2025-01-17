from collections import defaultdict

#CONSTANTES :
CASE_VIDE = 1
BOB = 2
FOOD = 3


class Network_property:
    """
    Propriétés réseaux : 

    Les propriétés réseaux représente l'appartenance à un joueur d'une case de la grille. 
    Si la case [x,y] appartiens au joueur, le dictionnaire np_grid aura pour valeur un tuple (x, y) avec :
    x : le type d'objet sur la case (CASE_VIDE = 1, BOB = 2, FOOD = 3)
    y : info sur l'objet, la masse du bob et l'énergie de la food
    Sinon, le dictionnaire aura une valeur par défaut (0).
    """

    #network_property_grid : contient l'information d'appartenance des cases de la grilles. 
    np_grid = defaultdict(lambda: int())

    @staticmethod
    def get_np_grid():
        """Obtenir le contenu de np_grid

        Returns:
            defaultdict
        """
        return Network_property.np_grid

    @staticmethod
    def add_bob(x,y, masse):
        """Ajouter une appartenance sur la case de coordonnée x,y, avec un bob dessus

        Returns:
            void
        """
        Network_property.np_grid[(x,y)] = (BOB, masse)

    @staticmethod
    def add_food(x,y, energie):
        """Ajouter une appartenance sur la case de coordonnée x,y, avec de la food dessus

        Returns:
            void
        """
        Network_property.np_grid[(x,y)] = (FOOD, energie)
    
    @staticmethod
    def add_case(x,y):
        """Ajouter une appartenance sur la case de coordonnée x,y, avec une case dessus

        Returns:
            void
        """
        Network_property.np_grid[(x,y)] = (CASE_VIDE)

    @staticmethod
    def remove_appartenance(x,y):
        """Enlève l'appartenance sur la case de coordonnée x,y

        Returns:
            void
        """
        del Network_property.np_grid[(x,y)]

if __name__ == '__main__':
    #test
    print(Network_property.np_grid)
    Network_property.add_bob(1,2, 3)
    Network_property.add_food(3,4, 4)
    Network_property.add_case(5,6)
    print(Network_property.get_np_grid())
    Network_property.remove_appartenance(3,4)
    print(Network_property.get_np_grid())