class ActionBuffer:
    buffer_placement = {}
    buffer_move = {}
    buffer_eat = {}
    buffer_attack = {}
    buffer_dead = {}
    buffer_ANP = {}

    @staticmethod
    def get_buffer_placement() -> dict:
        """Obtenir le contenu du buffer des placements de nouveau bob

        Returns:
            dict: {id_bob : (coordonnées, type, énergie, masse, mouvement)}
        """
        temp = ActionBuffer.buffer_placement
        ActionBuffer.buffer_placement = {}
        return temp

    @staticmethod
    def get_buffer_move() -> dict:
        """Obtenir le contenu du buffer des déplacements des bobs de A à B

        Returns:
            dict: {id_bob : (coordonnées A, coordonnées B)}
        """
        temp = ActionBuffer.buffer_move
        ActionBuffer.buffer_move = {}
        return temp

    @staticmethod
    def get_buffer_eat() -> dict:
        """Obtenir le contenu du buffer des action "manger" des bobs

        Returns:
            dict: {id_bob : (coordonnées de l'action, énergie gagnée, id de l'objet mangé)}
        """
        temp = ActionBuffer.buffer_eat
        ActionBuffer.buffer_eat = {}
        return temp

    @staticmethod
    def get_buffer_attack() -> dict:
        """Obtenir le contenu du buffer des attaques

        Returns:
            dict: {id_bob : (coordonnées de l'attaque, id de l'adversaire)}
        """
        temp = ActionBuffer.buffer_attack
        ActionBuffer.buffer_attack = {}
        return temp

    @staticmethod
    def get_buffer_dead() -> dict:
        """Obtenir le contenu du buffer des morts

        Returns:
            dict: {id_bob : coordonnées}
        """
        temp = ActionBuffer.buffer_dead
        ActionBuffer.buffer_dead = {}
        return temp


    @staticmethod
    def add_placement(item_id:int, type_item:str, pos:tuple, energy:int, mass:int, speed:int):
        """Ajouter un item à notre jeu

        Args:
            item_id (int): id de l'item à ajouter
            type_item (str): type de l'item (B ou F)
            pos (tuple): coordonnées de l'item
            energy (int): énergie de l'item
            mass (int): masse de l'item (si le type est B)
            speed (int): vitesse de l'item (si le type est B)
        """
        ActionBuffer.buffer_placement[item_id] = (pos, type_item, energy, mass, speed)

    @staticmethod
    def add_move(p1:tuple, p2:tuple, bob_id:int):
        """Ajouter un déplacement d'un bob au buffer

        Args:
            p1 (tuple): position A
            p2 (tuple): position B
        """
        ActionBuffer.buffer_move[bob_id] = (p1, p2)

    @staticmethod
    def add_eat(bob_id:int, pos:tuple, energy_get:int, food_id:int):
        """Ajouter une action "manger" d'un bob sur une nourriture

        Args:
            bob_id (int): id du mangeur
            pos (tuple): coordonnées de l'action
            energy_get (int): énéergies gagnées
            food_id (int): id de la nourriture
        """
        ActionBuffer.buffer_eat[bob_id] = (pos, energy_get, food_id)

    @staticmethod
    def add_attack(bob_id:int, pos:tuple, bob_cible_id:int):
        """Ajouter une action "attaquer" d'un bob sur un autre bob

        Args:
            bob_id (int): id de l'attaquant
            pos (tuple): coordonnées de l'attaque
            bob_cible_id (int): id de la victime
        """ 
        ActionBuffer.buffer_attack[bob_id] = (pos, bob_cible_id)

    @staticmethod
    def add_dead(item_id:int, pos:tuple):
        """Ajouter une disparition d'un item

        Args:
            item_id (int): id de l'item disparu
            pos (tuple): coordonnées de la disparition
        """
        ActionBuffer.buffer_dead[item_id] = pos

    def add_ANP_request(pos : tuple, id_of_asker : int):
        """Ajouter une requête ANP au buffer pour une case

        Args:
            pos (tuple): coordonnées de la case 
        """
        ActionBuffer.buffer_ANP[pos] = id_of_asker