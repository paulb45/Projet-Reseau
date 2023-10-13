class GRID():
    def __init__(self,N,M,tiles):
        self.tiles=tiles
        self.N=N
        self.M=M
        self.grid = [[None for _ in range(M)] for _ in range(N)]
    def get_N(self):
        return self.N
    def get_M(self):
        return self.M
    def set_N(self,nv_N):
        self.N = nv_N
    def set_M(self,nv_M):
        self.M = nv_M
    

    def scan_around(position, distance):
        pass
    def get_position(self,obj):
        for key, bobs in self.grid.items():
            for bob in bobs:
                if id(bob) == id(obj):
                    return key  # Retourne les coordonnées (x, y) d'objet recherché
        return None  # Retourne None si l'objet n'est pas trouvé

        
    def get_bobs(self,x,y):
        key = (x, y)
        return self.grid.get(key, [])  # Retourne la liste des objets à la clé (x, y), ou une liste vide s'il n'y a pas d'objet à cet endroit
    def update_size(self,N,M):
        self.N=N
        self.M=M
        
        