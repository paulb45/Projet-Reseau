

class Item():

    actual_id = 0

    def __init__(self):
        self.id = Item.actual_id
        Item.actual_id += 1

    def get_id(self):
        return self.id