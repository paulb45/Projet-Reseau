

class Item():

    actual_local_id = 1

    def __init__(self, local_item=True, player_id=0, item_id=0):
        self.player_id = player_id
        self.local = local_item

        if local_item:
            self.id = self.player_id*10**10 + Item.actual_local_id
            Item.actual_local_id = (Item.actual_local_id % 9999999999) + 1
        else:
            self.id = item_id

        # nombre de jours depuis que l'item a été vu (donc une action à été reçu depuis le réseau)
        self.nb_day_not_view = 0

    def get_id(self):
        """Obtenir l'id complet de l'item

        Returns:
            int: id sur max 15 chiffres
        """
        return self.id

    def is_local(self):
        return self.local

    def get_nb_day_not_view(self):
        """Obtenir le nombre de jours depuis que l'item a été vu
        """
        return self.nb_day_not_view

    def reset_nb_day_not_view(self):
        self.nb_day_not_view = 0

    def add_nb_day_not_view(self, nb_day):
        self.nb_day_not_view += nb_day

    def get_player_id(self):
        """Obtenir l'id du joueur

        Returns:
            int: id du joueur sur max 5 chiffres
        """
        return self.player_id

    def get_item_id(self):
        """Obtenir l'id de l'item sans l'id du joueur

        Returns:
            int: id sur max 10 chiffres
        """
        return self.id - self.player_id