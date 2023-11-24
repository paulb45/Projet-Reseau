class Grid():
    def __init__(self,N,M):
        #self.tiles=tiles
        self.N=N
        self.M=M
        #self.grid = [[None for _ in range(M)] for _ in range(N)]
        self.grid={}
    def get_N(self):
        return self.N
    def get_M(self):
        return self.M
    def set_N(self,nv_N):
        self.N = nv_N
    def set_M(self,nv_M):
        self.M = nv_M
    

    def scan_around(self,position, distance):
        x, y = position
        positions_disponibles = []

        for i in range(-distance, distance + 1):
            for j in range(-distance, distance + 1):
                new_x = x + i
                new_y = y + j

                # Vérification que la nouvelle position est à l'intérieur de la grille
                # et que x et y diffèrent, excluant ainsi la diagonale lorsque la distance vaut 1
                if distance == 1:
                    if 0 <= new_x < self.N and 0 <= new_y < self.N and (new_x != x or new_y != y):
                        positions_disponibles.append((new_x, new_y))
                else : 
                    if 0 <= new_x < self.N and 0 <= new_y < self.N :
                        positions_disponibles.append((new_x, new_y))

        return positions_disponibles
            
    def get_position(self,obj):
        for key, i in self.grid.items():
            for bob in i:
                if id(bob) == id(obj):
                    return key  # Retourne les coordonnées (x, y) d'objet recherché
        return None  # Retourne None si l'objet n'est pas trouvé

        
    def get_bobs(self,x,y):
        key = (x, y)
        return self.grid.get(key, [])  # Retourne la liste des objets à la clé (x, y), ou une liste vide s'il n'y a pas d'objet à cet endroit
    def update_size(self,N,M):
        self.N=N
        self.M=M
        
        