import arcade
import pathlib
from random import randrange,choice

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
        self.texture = choice(handler.images)
        self.angle = 0
        self.rot_vel = randrange(-SPEED, SPEED)
        self.vel_x, self.vel_y = randrange(-SPEED, SPEED),randrange(-SPEED, SPEED)

    
    def update(self, delta_time = 0):  # delta_time を追加
        self.angle += self.rot_vel * self.handler.app.経過時間# rotate
        self.position=(self.position[0]+self.vel_x * self.handler.app.経過時間, self.position[1]+self.vel_y * self.handler.app.経過時間)
        if not (0<=self.position[0]<=画面幅):self.vel_x *= -1# 反射
        if not (0<=self.position[1]<=画面高):self.vel_y *= -1# 反射

class スプライト管理:
    def __init__(self, アプリ ):
        self.app = アプリ 
        self.images = [*map(arcade.load_texture,pathlib.Path(SPRITE_DIR_PATH).rglob('*.png'))]
        self.sprites = arcade.SpriteList(use_spatial_hash=False)
        self.sprites.append(スプライト(self, 画面幅 // 2, 画面高 // 2))

    def add_sprite(self, x, y):
        for _ in range(クリック毎の生成数):
            self.sprites.append(スプライト(self, x, y))

    def update(self):
        self.sprites.update()

    def draw(self):
        self.sprites.draw()

class 俺アプリ (arcade.Window):
    経過時間 = 0.0

    def __init__(self):
        super().__init__(*WIN_SIZE, center_window=True, antialiasing=False)
        self.文字 = arcade.Text(text='text', x=0, y=画面高 - FONT_SIZE,font_size=FONT_SIZE, color=arcade.color.GREEN, bold=True)
        self.sprite_handler = スプライト管理(self)
        self.スプライト数=1

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.スプライト数+=クリック毎の生成数
            self.sprite_handler.add_sprite(x, y)
        elif button == arcade.MOUSE_BUTTON_RIGHT:            
            count=min(クリック毎の生成数,len(self.sprites))
            self.スプライト数-=count
            for i in range(count):self.sprites.pop()

    def on_update(self, delta_time):
        self.sprite_handler.update()
        self.経過時間 = delta_time

    def on_draw(self):
        self.clear()
        self.sprite_handler.draw()
        self.文字.text = f'{1 // self.経過時間} FPS | {self.スプライト数} SPRITES'
        self.文字.draw()

app = 俺アプリ()
app.run()
