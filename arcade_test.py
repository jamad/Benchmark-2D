import arcade
import pathlib
from random import randrange, choice

WIN_SIZE = 画面幅, 画面高 = 1600, 900
SPRITE_DIR_PATH = 'W:/Benchmark-2D/assets/sprites'
FONT_SIZE = 40
SPEED = 200
生成数 = 100

class スプライト(arcade.Sprite):
    def __init__(self, images, x, y):
        super().__init__()
        self.center_x, self.center_y = x, y
        self.texture = choice(images)
        self.angle = 0
        self.rv = randrange(-SPEED, SPEED)
        self.vx = randrange(-SPEED, SPEED)
        self.vy = randrange(-SPEED, SPEED)

    def update(self, dt):
        self.angle += self.rv * dt
        self.center_x += self.vx * dt
        self.center_y += self.vy * dt
        if not (0 <= self.center_x <= 画面幅): self.vx *= -1
        if not (0 <= self.center_y <= 画面高): self.vy *= -1

class 俺アプリ(arcade.Window):
    def __init__(self):
        super().__init__(*WIN_SIZE, center_window=True, antialiasing=False)
        self.images = [*map(arcade.load_texture, pathlib.Path(SPRITE_DIR_PATH).rglob('*.png'))]
        self.sprites = arcade.SpriteList(use_spatial_hash=False)
        self.sprites.append(スプライト(self.images, 画面幅 // 2, 画面高 // 2))
        self.文字 = arcade.Text(text='text', x=0, y=画面高 - FONT_SIZE, font_size=FONT_SIZE, color=arcade.color.GREEN, bold=True)
        self.スプライト数 = 1

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.スプライト数 += 生成数
            for _ in range(生成数): self.sprites.append(スプライト(self.images, x, y))
        elif button == arcade.MOUSE_BUTTON_RIGHT:
            count = min(生成数, len(self.sprites))
            self.スプライト数 -= count
            for _ in range(count):self.sprites.pop()

    def on_update(self, delta_time):
        self.sprites.update(delta_time)
        self.文字.text = f'{1//delta_time} FPS | {self.スプライト数} SPRITES'

    def on_draw(self):
        self.clear()
        self.sprites.draw()
        self.文字.draw()

俺アプリ().run()