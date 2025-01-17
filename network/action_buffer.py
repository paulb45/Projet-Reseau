from collections import defaultdict

from logic.bob import Bob
from logic.grid import Grid

# class ActionBuffer:
#     buffer = Grid()

#     @staticmethod
#     def get_buffer():
#         """Obtenir le contenu du buffer

#         Returns:
#             Grid: buffer d'une grille 
#         """
#         temp = ActionBuffer.buffer
#         ActionBuffer.buffer = Grid()
#         return temp

#     @staticmethod
#     def add_move(p1, p2):
#         """Ajouter un déplacement d'un bob au buffer

#         Args:
#             p1 (tuple): position A
#             p2 (tuple): position B
#         """
#         b = Bob()
#         b.set_last_move(p1)
#         ActionBuffer.buffer.add_bob(p2, b)

class ActionBuffer:
    buffer = {}

    @staticmethod
    def get_buffer():
        """Obtenir le contenu du buffer

        Returns:
            Grid: buffer d'une grille 
        """
        temp = ActionBuffer.buffer
        ActionBuffer.buffer = {}
        return temp

    @staticmethod
    def add_move(p1, p2, bob_id):
        """Ajouter un déplacement d'un bob au buffer

        Args:
            p1 (tuple): position A
            p2 (tuple): position B
        """
        ActionBuffer.buffer[bob_id] = (p1, p2)


if __name__ == '__main__':
    ActionBuffer.add_move((0,0),(1,1))
    ActionBuffer.add_move((1,7),(4,9))
    print(ActionBuffer.get_buffer())
    ActionBuffer.add_move((4,8),(6,9))
    ActionBuffer.add_move((1,4),(9,6))
    print(ActionBuffer.get_buffer())
    ActionBuffer.add_move((4,0),(1,7))
    ActionBuffer.add_move((0,3),(1,9))
    ActionBuffer.add_move((0,8),(3,1))
    print(ActionBuffer.get_buffer())