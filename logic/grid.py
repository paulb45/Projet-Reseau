class Grid():
    def __init__(self,N,M):
        
        self.N=N
        self.M=M
        self.map={}
        
    
        """GETTERS"""
    def get_N(self):
        return self.N
    def get_M(self):
        return self.M
    
    """SETTERS"""
    def set_N(self,nv_N):
        self.N = nv_N
    def set_M(self,nv_M):
        self.M = nv_M
    

    
    
        """ la fonction get_position permet de donner la position dans la grille d'un objet passe en parametres
        """
    def get_position(self,obj):
        
        for key, itms in self.map.items():
            for itm in itms:
                if id(itm) == id(obj):
                    return key  # Retourne les coordonnées (x, y) d'objet recherché
        return None  # Retourne None si l'objet n'est pas trouvé

        """
        #Retourne la liste des objets à la clé (x, y), ou une liste vide s'il n'y a pas d'objet à cet endroit
        """
    
    def get_items(self,x,y):
        position = (x, y)
        return self.map[position]  
    """    def scan_around(self,grid):
        mon_cercle=[]
        x,y=self.last_move
        for i in range(-self.perception,self.perception):
            x+=i
            for j in range(-self.perception,self.perception):
                if i+j<self.perception:
                    y+=j
                    mon_cercle.append((x,y))
                    
            return mon_cercle                     
"""         
        