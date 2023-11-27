from config import *

class Grid():
    def __init__(self):
        #self.tiles=tiles
        #self.grid = [[None for _ in range(M)] for _ in range(N)]
        
        self.grid={} # une grid à un attribut grid ??? -> c'est pas très logique d'avoir à faire grid.grid pour avoir une grid...
    
    #aymen scan around fiha des erreurs katle3 des valeurs pas forcément correct
    #[0,1]->[(0, 0), (0, 2), (1, 0), (1, 1), (1, 2)] :/
    #[0,0] ->[(0, 1), (1, 0), (1, 1)] :/

    def scan_around(self,position, distance):
        x, y = position
        positions_disponibles = [] # SOUS FORME DE DICTIONNAIRE COMME LA CARTE !!!

        # NE PEUT PAS FONCTIONNER si x=0 et i<0 par exemple, ou si x=N et i>0 !!!
        for i in range(-distance, distance + 1):
            for j in range(-distance, distance + 1):
                new_x = x + i
                new_y = y + j

                # Vérification que la nouvelle position est à l'intérieur de la grille
                # et que x et y diffèrent, excluant ainsi la diagonale lorsque la distance vaut 1
                # LA DISTANCE SERA PAS TOUJOURS 1 !!!!!
                if distance == 1:
                    if (0 <= new_x < N) and (0 <= new_y < N) and (new_x != x or new_y != y): # Pourquoi cette dernière condition ?
                        positions_disponibles.append((new_x, new_y))
                else : 
                    # c'est exactement pareil qu'au dessus ?!
                    if (0 <= new_x < N) and (0 <= new_y < N) :
                        positions_disponibles.append((new_x, new_y))
        # A REVOIR ENTIEREMENT
        return positions_disponibles
            
    def get_position(self,obj):
        # A vérif
        for key, i in self.grid.items():
            for bob in i:
                if id(bob) == id(obj):
                    return key  # Retourne les coordonnées (x, y) d'objet recherché
        return None  # Retourne None si l'objet n'est pas trouvé -> PAS OBLIGATOIRE

        
    def get_bobs(self,x,y):
        # A TESTER MAIS BIZARRE -> Pas de test d'instance
        key = (x, y)
        return self.grid.get(key, [])  # Retourne la liste des objets à la clé (x, y), ou une liste vide s'il n'y a pas d'objet à cet endroit      
        