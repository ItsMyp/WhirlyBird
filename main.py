from pygame import *
from random import randint 

init()
back = (200, 255, 255)
win_width = 600
win_height = 800
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



class Platform(GameSprite):
    def update(self): 
        self.rect.y += self.speed 
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



jumping =   True
running = True
player = Player('PlayerR1.png', 235, 700, 100, 100, 10)
x_bg = 0
y_bg=0
jump_count=10
jump_height=10


platforms = sprite.Group()
platforms.add(Platform(platform_img,400,win_height - 0,120,20,5))#1
platforms.add(Platform(platform_img,300,win_height - 200,120,20,5))#2
platforms.add(Platform(platform_img,200,win_height - 400,120,20,5))#3
platforms.add(Platform(platform_img,100,win_height - 600,120,20,5))#4



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
        platforms.draw(window)
        platforms.update()
        #spikes.draw(window)
        #spikes.update()
        y_bg=4
        
#        text = font2.render("Рахунок:" + str(score), 1, (0, 0, 0)) 
#        window.blit(text, (10, 20))
        player.update()
        player.animation()
        
        
#        if not sprite.spritecollide(player, platforms, True):
#            player.rect.y -=3

#        hits_lose = sprite.spritecollide(player,spikes,False)
#        if hits_lose:
#            text_lose = font2.render('YOU LOSE', True, [255, 0, 0])
#            window.blit(text_lose, (350, 250))
#            game = False
        
        hits = sprite.spritecollide(player,platforms,False)
        for platform in hits:
            if player.rect.bottom> platform.rect.top:
                    player.rect.bottom =  platform.rect.top
                    player.vel_y =0 

            elif player.rect.top < platform.rect.bottom:
                    player.rect.top =  platform.rect.bottom-10
                    player.vel_y =0 
                    
        
        
        # if hits:
        #     player.rect.bottom = hits[0].rect.top-10
            
        #     score+=1
        #     player.update()
            
            
        if not hits:
            player.rect.bottom +=5 
        if player.rect.y > win_height:
            text_lose = font2.render('YOU LOSE', True, [255, 0, 0])
            window.blit(text_lose, (235, 250))
            game = False

            

        if y_bg == win_width:
            y_bg=0
        elif not jumping:
            if keys[K_SPACE]:
                jumping = False
        else:
            if jump_count >= -jump_height:
                neg = 1
                if jump_count < 0:
                    neg = -1
                player.rect.y -= (jump_count ** 2) * 0.5 * neg
                jump_count -= 1
            else:
                jumping = True
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