from ursina import *

class Menu(Entity):
    def __init__(self, actions, **kwargs):#змінна кількіть агрументів(kwagrs)
        super().__init__(parent = camera.ui,ignore_paused = True, **kwargs)

        self.main_menu = Entity(parent =self, enabled = True)
        self.bg = Sprite(parent =self.main_menu,scale = 0.1, texture = "assets/bag.jpg", color = color.dark_gray, z = 1)

