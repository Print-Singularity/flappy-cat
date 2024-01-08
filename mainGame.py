import pygame
import random
import time

pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()

# Font
font = pygame.font.SysFont('Bauhaus 93', 63)
font, font2 = pygame.font.SysFont('Arial', 72), pygame.font.SysFont('Arial', 36)
font3 = pygame.font.SysFont('Arial', 64)

# Variables
WIDTH = 800
HEIGHT = 600
FPS = 60
ground_scroll = 0
scroll_speed = 5
title = font.render('Cat fly', True, (0, 0, 0), None)
caption = font2.render('Press SPACE to Start', True, (0, 0, 0), None)
caption1 = font2.render('You die', True, (0, 0, 0), None)
pygame.display.set_caption('Cat Fly')
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
start = False
run = True
fly = False
game_over = False
pipe_gap = 250
time_spaw = 2500
last_pipe = pygame.time.get_ticks()
score = 0
died = False
HIT = pygame.mixer.Sound("img\media_hit.wav")
keepCoin = pygame.mixer.Sound("img\media_point.wav")
SPAWNCOIN = pygame.USEREVENT
pygame.time.set_timer(SPAWNCOIN, 500)

# Load images
bg = pygame.image.load('img\BG1.png')
bg = pygame.transform.scale(bg, (800, 600))
ground_img = pygame.image.load(r'img\floor.png')
img_player = pygame.image.load('img\cat.png')
player_dead = pygame.image.load("img\cat1.png")
img_coin = pygame.image.load("img\coin1.png")
img_coin = pygame.transform.scale(img_coin, (20, 20))

def text_score(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# restart_button = Button(score, 600, 50, 150, 50, GREEN, RED)


class Cat(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img\cat.png").convert()
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH - 750
        self.rect.bottom = HEIGHT / 2
        self.image.set_colorkey(BLACK)
        self.vel = 0

    def update(self):
        if fly == True:
            self.vel += 0.5
            if self.rect.bottom < 500:
                self.rect.y += self.vel

            keystate = pygame.key.get_pressed()
            if keystate[pygame.K_SPACE]:
                self.vel = -6

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img\pipe-green.png')
        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]
        self.rect.right = 0
        if position == 1:
            self.image = pygame.transform.flip(self.image, True, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
        if position == -1:
            self.rect.topleft = [x, y + int(pipe_gap / 2)]

    def update(self):
        self.rect.x -= scroll_speed

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = img_coin
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = random.randrange(200, HEIGHT)
        self.speedx = scroll_speed

    def update(self):
        self.rect.x -= self.speedx



all_sprite = pygame.sprite.Group()
player = pygame.sprite.Group()
cat = Cat()
player.add(cat)

pipe = pygame.sprite.Group()
coin = pygame.sprite.Group()
Obj_coin = Coin()
coin.add(Obj_coin)
   
while run:
    screen.blit(bg, (0, 0))
    screen.blit(caption, (100, 300))
    screen.blit(title, (100, 100))
    screen.blit(player_dead, (100, WIDTH / 2))
    screen.blit(player_dead, (300, WIDTH / 2))
    screen.blit(player_dead, (500, WIDTH / 2))
    
    if run == False:
        screen.blit(bg, (0, 0))
        screen.blit(caption1, (100, 300))
        screen.blit(title, (100, 100))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run == False
            pygame.quit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if start == False:
                    start = True
                if fly == False:
                    fly = True
        if start == True:
            if event.type == SPAWNCOIN:
                c = Coin()
                all_sprite.add(c)
                coin.add(c)

    if start:
        screen.blit(bg, (0, 0))
        player.draw(screen)
        player.update()
        pipe.draw(screen)
        coin.draw(screen)
        coin.update()
        screen.blit(ground_img, (ground_scroll, 500))
        text_score(str(score), font, BLACK, int(WIDTH / 2), 20)

        if pygame.sprite.groupcollide(player, pipe, False, False):
            game_over = True
            start = False
            fly = False
            HIT.play()
            time.sleep(2)
            pygame.quit()
            

        if pygame.sprite.groupcollide(player, coin, False, True):
            score += 1
            keepCoin.play()
            print(score)
            
        
        if cat.rect.bottom >= 500:
            game_over = True
            fly = False
            start = False
            HIT.play()
            time.sleep(2)
            pygame.quit()
        
        if game_over == False and fly == True:
            time_now = pygame.time.get_ticks()
            if time_now - last_pipe > time_spaw:
                pipe_height = random.randint(-100, 100)
                Objbtm_pipe = Pipe(WIDTH, int(HEIGHT / 2) + pipe_height, -1)
                Objtop_pipe = Pipe(WIDTH, int(HEIGHT / 2) + pipe_height, 1)
                pipe.add(Objbtm_pipe)
                pipe.add(Objtop_pipe)
                last_pipe = time_now
            screen.blit(ground_img, (ground_scroll, 500))
            ground_scroll -= scroll_speed
            if abs(ground_scroll) > 35:
                ground_scroll = 0
            pipe.update()
            

    # restart_button.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()


# Kob

