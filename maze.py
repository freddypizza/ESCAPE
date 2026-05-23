from pygame import *
import random
mixer.init()
font.init()

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('Maze - No Walls, Only Borders')
background = transform.scale(image.load('background.jpg'), (win_width, win_height))

mixer.music.load('jungles.ogg')
mixer.music.play()
clock = time.Clock()
FPS = 60
game = True

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (50, 50))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 55:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 55:
            self.rect.y += self.speed

class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)
    
    def update(self, target):
        # Преследование игрока
        # Движение по X
        if self.rect.x < target.rect.x:
            self.rect.x += self.speed
        elif self.rect.x > target.rect.x:
            self.rect.x -= self.speed
        
        # Движение по Y
        if self.rect.y < target.rect.y:
            self.rect.y += self.speed
        elif self.rect.y > target.rect.y:
            self.rect.y -= self.speed
        
        # Границы для монстров (чтобы не выходили за пределы)
        self.rect.x = max(5, min(win_width - 55, self.rect.x))
        self.rect.y = max(5, min(win_height - 55, self.rect.y))

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

# Создание только границ (внешних стен)
walls = []

# Верхняя граница
for x in range(0, win_width, 50):
    walls.append(Wall(100, 50, 40, x, 0, 48, 20))

# Нижняя граница
for x in range(0, win_width, 50):
    walls.append(Wall(100, 50, 40, x, win_height - 20, 48, 20))

# Левая граница
for y in range(0, win_height, 50):
    walls.append(Wall(100, 50, 40, 0, y, 20, 48))

# Правая граница
for y in range(0, win_height, 50):
    walls.append(Wall(100, 50, 40, win_width - 20, y, 20, 48))

# Создание игрока, монстров и сокровища
player = Player('hero.png', 50, 50, 5)

# Создаем трех монстров в разных углах
enemy1 = Enemy('cyborg.png', 600, 50, 2)    # Правый верхний угол
enemy2 = Enemy('cyborg.png', 50, 430, 2)    # Левый нижний угол
enemy3 = Enemy('cyborg.png', 600, 430, 2)   # Правый нижний угол

# Собираем всех монстров в список
enemies = [enemy1, enemy2, enemy3]

treasure = GameSprite('treasure.png', 620, 440, 0)

# Шрифты
main_font = font.SysFont('Arial', 70)
small_font = font.SysFont('Arial', 30)
win_text = main_font.render('YOU WIN!', True, (255, 215, 0))
lose_text = main_font.render('YOU LOSE!', True, (252, 3, 3))

finish = False
victory = False

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_r:  # Перезапуск игры
                player.rect.x = 50
                player.rect.y = 50
                enemy1.rect.x = 600
                enemy1.rect.y = 50
                enemy2.rect.x = 50
                enemy2.rect.y = 430
                enemy3.rect.x = 600
                enemy3.rect.y = 430
                treasure.rect.x = 620
                treasure.rect.y = 440
                finish = False
                victory = False
    
    if not finish:
        window.blit(background, (0, 0))
        
        # Обновление игрока
        player.update()
        
        # Обновление всех монстров (они преследуют игрока)
        for enemy in enemies:
            enemy.update(player)
        
        # Отрисовка игрока
        player.reset()
        
        # Отрисовка всех монстров
        for enemy in enemies:
            enemy.reset()
        
        # Отрисовка сокровища
        treasure.reset()
        
        # Отрисовка границ
        for wall in walls:
            wall.draw_wall()
        
        # Проверка победы
        if sprite.collide_rect(player, treasure):
            finish = True
            victory = True
        
        # Проверка поражения (столкновение с любым монстром)
        for enemy in enemies:
            if sprite.collide_rect(player, enemy):
                finish = True
                victory = False
                break
        
        # Отображение информации
        info_text = small_font.render(f'FPS: {int(clock.get_fps())}', True, (255, 255, 255))
        window.blit(info_text, (10, 10))
        
        restart_hint = small_font.render('Press R to restart', True, (255, 255, 255))
        window.blit(restart_hint, (10, win_height - 30))
        
        # Отображение количества монстров
        monsters_text = small_font.render(f'Monsters: {len(enemies)}', True, (255, 0, 0))
        window.blit(monsters_text, (win_width - 150, 10))
        
        # Подсказка по управлению
        controls_text = small_font.render('Use ARROWS to move', True, (255, 255, 255))
        window.blit(controls_text, (win_width//2 - 100, 10))
        
    else:
        # Экран победы/поражения
        if victory:
            window.blit(win_text, (win_width//2 - win_text.get_width()//2, win_height//2 - 100))
        else:
            window.blit(lose_text, (win_width//2 - lose_text.get_width()//2, win_height//2 - 100))
        
        restart_text = small_font.render('Press R to restart', True, (255, 255, 255))
        window.blit(restart_text, (win_width//2 - restart_text.get_width()//2, win_height//2 + 50))
    
    display.update()
    clock.tick(FPS)

time.wait(1000)

