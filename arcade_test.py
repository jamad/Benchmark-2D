import arcade
import pathlib
from random import randrange

WIN_SIZE = 画面幅, 画面高 = 1600, 900
SPRITE_DIR_PATH = 'W:/Benchmark-2D/assets/sprites'
FONTS_DIR_PATH = 'W:/Benchmark-2D/assets/fonts'
FONT_SIZE = 40
SPEED = 200
クリック毎の生成数 = 100

class スプライト(arcade.Sprite):
    def __init__(self, handler, x, y):
        super().__init__()
        self.handler = handler
        self.position=(x,y)
        self.image_ind = randrange(len(handler.images)) 
        self.texture = handler.images[self.image_ind]
        self.angle = 0
        self.rot_vel = self.get_vel()
        self.vel_x, self.vel_y = self.get_vel(), self.get_vel()

    def get_vel(self):
        return randrange(-SPEED, SPEED)

    def translate(self):
        self.position=(self.position[0]+self.vel_x * self.handler.app.経過時間, self.position[1]+self.vel_y * self.handler.app.経過時間)
        if not (0<=self.position[0]<=画面幅):self.vel_x *= -1
        if not (0<=self.position[1]<=画面高):self.vel_y *= -1

    def rotate(self):
        self.angle += self.rot_vel * self.handler.app.経過時間

    def update(self, delta_time = 0):  # delta_time を追加
        self.rotate()
        self.translate()    
        #self.position=(self.x,self.y)

class スプライト管理:
    def __init__(self, アプリ ):
        self.app = アプリ 
        self.images = self.get_images()
        self.sprites = arcade.SpriteList(use_spatial_hash=False)
        self.sprites.append(スプライト(self, 画面幅 // 2, 画面高 // 2))

    def add_sprite(self, x, y):
        for _ in range(クリック毎の生成数):
            self.sprites.append(スプライト(self, x, y))

    def get_images(self):
        return [arcade.load_texture(str(path)) for path in pathlib.Path(SPRITE_DIR_PATH).rglob('*.png') ]

    def update(self):
        self.sprites.update()

    def draw(self):
        self.sprites.draw()

class 俺アプリ (arcade.Window):
    def __init__(self):
        super().__init__(*WIN_SIZE, center_window=True, antialiasing=False)
        self.経過時間 = 0.0
        self.文字 = arcade.Text(text='text', x=0, y=画面高 - FONT_SIZE,font_size=FONT_SIZE, color=arcade.color.GREEN, bold=True)
        self.sprite_handler = スプライト管理(self)
        self.spritecount=1

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.sprite_handler.add_sprite(x, y)
            self.spritecount+=クリック毎の生成数
        elif button == arcade.MOUSE_BUTTON_RIGHT:            
            count=min(クリック毎の生成数,len(self.sprites))
            for i in range(count):self.sprites.pop()
            self.spritecount-=count

    def on_update(self, delta_time):
        self.sprite_handler.update()
        self.経過時間 = delta_time

    def on_draw(self):
        self.clear()
        self.sprite_handler.draw()
        self.文字.text = f'{1 // self.経過時間} FPS | {self.spritecount} SPRITES'
        self.文字.draw()

app = 俺アプリ()
app.run()
