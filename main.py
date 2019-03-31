from shapely.geometry import Polygon
import datetime
import pygame
import time


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


# mainloop
pygame.init()

win_width = 500
win_height = 480
black = (0, 0, 0)
white = (255, 255, 255)
red = (200, 0, 0)
green = (0, 200, 0)
bright_red = (255, 0, 0)
bright_green = (0, 255, 0)
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("006")
clock = pygame.time.Clock()


def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()


def game_intro():
    is_intro = True

    while is_intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        click = pygame.mouse.get_pressed()
        if click[0] == 1:
            break

        win.fill(black)
        largeText = pygame.font.Font('freesansbold.ttf', 32)
        TextSurf, TextRect = text_objects("Click To Play", largeText)
        TextRect.center = ((win_width/2), (win_height/2))
        win.blit(TextSurf, TextRect)
        pygame.display.update()
        clock.tick(15)


def button(msg, x, y, w, h, ic, ac):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(win, ac, (x, y, w, h))
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(win, ic, (x, y, w, h))
    smallText = pygame.font.SysFont("comicsansms", 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x+(w/2)), (y+(h/2)))
    win.blit(textSurf, textRect)

    return False


def quitgame():
    pygame.quit()
    quit()


def game_ended(time_score):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        win.fill(black)
        largeText = pygame.font.SysFont("comicsansms", 32)
        score_string = "Final Score: {0:.2f} seconds".format(time_score)
        TextSurf, TextRect = text_objects(score_string, largeText)
        mid_x = win_width/2
        mid_y = win_height/2 - 50
        TextRect.center = (mid_x, mid_y)
        win.blit(TextSurf, TextRect)

        button_width = 100
        button_height = 50
        again_clicked = button("Play Again", mid_x - 50 - button_width,
                               mid_y + 50,
                               button_width, button_height, green,
                               bright_green)
        quit_clicked = button("Quit", mid_x + 50, mid_y + 50, button_width,
                              button_height, red, bright_red)

        if again_clicked:
            return True

        if quit_clicked:
            return False

        pygame.display.update()
        clock.tick(60)


def game_loop():
    man_height = 50
    man_width = 50
    ground_thickness = 10
    man = Player(0, win_height - man_height -
                 ground_thickness, man_width, man_height)

    enemy_height = 30
    enemy_width = 30
    init_enemy = Enemy(win_width + 5, win_height - enemy_height -
                       ground_thickness, enemy_width, enemy_height)
    is_game_running = True

    enemy_list = [
        init_enemy
    ]

    spawn_count = 0
    starting_time = time.time()
    time_score = 0
    score_font = pygame.font.SysFont("comicsans", 30, True)
    while is_game_running:
        clock.tick(60)
        spawn_count += 1
        time_score = time.time() - starting_time
        if spawn_count >= 50:
            spawn_count = 0
            new_enemy = Enemy(win_width + 5, 440, 30, 30)
            enemy_list.append(new_enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        enemy_list = [enemy for enemy in enemy_list if enemy.x > -enemy.width]
        for enemy in enemy_list:
            if man.to_polygon().intersects(enemy.to_polygon()):
                return time_score

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

        # redrawing window
        win.fill((0, 0, 0))
        text = score_font.render("Time: {0:.2f}".format(time_score), 1, white)
        # centering score text in the middle
        text_x = win_width / 2 - text.get_width() / 2
        win.blit(text, (text_x, 10))
        man.draw(win)
        for enemy in enemy_list:
            enemy.draw(win)
        pygame.display.update()


game_intro()

is_playing = True
while is_playing:
    score = game_loop()
    is_playing = game_ended(score)

pygame.quit()
quit()
