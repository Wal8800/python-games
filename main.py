import pygame


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


def redrawGameWindow():
    win.fill((0, 0, 0))
    man.draw(win)
    pygame.display.update()


# mainloop
pygame.init()

win_width = 500
win_height = 480
win = pygame.display.set_mode((win_width, win_height))

pygame.display.set_caption("First Game")
man = player(200, 410, 64, 64)
run = True

clock = pygame.time.Clock()
while run:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

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
