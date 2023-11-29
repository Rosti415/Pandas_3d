from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import basic_lighting_shader, unlit_shader
from ursina.shaders import lit_with_shadows_shader

from perlin_noise import PerlinNoise
import random
import pickle

from ui import Menu

app = Ursina()

block_textures = [
    load_texture("assets/grass.png"), #0
    load_texture("assets/gold.png"),#1
    load_texture("assets/stone.png"),#2
    load_texture("assets/lava.png"),#3
    load_texture("assets/Barril.png"),
    load_texture("assets/ww.jpg"),
]

footstep_sound = Audio('assets/minecraft-footsteps.mp3', loop = False, autoplay=False)
punch_sound = Audio('assets/punch.wav', loop = False, autoplay=False)
bg_music = Audio('assets/crafting_game_music.mp3',loop = True, autoplay=True)

class Sky(Entity):
    def __init__(self):
        super().__init__(
            parent = scene,
            model = "sphere",
            texture = load_texture("assets/sky.jpg"),
            scale = 500,
            double_sided = True,
            shader = unlit_shader,
            eternal = True,
        )

class Arm(Entity):
    def __init__(self):
        super().__init__(
            parent = camera.ui,
            model = "assets/arm",
            texture = load_texture("assets/arm.png"),
            scale = 0.2,
            rotation = Vec3(150, -10, 0),
            position = Vec2(0.4, -0.6),
            shader = basic_lighting_shader,
            eternal = True,
        )
        
    def active(self):
        self.position = Vec2(0.3, -0.5)
    
    def passive(self):
        self.position = Vec2(0.4, -0.6)

class Voxel(Button):
    id = 0

    def __init__(self,position = (0,0,0), id = 0):
        super().__init__(
            parent = scene,
            model = "assets/block",
            texture = block_textures[id],
            scale = 0.5,
            position = position,
            origin_y = 0.5,
            color = color.color(0,0, random.uniform(0.9, 1.0)),
            highlight_color = color.gray,
            shader = basic_lighting_shader  
        )
        self.id = id

    def input(self, key):
        if self.hovered:
            if key == "left mouse down":
                arm.active()
                punch_sound.play()
                block = Voxel(position=self.position + mouse.normal, id = Voxel.id)
                game.blocks.append(block)
            elif key == "right mouse down":
                arm.active()
                punch_sound.play()
                destroy(self)#видаляє блок з гри
                game.blocks.remove(self)
            else:
                arm.passive()

        for i in range(1,len(block_textures)+1):
            if key == str(i):
                Voxel.id = i-1
                arm.texture = block_textures[Voxel.id]


class Tree (Entity):
    def __init__(self,position = (0,0,0)):
        super().__init__(
            parent = scene,
            model = "assets/tree/scene",
            scale = 5,
            position = position,
            origin_y = 0.5,
            shader = basic_lighting_shader,
            )
        
class GameController(Entity):# клас для всього руху гри(контролю або налаштування)
    def __init__(self, add_to_scene_entities=True, **kwargs):
        super().__init__(add_to_scene_entities, **kwargs)
        scene.fog_density = 0.025
        scene.fog_color = color.rgb(62, 103, 169)
        player.jumping = True
        player.jump_height = 3
        player.jump_up_duration = 0.3
        player.speed = 10
        player.start_pos = player.position
        #window.fullscreen = True
        self.blocks = []
        #self.menu = Menu(actions=[self.load, self.save, self.new_game, application.quit])
        #arm.disable()
        #application.paused = True
        '''for z in range(-40, 41, 10):
            for x in range(-20, 21, 10):
                tree = Tree(position=(x, 3, z))
                self.blocks.append(tree)'''

    def update(self):# стала методом після додавання в клас
        if player.y < -50:
            player.position = player.start_pos
        if held_keys['shift']:
            player.speed = 10
        else:
            player.speed = 5

        if held_keys['a'] or held_keys['d'] or held_keys['w'] or held_keys['s']:
            footstep_sound.play()
    
    def input (self, key):
        if key == 'k':
            self.save()
        if key == 'n':
            self.new_game()
        if key == 'l':
            self.load()

    def new_game(self):
        for block in self.blocks:
            destroy(block)#очищує певний обєкт
        
        self.blocks.clear()# очищуємо список

        noise = PerlinNoise(octaves=4, seed=random.randint(1,1000))# зміна рельєфу за допомогою перліна і random

        for z in range(-20,20):
            for x in range(-20,20):
                height = noise([x * 0.02, z * 0.02])
                height = math.floor(height * 7.5)
                block = Voxel(position=(x, height, z))
                self.blocks.append(block)
                rand_k = random.randint(0,100)
                if rand_k == 2:
                    tree = Tree(position=(x,height,z))

        player.position = (0,30, 0)

    def save(self):
        with open("save.data", "wb") as file:
            k = len(self.blocks)# зберігаємо кількість блоків
            pickle.dump(k, file)
            for block in self.blocks:
                pickle.dump(block.position, file)
                pickle.dump(block.id, file)

            pickle.dump(player.position, file)

    def load(self):
        for block in self.blocks:
            destroy(block)
        self.blocks.clear()

        with open("save.data", "rb") as file:#видаляємо страрі блоки і додаєм нові і додаєм їх в список
            k = pickle.load(file)
            for i in range(k):
                pos = pickle.load(file)
                id = pickle.load(file)
                block = Voxel(position=pos,id =id)
                self.blocks.append(block)

            player.position = pickle.load(file)
            player.start_pos = player.position

sun = DirectionalLight(y = 20, z= 10)# додавання тіні
sun.look_at(Vec3(1, -1, -1))
sky = Sky()
player = FirstPersonController()
arm = Arm()



game = GameController()
game.load()
app.run()