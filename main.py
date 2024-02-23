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

player = Player('racket.png', 30, 200, 4, 50, 150) 
Platform = GameSprite('racket.png', 520, 200, 4, 50, 150)
Spike = GameSprite('tenis_ball.png', 200, 200, 4, 50, 50)

font.init()
font = font.Font(None, 35)
lose1 = font.render('YOU LOSE', True, (180, 0, 0))