#Создай собственный Шутер!

from pygame import *
from random import randint
win_width = 700
win_height = 500

lost = 0

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, size_x, size_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_press = key.get_pressed()
        if keys_press[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_press[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.x + 7, self.rect.top - 40, 10, 55, 60)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed 
        global lost
        if self.rect.y >= win_height:
            self.rect.y = 0
            self.rect.x = randint(50, win_width - 80)
            lost = lost + 1


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()




window = display.set_mode((win_width, win_height))
display.set_caption('Шутер')

background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
music_f = mixer.Sound('fire.ogg')

font.init()
font1 = font.SysFont("Arial", 36)


player = Player('rocket1.png', 300, 400, 5, 80, 100)

enemies = sprite.Group()
for i in range(5):
    enemy = Enemy('ufo.png', randint(50, win_width - 80), -60, randint(2, 7), 80, 60)
    enemies.add(enemy)

bullets = sprite.Group()

asteroids = sprite.Group()
for i in range(2):
    asteroid = Enemy('asteroid.png', randint(50, win_width - 80), -60, randint(2, 4), 100, 80)
    asteroids.add(asteroid)



FPS = 60
game = True
finish = False

clock = time.Clock()

highscore = 0

print_win = font1.render('Ты победил! ', 1, (0, 255, 47))
print_lose = font1.render('Ты проиграл ', 1, (255, 0, 0))

live = 99999999999999999999999999999999999999999999999999999999999999

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()
                music_f.play()
    if finish != True:

        window.blit(background, (0, 0))

        text_lose = font1.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 20))

        text_win = font1.render("Счёт: " + str(highscore), 1, (255, 255, 255))

        window.blit(text_win, (10, 50))

        live_ = font1.render('Жизни: ' + str(live), 1, (255, 255, 255))

        window.blit(live_, (10, 80))





        player.update()

        player.reset()


        enemies.draw(window)

        enemies.update()

        bullets.draw(window)

        bullets.update()

        asteroids.draw(window)

        asteroids.update()

        sprites_list = sprite.groupcollide(enemies, bullets, True, True)
        for s in sprites_list:
            highscore += 1
            enemy = Enemy('nlo.png', randint(50, win_width - 80), -60, randint(2, 7), 80, 60)
            enemies.add(enemy)
        if sprite.spritecollide(player, enemies, False) or sprite.spritecollide(player, asteroids, False):
            live -= 1
            sprite.spritecollide(player, enemies, True)
            sprite.spritecollide(player, asteroids, True)
        if live == 0:
            finish = True
            window.blit(print_lose, (200, 200))
        if highscore >= 15:
            finish = True
            window.blit(print_win, (200, 200)) 
        

















    display.update()
    clock.tick(FPS)

