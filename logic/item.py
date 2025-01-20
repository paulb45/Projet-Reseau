

class Item():

    actual_local_id = 1

    def __init__(self, local_item=True, player_id=0, item_id=0):
        self.player_id = player_id
        self.local = local_item

        if local_item:
            self.id = self.player_id*10**10 + Item.actual_local_id
            Item.actual_local_id += 1
        else:
            self.id = item_id

    def get_id(self):
        return self.id

    def is_local(self):
        return self.local