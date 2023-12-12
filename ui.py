from ursina import *


class MenuButton(Button):
    def __init__(self, text, action, x,y,parent, **kwargs):
        super().__init__(text, on_click = action,parent = parent, 
                        color = color.rgb(133,133,133), texture = 'assert/btn.png', 
                        scale = (0.5,0.125),text_size = 2,text_color=color.white,
                        pressed_scale = 1.05,x=x,y=y,origin=(0,0), **kwargs)


class Menu(Entity):
    def __init__(self, actions, **kwargs):#змінна кількіть агрументів(kwagrs)
        super().__init__(parent = camera.ui,ignore_paused = True, **kwargs)

        self.main_menu = Entity(parent =self, enabled = True)
        self.bg = Sprite(parent =self.main_menu,scale = 0.1, texture = "assets/bag.jpg", color = color.dark_gray, z = 1)

        Text.default_font = 'assets/Minecraft-font.ttf'
        
        Text("Minecraft",scale = 3,parent = self.main_menu, y = 0.3, x = 0, origin = (0, 0))
        
        self.btns = [
            MenuButton("Start", actions[0], x = 0 ,y = 0.1,parent= self.main_menu),
            MenuButton("Save", actions[1], x = 0 ,y = -0.05,parent= self.main_menu),
            MenuButton("New Game", actions[2], x = 0 ,y = -0.2,parent= self.main_menu),
            MenuButton("Quit", actions[3], x = 0 ,y = -0.35,parent= self.main_menu),
        ]
