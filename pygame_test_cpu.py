#from settings import *
import pygame as pg# pip install pygame
import pygame.freetype as ft
import sys

import pathlib
from random import randrange, choice

import os
current_directory = os.path.dirname(os.path.abspath(__file__)) # 現在のスクリプトのディレクトリを取得
#SPRITE_DIR_PATH = current_directory+'/sprites'
SPRITE_DIR_PATH =r'D:\myworks\project_github\practicePython\_folder_for_the_file_on_root\arcade/sprites'.replace('\\','/')
print(SPRITE_DIR_PATH)

WIN_SIZE = 画面幅, 画面高 = 1600, 900
FONT_SIZE = 40
SPEED = 200
生成数 = 100


class SpriteUnit(pg.sprite.Sprite):
    def __init__(self, handler, x, y):
        self.handler = handler
        super().__init__(handler.group)
        self.image =  choice(handler.images)
        self.rect = self.image.get_rect()
        self.x, self.y = x, y
        self.angle = 0
        self.rot_vel = self.get_vel()
        self.vel_x, self.vel_y = self.get_vel(), self.get_vel()

    def get_vel(self):
        return randrange(-SPEED, SPEED)

    def translate(self):
        self.x += self.vel_x * self.handler.app.dt
        self.y += self.vel_y * self.handler.app.dt
        if self.x < 0 or self.x > 画面幅:
            self.vel_x *= -1
        if self.y < 0 or self.y > 画面高:
            self.vel_y *= -1

    def rotate(self):
        self.angle += self.rot_vel * self.handler.app.dt
        self.image = pg.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect()

    def update(self):
        self.translate()
        self.rotate()
        self.rect.center = self.x, self.y


class SpriteHandler:
    def __init__(self, app):
        self.app = app
        self.images = self.load_images()
        self.group = pg.sprite.Group()
        self.sprites = [SpriteUnit(self, 画面幅 // 2, 画面高 // 2)]

    def add_sprite(self, x, y):
        for i in range(生成数):
            self.sprites.append(SpriteUnit(self, x, y))

    def del_sprite(self):
        for i in range(生成数):
            if len(self.sprites):
                sprite = self.sprites.pop()
                sprite.kill()

    def load_images(self):
        paths = [item for item in pathlib.Path(SPRITE_DIR_PATH).rglob('*.png') if item.is_file()]
        return [pg.image.load(str(path)).convert_alpha() for path in paths]

    def update(self):
        self.group.update()

    def draw(self):
        self.group.draw(self.app.screen)

    def on_mouse_press(self):
        mouse_button = pg.mouse.get_pressed()
        if mouse_button[0]:
            x, y = pg.mouse.get_pos()
            self.add_sprite(x, y)
        elif mouse_button[2]:
            self.del_sprite()


class App:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(WIN_SIZE)
        print(type(self.screen))
        self.clock = pg.time.Clock()
        self.font = ft.SysFont('Verdana', FONT_SIZE)
        self.sprite_handler = SpriteHandler(self)
        self.dt = 0.0

    def update(self):
        self.sprite_handler.update()
        pg.display.flip()
        self.dt = self.clock.tick() * 0.001

    def draw_fps(self):
        fps = f'{self.clock.get_fps() :.0f} FPS | {len(self.sprite_handler.sprites)} SPRITES'
        self.font.render_to(self.screen, (0, 0), text=fps, fgcolor='green', bgcolor='black')

    def draw(self):
        self.screen.fill('black')
        self.sprite_handler.draw()
        self.draw_fps()

    def check_events(self):
        for e in pg.event.get():
            if e.type == pg.QUIT or (e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif e.type == pg.MOUSEBUTTONDOWN:
                self.sprite_handler.on_mouse_press()

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    app = App()
    app.run()
