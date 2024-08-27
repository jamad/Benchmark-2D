#from settings import *
import pygame
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

class SpriteUnit(pygame.sprite.Sprite):
    def __init__(self, handler, x, y):
        self.handler = handler
        self.x, self.y = x, y
        super().__init__(handler.group)
        self.image_ind = randrange(len(handler.images))
        self.image = handler.images[self.image_ind]
        self.rect = self.image.get_rect()
        self.vel_x, self.vel_y = self.get_vel(), self.get_vel()
        self.angle = 0
        self.rot_vel = self.get_vel()

    def rotate(self):
        self.angle += self.rot_vel * self.handler.app.dt
        self.image = self.handler.rot_cache[self.image_ind][
            int(生成数 * (self.angle % 360) / 360)]
        self.rect = self.image.get_rect()

    def translate(self):
        self.x += self.vel_x * self.handler.app.dt
        self.y += self.vel_y * self.handler.app.dt
        if self.x < 0 or self.x > 画面幅:
            self.vel_x *= -1
        if self.y < 0 or self.y > 画面高:
            self.vel_y *= -1

    def get_vel(self):
        return randrange(-SPEED, SPEED)

    def update(self):
        self.translate()
        self.rotate()
        self.rect.center = self.x, self.y


class SpriteHandler:
    def __init__(self, app):
        self.app = app
        self.images = [pygame.image.load(path).convert_alpha() for path in pathlib.Path(SPRITE_DIR_PATH).rglob('*.png')]
        self.rot_cache = self.get_rot_cache()
        self.group = pygame.sprite.Group()
        self.sprites = [SpriteUnit(self, 画面幅 // 2, 画面高 // 2)]

    def get_rot_cache(self):
        rot_cache = {}
        for i, image in enumerate(self.images):
            rot_cache[i] = []
            for angle in range(生成数):
                rot_img = pygame.transform.rotate(image, angle * 360 / 生成数)
                rot_cache[i].append(rot_img)
        return rot_cache

    def on_mouse_press(self):
        mouse_button = pygame.mouse.get_pressed()
        if mouse_button[0]:
            x, y = pygame.mouse.get_pos()
            for i in range(生成数):
                self.sprites.append(SpriteUnit(self, x, y))
        elif mouse_button[2]:
            for i in range(生成数):
                if len(self.sprites):
                    sprite = self.sprites.pop()
                    sprite.kill()


    def update(self):
        self.group.update()

    def draw(self):
        self.group.draw(self.app.画面)

class App:
    def __init__(self):
        pygame.init()
        self.画面 = pygame.display.set_mode(WIN_SIZE)
        self.クロック = pygame.time.Clock()
        self.フォント = ft.SysFont('Verdana', FONT_SIZE)
        self.dt = 0.0
        self.管理者 = SpriteHandler(self)

    def update(self):
        pygame.display.flip()
        self.管理者.update()
        self.dt = self.クロック.tick() * 0.001

    def draw(self):
        self.画面.fill('black')
        self.管理者.draw()
        
        fps = f'{self.クロック.get_fps() :.0f} FPS | {len(self.管理者.sprites)} SPRITES'
        self.フォント.render_to(self.画面, (0, 0), text=fps, fgcolor='green', bgcolor='black')

    def check_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif e.type == pygame.MOUSEBUTTONDOWN:
                self.管理者.on_mouse_press()

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()

App().run()






















