from pygame import *

# клас-батько для спрайтів
class GameSprite(sprite.Sprite):
    #конструктор класу
    def __init__(self, player_image, player_x, player_y, player_speed, wight, height):
        super().__init__()
        # кожен спрайт повинен зберігати властивість image - зображення
        self.image = transform.scale(image.load(player_image), (wight, height)) #разом 55,55 - параметри
        self.speed = player_speed
        # кожен спрайт повинен зберігати властивість rect - прямокутник, в який він вписаний
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# клас-спадкоємець для спрайту-гравця (керується стрілками)    
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.y > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.y < win_height - 80:
            self.rect.x += self.speed

#ігрова сцена:
back = (200, 255, 255)  #колір фону (background)
win_width = 600
win_height = 500

window = display.set_mode((win_width, win_height))
window.fill(back)
 
#прапорці, що відповідають за стан гри
game = True
finish = False
clock = time.Clock()
FPS = 60

Playerr = Player('racket.png', 30, 200, 4, 50, 150) 
Platform = GameSprite('racket.png', 520, 200, 4, 50, 150)
Spike = GameSprite('spikes.png', 200, 200, 4, 50, 50)

mixer.init() 
fire = mixer.Sound(".ogg")
fire.set_volume(0.1)

font.init()
font = font.Font(None, 35)
lose = font.render('YOU LOSE', True, (180, 0, 0))
#the variable game is over 
 
finish = False 
 
 
#main game cycle
run = True 

while run: 
 
    #the event of clicking on the close button 
     
    for e in event.get(): 
        if e.type == QUIT: 
            run = False 
            #the event of clicking to space - sprite is shooting
        elif e.type == KEYDOWN:
            if e.key == K_LEFT:

            elif e.key == K_RIGHT:
                #M


    if not finish: 
 
        window.blit((0, 0)) 
         
        #writing text on screen 
 
        lose = font.render("Рахунок:" + str(score), 1, (255, 255, 255)) 
        window.blit(lose, (10, 20)) 
 
        #sprites moves
 
        Playerr.update() 
        Platform.update() 
        Spike.update()
         
        Platform.draw(window) 
        Spike.draw(window)

        if sprite.spritecollide(rocket, monsters, False):
            finish = True
            window.blit(lose, [200, 200])
 
        collides = sprite.groupcollide(Platform, Spike, True, True)
        for c in collides:

            score += 1

        if score >= 100:
            finish = True
            window.blit(txt_win_game, [200, 200])

        if lost == 3:
            finish = True
            window.blit(txt_lose_game, [200, 200])

        display.update() 
    
    else:
        score = 0
        lost = 0
        finish = False
        
        time.delay(3000)
        for i in range(1, 6): 


    time.delay(50)
