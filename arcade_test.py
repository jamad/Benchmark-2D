import arcade
import pathlib
from random import randrange

WIN_SIZE = WIN_W, WIN_H = 1600, 900
SPRITE_DIR_PATH = 'W:/Benchmark-2D/assets/sprites'
FONTS_DIR_PATH = 'W:/Benchmark-2D/assets/fonts'

FONT_SIZE = 40
SPEED = 200
NUM_SPRITES_PER_CLICK = 100
NUM_ANGLES = 180

class SpriteUnit(arcade.Sprite):
    def __init__(self, handler, x, y):
        super().__init__()
        self.handler = handler
        self.position=(x,y)
        #self.x, self.y = x, y

        self.image_ind = randrange(len(handler.images)) 
        self.texture = handler.images[self.image_ind]
        self.angle = 0
        self.rot_vel = self.get_vel()
        self.vel_x, self.vel_y = self.get_vel(), self.get_vel()

    def get_vel(self):
        return randrange(-SPEED, SPEED)

    def translate(self):
        self.position=(self.position[0]+self.vel_x * self.handler.app.dt, self.position[1]+self.vel_y * self.handler.app.dt)
        if not (0<=self.position[0]<=WIN_W):self.vel_x *= -1
        if not (0<=self.position[1]<=WIN_H):self.vel_y *= -1

    def rotate(self):
        self.angle += self.rot_vel * self.handler.app.dt

    def update(self, delta_time = 0):  # delta_time を追加
        self.rotate()
        self.translate()    
        #self.position=(self.x,self.y)

class SpriteHandler:
    def __init__(self, app):
        self.app = app
        self.images = self.get_images()
        self.sprites = arcade.SpriteList(use_spatial_hash=False)
        self.sprites.append(SpriteUnit(self, WIN_W // 2, WIN_H // 2))

    def add_sprite(self, x, y):
        for i in range(NUM_SPRITES_PER_CLICK):
            self.sprites.append(SpriteUnit(self, x, y))

    def get_images(self):
        paths = [item for item in pathlib.Path(SPRITE_DIR_PATH).rglob('*.png') if item.is_file()]
        return [arcade.load_texture(str(path)) for path in paths]

    def update(self):
        self.sprites.update()

    def draw(self):
        self.sprites.draw()

class App(arcade.Window):
    def __init__(self):
        super().__init__(*WIN_SIZE, center_window=True, antialiasing=False)
        self.dt = 0.0
        self.text = arcade.Text(text='text', x=0, y=WIN_H - FONT_SIZE,font_size=FONT_SIZE, color=arcade.color.GREEN, bold=True)
        self.sprite_handler = SpriteHandler(self)
        self.spritecount=1

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.sprite_handler.add_sprite(x, y)
            self.spritecount+=NUM_SPRITES_PER_CLICK
        elif button == arcade.MOUSE_BUTTON_RIGHT:            
            count=min(NUM_SPRITES_PER_CLICK,len(self.sprites))
            for i in range(count):self.sprites.pop()
            self.spritecount-=count

    def on_update(self, delta_time):
        self.sprite_handler.update()
        self.dt = delta_time

    def on_draw(self):
        self.clear()
        self.sprite_handler.draw()
        self.text.text = f'{1 // self.dt} FPS | {self.spritecount} SPRITES'
        self.text.draw()

app = App()
app.run()
