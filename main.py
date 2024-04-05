from pygame import *
from random import randint 
import sys
init()
back = (200, 255, 255)
win_width = 600
win_height = 600
window = display.set_mode((win_width, win_height))
player_l = [image.load('PlayerL1.png'), image.load('PlayerL2.png'), image.load('PlayerL3.png')]
player_r = [image.load('PlayerR1.png'), image.load('PlayerR2.png'), image.load('PlayerR3.png')]

clock = time.Clock()
start_time = time.get_ticks()

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
    def check_collisions_down(self, blocks):
        is_on_ground = False
        for block in blocks:
            if self.rect.colliderect(block.rect):
                if self.rect.y <= block.rect.y-40:
                    self.rect.bottom = block.rect.y + 7.5
                    is_on_ground = True
        if not is_on_ground:
             self.rect.y += 12



class Platform(GameSprite):
    def update(self): 
        self.rect.y += 7 
        if self.rect.y > win_height: 
            self.rect.x = randint(120, win_width - 120) 
            self.rect.y = 0 
        
            

        

FPS = 24
bg = transform.scale(image.load("bg.png"), (win_width, win_height))
display.set_caption("WhirlyBird")

clock = time.Clock()

game = False
menu = True

platform_img = 'platform.png' 
spikes_img = 'spikes.png'

score = 0

font.init() 
font4 = font.Font(None, 36)
font3 = font.Font(None, 36)
font2 = font.Font(None, 36) 
font1 = font.Font(None,100)



running = True
player = Player('PlayerR1.png', 235, 300, 100, 100, 10)
x_bg = 0
y_bg=0
jump_count = 7.5
jump_height = 7.5
jumping = False
text_score = font2.render(f'Рахунок:{score}',True,(255,255,22))

platforms = sprite.Group()
platforms.add(Platform(platform_img,100,win_height - 0,120,20,5))#1
platforms.add(Platform(platform_img,200,win_height - 200,120,20,5))#2
platforms.add(Platform(platform_img,300,win_height - 400,120,20,5))#3
platforms.add(Platform(platform_img,500,500,120,20,5))#1



while running:
    keys = key.get_pressed()
    current_time = time.get_ticks()
    game_time = (current_time - start_time)/1000

    for e in event.get():
        if e.type == QUIT:
            running = False
        if  e.type==KEYDOWN :
            if e.key == K_UP and menu == True:
                game = True
                menu = False

        
    

    if game:
        window.fill(back)
        window.blit(bg, (y_bg, y_bg))
        window.blit(bg, (y_bg+win_width, y_bg))
        platforms.draw(window)
        platforms.update()
        text_score = font2.render(f'Таймер:{game_time}',True,(0,255,0))
        window.blit(text_score, (20, 20))


        y_bg=4
 
        player.update()
        player.animation()
        player.check_collisions_down(platforms)
    
        
        

        if player.rect.y > win_height:
            text_lose = font2.render('YOU LOSE', True, [255, 0, 0])
            window.blit(text_lose, (235, 250))
            game = False

            

        if y_bg == win_width:
            y_bg=0
        if not jumping:
            if keys[K_UP]:
                jumping = True 


        else:
            if jump_count >= -jump_height:
                neg = 1
                if jump_count < 0:
                    neg = -1

                player.rect.y -= (jump_count ** 2)  * neg
                jump_count -= 0.8
            else:
                jumping = False
                jump_count = jump_height


    if menu:
        window.fill(back)
        window.blit(bg, (y_bg, y_bg))
        window.blit(bg, (y_bg+win_width, y_bg))
        text = font2.render("WhirlyBird", 1, (0, 0, 0))
        window.blit(text, (235, 200))
        playerintro = transform.scale(image.load("PlayerIntro.png"), (80, 95))
        window.blit(playerintro, (260, 350))

    display.update()

    time.delay(FPS)