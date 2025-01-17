from collections import defaultdict

class Network_property:
    """
    Propriétés réseaux : 

    Les propriétés réseaux représente l'appartenance à un joueur d'une case de la grille. 
    Si la case [x,y] appartiens au joueur, le dictionnaire np_grid aura une valeur (1). 
    Sinon, le dictionnaire aura une valeur par défaut (0).
    """

    #network_property_grid : contient l'information d'appartenance des cases de la grilles. 
    np_grid = defaultdict(lambda: False)

    @staticmethod
    def get_np_grid():
        """Obtenir le contenu de np_grid

        Returns:
            defaultdict
        """
        temp = Network_property.np_grid
        Network_property.np_grid = defaultdict(lambda: False)
        return temp

    @staticmethod
    def set_appartenance(x,y, appartient : bool):
        """Ajouter une appartenance sur la case de coordonnée x,y

        Returns:
            void
        """
        Network_property.np_grid[(x,y)] = appartient

if __name__ == '__main__':
    #test
    print(Network_property.np_grid)
    Network_property.set_appartenance(1,2, True)
    print(Network_property.get_np_grid())