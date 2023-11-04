from pygame import Surface

class CameraController:

    def __init__(self, window_width, window_height, main_surface):
        self.main_surface = main_surface
        self.window_width = window_width
        self.window_height = window_height

        self.viewpoint = Surface((window_width, window_height))

        self.zoom_max = 0
        self.zoom_min = 0

        self.move_step = 0


    def get_viewpoint(self) -> Surface:
        pass


    def zoom_in(self) -> Surface:
        pass


    def zoom_out(self) -> Surface:
        pass


    def move_right(self) -> Surface:
        pass


    def move_left(self) -> Surface:
        pass


    def move_top(self) -> Surface:
        pass


    def move_bottom(self) -> Surface:
        pass