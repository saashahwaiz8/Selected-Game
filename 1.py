from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader
from perlin_noise import PerlinNoise

app = Ursina()

def update():
    global selected_block
    if held_keys['tab']:
        sword.visible = False
        camera.z = -5
    if held_keys['control']:
        sword.visible = True
        camera.z = 0
    if held_keys['1']:
        selected_block = "my_grass"
    if held_keys['2']:
        selected_block = "dirt"
    if held_keys['3']:
        selected_block = "stone"
    if held_keys['4']:
        selected_block = "bedrock"
    if held_keys['left mouse'] or held_keys['right mouse']:
        sword.active()
    else:
        sword.passive()
        

block_textures = {
    "grass": load_texture("my_grass.png"),
    "dirt": load_texture("dirt.png"),
    "stone": load_texture("stone.png"),
    "bedrock": load_texture("bedrock.png")
}

selected_block = "my_grass"

class Voxel(Button):
    def __init__(self,position=(0,0,0)):
        super().__init__(
            parent = scene,
            color = color.gray,
            model = 'cube',
            texture = selected_block,
            collider = 'box',
            shader = lit_with_shadows_shader,
            highlight_color = color.lime,
            position = position
        )

    def input(self, key):
        if self.hovered:
            if key == "left mouse down":
                destroy(self)
            if key == 'right mouse down':
                voxel = Voxel(position = self.position + mouse.normal)

noise = PerlinNoise(octaves=2, seed=6627)
amp = 3
freq = 24
width = 50

for po in range(width*width):
    voxel = Voxel()
    voxel.x = floor(po/width)
    voxel.z = floor(po % width)
    voxel.y = floor(noise([voxel.x/freq, voxel.z/freq]) * amp)
    
class Cow(Entity):
    def __init__(self):
        super().__init__(
            model = 'cow',
            texture = 'Image_0_2',
            scale = (1.3,1.3,1.3),
            position = (5,-0.5,8),
            rotation = (0,-120,0)
        )

class Sword(Entity):
    def __init__(self):
        super().__init__(
            parent = camera.ui,
            model = 'blade',
            texture = 'sword',
            scale = (0.2,0.15),
            position = (0.5,-0.6),
            rotation = (30,-40)
        )

    def active(self):
        self.position = Vec2(0.3,-0.5)
        self.rotation = Vec2(30,-40)

    def passive(self):
        self.position = Vec2(0.5,-0.6)
        self.rotation = Vec2(30,-40)

player = FirstPersonController(model = 'cube', texture = 'white_cube', shader = lit_with_shadows_shader, color = color.gray)
Sky(texture = 'castaway_sky')
window.fullscreen = True

cow = Cow()
sword = Sword()

player.position = (19,20,10)
app.run()
