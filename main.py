from pygame import *
from random import randint 

init()
back = (200, 255, 255)
win_width = 800
win_height = 600
window = display.set_mode((win_width, win_height))
player_l = [image.load('PlayerL1.png'), image.load('PlayerL2.png'), image.load('PlayerL3.png')]
player_r = [image.load('PlayerR1.png'), image.load('PlayerR2.png'), image.load('PlayerR3.png')]

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.left=False
        self.right= False
        self.count = 0
        

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):

    def update(self):
        keys = key.get_pressed()

        if keys[K_LEFT] :
            self.rect.x -= self.speed
            self.left = True
            self.right = False

        elif keys[K_RIGHT] :
            self.left = False
            self.right = True
            self.rect.x += self.speed
        else:
            self.right = self.left = False
            
    def animation(self):
        if self.left:
            self.count = (self.count + 1) % len(player_l)  
            window.blit(player_l[self.count], (self.rect.x, self.rect.y))
        elif self.right:
            self.count = (self.count + 1) % len(player_l)  
            window.blit(player_r[self.count], (self.rect.x, self.rect.y))
        else:
            self.count = (self.count + 1) % len(player_l)  
            window.blit(player_r[self.count], (self.rect.x, self.rect.y))

class Enemy(GameSprite): 
    def update(self): 
        self.rect.y += self.speed 
        global lost
        if self.rect.y > win_height: 
            self.rect.x = randint(80, win_width - 80) 
            self.rect.y = 0 
            lost = lost + 1



FPS = 40
bg = transform.scale(image.load("bg.png"), (win_width, win_height))
display.set_caption("WhirlyBird")

clock = time.Clock()

game = False
menu = True

platform_img = 'platform.png' 
spikes_img = 'spikes.png'

score = 0

font.init() 
font3 = font.Font(None, 36)
font2 = font.Font(None, 36) 
font1 = font.Font(None,100)

platform = sprite.Group() 
spike = sprite.Group() 

jumping = False
running = True
player = Player('PlayerR1.png', 5, 300, 85, 100, 10)
x_bg = 0
y_bg=0
jump_count=10
jump_height=10
while running:
    keys = key.get_pressed()

    for e in event.get():
        if e.type == QUIT:
            running = False
        elif  e.type==KEYDOWN :
            game = True
            menu = False
        elif e.type == K_SPACE:
            game = False
            menu = True
            

    if game:
        window.fill(back)
        window.blit(bg, (y_bg, y_bg))
        window.blit(bg, (y_bg+win_width, y_bg))
        y_bg=4
        
        text = font2.render("Рахунок:" + str(score), 1, (255, 255, 255)) 
        window.blit(text, (10, 20))

        player.update()
        player.animation()

        platforms = transform.scale(image.load("platform.png"), (100, 10))
        window.blit(platforms, (350, 300))

        spikes = transform.scale(image.load("spikes.png"), (100, 33))
        window.blit(spikes, (100, 300))

        if y_bg == win_width:
            y_bg=0
        elif not jumping:
            if keys[K_SPACE]:
                jumping = True
        else:
            if jump_count >= -jump_height:
                neg = 1
                if jump_count < 0:
                    neg = -1
                player.rect.y -= (jump_count ** 2) * 0.5 * neg
                jump_count -= 1
            else:
                jumping = False
                jump_count = jump_height

    if menu:
        window.fill(back)
        window.blit(bg, (y_bg, y_bg))
        window.blit(bg, (y_bg+win_width, y_bg))
        text = font2.render("WhirlyBird", 1, (0, 0, 0))
        window.blit(text, (325, 77))
        playerintro = transform.scale(image.load("PlayerIntro.png"), (80, 95))
        window.blit(playerintro, (350, 300))
    
   

    display.update()

    time.delay(FPS)