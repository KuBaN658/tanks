import math
import random
from random import choice

import pygame

FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600


class Ball:
    def __init__(self, screen: pygame.Surface, x=80, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30
        self.ay = 0.5

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.x += self.vx
        self.y += self.vy
        self.vx *= 0.98
        if self.y >= 550 - self.r:
            self.vy = -(self.vy + 1) * 0.85
            if abs(self.vy) < 1:
                self.vy = self.ay = 0
        if self.x + self.r > 790:
            self.vx = - self.vx
        self.vy += self.ay

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )
        pygame.draw.circle(
            self.screen,
            BLACK,
            (self.x, self.y),
            self.r, 1
        )


    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        distance = math.hypot(self.x - obj.x, self.y - obj.y)
        if distance <= self.r + obj.r:
            return True
        else:
            return False


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.pos = (1, 1)

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = round(self.f2_power * math.sin(self.an))
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan((event.pos[1]-450) / (event.pos[0]-20.00001))
            self.pos = event.pos
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        width_gun = 10
        distance_to_aim = math.hypot(20 - self.pos[0], 420 - self.pos[1])
        scalar = distance_to_aim / self.f2_power
        x1 = 20
        y1 = 420
        x2 = 20 + (self.pos[0] - 20) / scalar
        y2 = 420 + (self.pos[1] - 420) / scalar
        scalar = distance_to_aim / width_gun
        x3 = x2 + (420 - self.pos[1]) / scalar
        y3 = y2 + (self.pos[0] - 20) / scalar
        x4 = x1 + (420 - self.pos[1]) / scalar
        y4 = y1 + (self.pos[0] - 20) / scalar
        pygame.draw.polygon(screen, self.color,  ((x1, y1), (x2, y2), (x3, y3), (x4, y4)))

    # caunt_point_polygon(x0, y0, x1, y1, width):
    # hypotenuse = ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5
    # x = abs(y1 - y0) / hypotenuse * width
    # y = abs(x1 - x0) / hypotenuse * width
    # x_point = x0 + x
    # if y0 < y1:
    #     y_point = y0 - y
    # else:
    #     y_point = y0 + y
    # coords_second = x_point, y_point
    # x_point = x1 + x
    # if y0 < y1:
    #     y_point = y1 - y
    # else:
    #     y_point = y1 + y
    # coords_first = x_point, y_point
    # coords = [coords_first, coords_second]
    # coords = [(x0, y0), (x1, y1)] + coords
    # return coords

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


class Target:
    def __init__(self, screen):
        self.screen = screen
        self.x = random.randint(600, 780)
        self.y = random.randint(300, 550)
        self.r = random.randint(2, 50)
        self.color = GREY
        self.live = 1
        self.points = 0
    # self.points = 0
    # self.live = 1
    # FIXME: don't work!!! How to call this functions when object is created?
    # self.new_target()

    def new_target(self, screen):
        self.screen = screen
        self.x = random.randint(600, 780)
        self.y = random.randint(300, 550)
        self.r = random.randint(2, 50)
        self.color = GREY
        self.live = 1
        self.points = 0

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )
        pygame.draw.circle(
            self.screen,
            BLACK,
            (self.x, self.y),
            self.r,
            1
        )


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Танчик")
bullet = 0
balls = []

clock = pygame.time.Clock()
gun = Gun(screen)
target = Target(screen)
finished = False

while not finished:
    screen.fill(WHITE)
    gun.draw()
    target.draw()
    for b in balls:
        b.draw()
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    for b in balls:
        b.move()
        if b.hittest(target) and target.live:
            target.live = 0
            target.hit()
            target.new_target(screen)
    gun.power_up()

pygame.quit()
