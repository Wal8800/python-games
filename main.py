import pygame
import datetime
from shapely.geometry import Polygon


class Player(object):
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

    def to_polygon(self):
        return Polygon([
            (self.x, self.y),
            (self.x + self.width, self.y),
            (self.x, self.y + self.height),
            (self.x + self.width, self.y + self.height)
        ])


class Enemy(object):
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

    def to_polygon(self):
        return Polygon([
            (self.x, self.y),
            (self.x + self.width, self.y),
            (self.x, self.y + self.height),
            (self.x + self.width, self.y + self.height)
        ])


def redrawGameWindow():
    win.fill((0, 0, 0))
    man.draw(win)
    for enemy in enemy_list:
        enemy.draw(win)
    pygame.display.update()


# mainloop
pygame.init()

win_width = 500
win_height = 480
win = pygame.display.set_mode((win_width, win_height))

pygame.display.set_caption("006")
man = Player(0, 420, 50, 50)
init_enemy = Enemy(win_width + 5, 440, 30, 30)
is_game_running = True

enemy_list = [
    init_enemy
]

clock = pygame.time.Clock()
spawn_count = 0
while is_game_running:
    clock.tick(60)
    spawn_count += 1
    if spawn_count >= 50:
        spawn_count = 0
        new_enemy = Enemy(win_width + 5, 440, 30, 30)
        enemy_list.append(new_enemy)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_game_running = False

    enemy_list = [enemy for enemy in enemy_list if enemy.x > -enemy.width]
    for enemy in enemy_list:
        if man.to_polygon().intersects(enemy.to_polygon()):
            enemy.hit()

        enemy.x -= 5

    keys = pygame.key.get_pressed()
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
