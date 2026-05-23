from pygame import *
mixer.init()
font.init()
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('Maze')
background = transform.scale(image.load('background.jpg'), (win_width, win_height))
mixer.music.load('jungles.ogg')
mixer.music.play()
clock = time.Clock()
FPS = 60
game = True
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):#конструктор класса
        super().__init__()#унаследование свойств класса Sprite
        self.image = transform.scale(image.load(player_image), (65, 65))#картинка 
        self.speed = player_speed#скорость 
        self.rect = self.image.get_rect()#хитбоксы
        self.rect.x = player_x#координаты
        self.rect.y = player_y#координаты
    def reset(self):#функция для отображения
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed
class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)
        self.direction = 'left'
    def update(self):
        if self.rect.x <= 470:
            self.direction = 'right'
        if self. rect.x > win_width - 85:
            self.direction = 'left'
        if self.direction == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.width = wall_width
        self.height = wall_height
        self.image = Surface((self.width, self.height))
        self.image.fill((color_1, color_2, color_3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
font = font.SysFont('Arial', 70)
win = font.render('YOU WIN!', True, (255, 215, 0))
lose = font.render('YOU LOSE!', True, (252, 3, 3))
player = Player('hero.png', 50, 400, 15)
enemy = Enemy('cyborg.png', 600, 300, 1)
treasure = GameSprite('treasure.png', 600, 400, 0)
wall = Wall(100, 50, 40, 200, 200, 20, 300)
wall1 = Wall(100, 50, 150, 250, 200, 20, 300)
wall2 = Wall(100, 50, 100, 300, 200, 20, 300)
finish = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if finish != True:
        window.blit(background, (0, 0))
        player.reset()
        player.update()
        enemy.reset()
        enemy.update()
        treasure.reset()
        wall.draw_wall()
        wall1.draw_wall()
        wall2.draw_wall()
        if sprite.collide_rect(player, treasure):
            finish = True
            window.blit(win, (200, 200))
        if sprite.collide_rect(player, enemy) or sprite.collide_rect(player, wall) or sprite.collide_rect(player, wall1) or sprite.collide_rect(player, wall2):
            finish = True
            window.blit(lose, (200, 200))
        display.update()
        clock.tick(FPS)

