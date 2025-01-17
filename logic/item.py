

class Item():

    actual_local_id = 0

    def __init__(self, local_item=True, player_id=0, item_id=0):
        if local_item:
            self.id = player_id*10**10 + Item.actual_local_id
            Item.actual_local_id += 1
        else:
            self.id = item_id

    def get_id(self):
        return self.id