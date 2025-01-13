from logic.bob import Bob

class ActionBuffer:
    buffer = {}

    @staticmethod
    def get_buffer():
        temp = ActionBuffer.buffer
        ActionBuffer.buffer = {}
        return temp

    @staticmethod
    def add_move(p1, p2):
        b = Bob()
        b.set_last_move(p1)
        ActionBuffer.buffer[p2] = b 


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