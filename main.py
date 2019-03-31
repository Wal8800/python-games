import pygame
import datetime
from shapely.geometry import Polygon


class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.jumpCount = 10

    def draw(self, win):
        pygame.draw.rect(win, (255, 0, 0),
                         (self.x, self.y, self.width, self.height))


class enemy(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5

    def draw(self, win):
        pygame.draw.rect(win, (0, 255, 0),
                         (self.x, self.y, self.width, self.height))

    def hit(self):
        print(datetime.datetime.now())


def redrawGameWindow():
    win.fill((0, 0, 0))
    man.draw(win)
    enemy.draw(win)
    pygame.display.update()


# mainloop
pygame.init()

win_width = 500
win_height = 480
win = pygame.display.set_mode((win_width, win_height))

pygame.display.set_caption("006")
man = player(0, 420, 50, 50)
enemy = enemy(210, 440, 30, 30)
is_game_running = True

clock = pygame.time.Clock()
while is_game_running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_game_running = False

    keys = pygame.key.get_pressed()

    man_shape = Polygon([
        (man.x, man.y),
        (man.x + man.width, man.y),
        (man.x, man.y + man.height),
        (man.x + man.width, man.y + man.height)
    ])

    enemy_shape = Polygon([
        (enemy.x, enemy.y),
        (enemy.x + enemy.width, enemy.y),
        (enemy.x, enemy.y + enemy.height),
        (enemy.x + enemy.width, enemy.y + enemy.height)
    ])
    if man_shape.intersects(enemy_shape):
        enemy.hit()

    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel

    if keys[pygame.K_RIGHT] and man.x < 500 - man.width - man.vel:
        man.x += man.vel

    if not(man.isJump):
        if keys[pygame.K_SPACE]:
            man.isJump = True
    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -= (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10

    redrawGameWindow()

pygame.quit()
