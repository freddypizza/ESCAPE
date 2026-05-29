from pygame import *
import random

#  НАСТРОЙКА 

mixer.init()
font.init()

win_width = 680
win_height = 680

window = display.set_mode((win_width, win_height))
display.set_caption('Maze')

background = Surface((win_width, win_height))
background.fill((30, 30, 30))

clock = time.Clock()
FPS = 60

game = True

# КЛАССЫ 

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()

        self.image = transform.scale(
            image.load(player_image),
            (28, 28)
        )

        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):

    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)

        self.lives = 3
        self.has_sword = False

        self.invincible = False
        self.invincible_timer = 0

    def update(self, walls):

        keys = key.get_pressed()

        dx = 0
        dy = 0

        if keys[K_LEFT]:
            dx = -self.speed

        if keys[K_RIGHT]:
            dx = self.speed

        if keys[K_UP]:
            dy = -self.speed

        if keys[K_DOWN]:
            dy = self.speed

        # X 

        self.rect.x += dx

        for wall in walls:
            if sprite.collide_rect(self, wall):

                if dx > 0:
                    self.rect.right = wall.rect.left

                if dx < 0:
                    self.rect.left = wall.rect.right

        #  Y 

        self.rect.y += dy

        for wall in walls:
            if sprite.collide_rect(self, wall):

                if dy > 0:
                    self.rect.bottom = wall.rect.top

                if dy < 0:
                    self.rect.top = wall.rect.bottom

        #  НЕУЯЗВИМОСТЬ 

        if self.invincible:

            self.invincible_timer -= 1

            if self.invincible_timer <= 0:
                self.invincible = False

    def take_damage(self):

        if not self.invincible:

            self.lives -= 1

            self.invincible = True
            self.invincible_timer = 60

            return True

        return False


class Enemy(GameSprite):

    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)

        self.alive = True

    def update(self, target, walls):

        if not self.alive:
            return

        dx = 0
        dy = 0

        if self.rect.x < target.rect.x:
            dx = self.speed

        if self.rect.x > target.rect.x:
            dx = -self.speed

        if self.rect.y < target.rect.y:
            dy = self.speed

        if self.rect.y > target.rect.y:
            dy = -self.speed

        # X

        self.rect.x += dx

        for wall in walls:

            if sprite.collide_rect(self, wall):

                if dx > 0:
                    self.rect.right = wall.rect.left

                if dx < 0:
                    self.rect.left = wall.rect.right

        #  Y

        self.rect.y += dy

        for wall in walls:

            if sprite.collide_rect(self, wall):

                if dy > 0:
                    self.rect.bottom = wall.rect.top

                if dy < 0:
                    self.rect.top = wall.rect.bottom

    def reset(self):

        if self.alive:
            window.blit(self.image, (self.rect.x, self.rect.y))


class Wall(sprite.Sprite):

    def __init__(self,
                 color_1,
                 color_2,
                 color_3,
                 wall_x,
                 wall_y,
                 wall_width,
                 wall_height):

        super().__init__()

        self.image = Surface((wall_width, wall_height))
        self.image.fill((color_1, color_2, color_3))

        self.rect = self.image.get_rect()

        self.rect.x = wall_x
        self.rect.y = wall_y

    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Sword(GameSprite):

    def __init__(self, x, y):
        super().__init__('sword.png', x, y, 0)

        self.collected = False

    def reset(self):

        if not self.collected:
            window.blit(self.image, (self.rect.x, self.rect.y))


class Trap(GameSprite):

    def __init__(self, x, y):
        super().__init__('dynamite.png', x, y, 0)

        self.triggered = False

    def reset(self):

        if not self.triggered:
            window.blit(self.image, (self.rect.x, self.rect.y))


#  ЛАБИРИНТ 

walls = []

TILE = 40

maze_map = [
    "#################",
    "#   #     #     #",
    "# # ### # ### # #",
    "# #     #     # #",
    "# ##### ##### # #",
    "#     #   #   # #",
    "##### ### # ### #",
    "#   #     #     #",
    "# # ####### ### #",
    "# #   #   # #   #",
    "# ### # # # # ###",
    "#     # #   #   #",
    "### ### ##### # #",
    "#   #     #   # #",
    "# ##### # # ### #",
    "#       #       #",
    "#################"
]

for row_index, row in enumerate(maze_map):

    for col_index, cell in enumerate(row):

        if cell == "#":

            x = col_index * TILE
            y = row_index * TILE

            walls.append(
                Wall(
                    100,
                    50,
                    40,
                    x,
                    y,
                    TILE,
                    TILE
                )
            )

# ИГРОК 

player = Player('hero.png', 50, 50, 3)

#  МОНСТРЫ 

enemy1 = Enemy('cyborg.png', 550, 70, 1)
enemy2 = Enemy('cyborg.png', 550, 550, 1)
enemy3 = Enemy('cyborg.png', 70, 550, 1)

enemies = [enemy1, enemy2, enemy3]

#  СОКРОВИЩЕ 

treasure = GameSprite('treasure.png', 600, 600, 0)

#  СЛУЧАЙНЫЕ ПОЗИЦИИ 

def get_random_position(
        walls_list,
        used_positions,
        object_size=28,
        min_distance=80,
        attempts=200):

    for _ in range(attempts):

        x = random.randint(40, win_width - 80)
        y = random.randint(40, win_height - 80)

        temp_rect = Rect(x, y, object_size, object_size)

        collision = False

        # Стены

        for wall in walls_list:

            if temp_rect.colliderect(wall.rect):
                collision = True
                break

        # Другие объекты

        if not collision:

            for pos in used_positions:

                dx = x - pos[0]
                dy = y - pos[1]

                distance = (dx * dx + dy * dy) ** 0.5

                if distance < min_distance:
                    collision = True
                    break

        if not collision:
            return x, y

    return 100, 100

# МЕЧ 

used_positions = []

sword_x, sword_y = get_random_position(
    walls,
    used_positions
)

used_positions.append((sword_x, sword_y))

sword = Sword(sword_x, sword_y)

# ЛОВУШКИ 

traps = []

for _ in range(3):

    trap_x, trap_y = get_random_position(
        walls,
        used_positions
    )

    used_positions.append((trap_x, trap_y))

    traps.append(Trap(trap_x, trap_y))

#  ШРИФТЫ 

main_font = font.SysFont('Arial', 70)
small_font = font.SysFont('Arial', 25)

win_text = main_font.render('YOU WIN!', True, (255, 215, 0))
lose_text = main_font.render('YOU LOSE!', True, (255, 0, 0))

finish = False
victory = False

#  РЕСТАРТ 

def restart_game():

    global finish
    global victory
    global traps

    player.rect.x = 50
    player.rect.y = 50

    player.lives = 3
    player.has_sword = False

    enemy1.rect.x = 550
    enemy1.rect.y = 70
    enemy1.alive = True

    enemy2.rect.x = 550
    enemy2.rect.y = 550
    enemy2.alive = True

    enemy3.rect.x = 70
    enemy3.rect.y = 550
    enemy3.alive = True

    used_positions = []

    #  МЕЧ 

    sword_x, sword_y = get_random_position_without_walls(
        walls,
        used_positions
    )

    used_positions.append((sword_x, sword_y))

    sword.rect.x = sword_x
    sword.rect.y = sword_y

    sword.collected = False

    # ЛОВУШКИ 

    traps = []

    for _ in range(3):

        trap_x, trap_y = get_random_position_without_walls(
            walls,
            used_positions
        )

        used_positions.append((trap_x, trap_y))

        traps.append(Trap(trap_x, trap_y))

    finish = False
    victory = False

#  ИГРОВОЙ ЦИКЛ 

while game:

    for e in event.get():

        if e.type == QUIT:
            game = False

        if e.type == KEYDOWN:

            if e.key == K_r:
                restart_game()

    if not finish:

        window.blit(background, (0, 0))

        #  ОБНОВЛЕНИЕ 

        player.update(walls)

        for enemy in enemies:
            enemy.update(player, walls)

        #  МЕЧ 

        if not sword.collected:

            if sprite.collide_rect(player, sword):

                sword.collected = True
                player.has_sword = True

        #  ЛОВУШКИ 

        for trap in traps:

            if not trap.triggered:

                if sprite.collide_rect(player, trap):

                    trap.triggered = True
                    player.take_damage()

        #  МОНСТРЫ 

        for enemy in enemies:

            if enemy.alive:

                if sprite.collide_rect(player, enemy):

                    if player.has_sword:
                        enemy.alive = False

                    else:
                        player.take_damage()

        #  ПОБЕДА 

        if sprite.collide_rect(player, treasure):

            finish = True
            victory = True

        # ПОРАЖЕНИЕ 
        if player.lives <= 0:

            finish = True
            victory = False

        # ОТРИСОВКА 

        for wall in walls:
            wall.draw_wall()

        treasure.reset()

        sword.reset()

        for trap in traps:
            trap.reset()

        for enemy in enemies:
            enemy.reset()

        player.reset()

        # ТЕКСТ 

        lives_text = small_font.render(
            f'Lives: {player.lives}',
            True,
            (255, 255, 255)
        )

        window.blit(lives_text, (10, 10))

        sword_text = small_font.render(
            f'Sword: {"YES" if player.has_sword else "NO"}',
            True,
            (255, 215, 0)
        )

        window.blit(sword_text, (10, 40))

        restart_text = small_font.render(
            'Press R to restart',
            True,
            (200, 200, 200)
        )

        window.blit(restart_text, (10, 70))

    else:

        window.fill((0, 0, 0))

        if victory:

            window.blit(
                win_text,
                (
                    win_width // 2 - win_text.get_width() // 2,
                    250
                )
            )

        else:

            window.blit(
                lose_text,
                (
                    win_width // 2 - lose_text.get_width() // 2,
                    250
                )
            )

        restart_text = small_font.render(
            'Press R to restart',
            True,
            (255, 255, 255)
        )

        window.blit(restart_text, (220, 370))

    display.update()
    clock.tick(FPS)

quit()

