from turtle import position
import pygame, debug
import random
from pathfinder import pathfinding_to_eagle, game_map_123

# Инициализация Pygame
pygame.init()

# Размеры окна и клетки
WIDTH, HEIGHT = 30 * 34, 18 * 34
TILE_SIZE = 34

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)    # Brick color
GRAY = (169, 169, 169)   # Steel color
BLUE = (0, 0, 255)       # Water color
GREEN = (0, 255, 0)      # Grass color
YELLOW = (255, 255, 0)   # Player tank color
RED = (255, 0, 0)        # Enemy tank color

enemies = pygame.sprite.Group()
blocks = pygame.sprite.Group()
p_bullets = pygame.sprite.Group()
e_bullets = pygame.sprite.Group()

wave = 0

# Определим карту как двумерный список
game_map = [
    ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
    ['T', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
    ['#', ' ', '#', '#', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', '#', '#', '#', '#', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', '#', ' ', ' ', '#'],
    ['#', ' ', '#', '#', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', '#', ' ', ' ', '#'],
    ['#', ' ', '#', '#', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', '#', ' ', ' ', '#'],
    ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
    ['#', ' ', '#', '#', ' ', '#', '#', '#', '#', '#', '#', '#', ' ', '#', ' ', ' ', ' ', '#', '#', '#', '#', '#', '#', '#', '#', '#', ' ', ' ', ' ', '#'],
    ['#', ' ', '#', '#', ' ', '#', '#', '#', '#', '#', '#', '#', ' ', '#', ' ', ' ', ' ', '#', '#', '#', '#', '#', '#', '#', '#', '#', ' ', ' ', ' ', '#'],
    ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
    ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
    ['#', ' ', '#', '#', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', '#', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', '#', ' ', ' ', ' ', '#'],
    ['#', ' ', '#', '#', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', '#', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', '#', ' ', ' ', ' ', 'T'],
    ['#', ' ', '#', '#', ' ', ' ', ' ', ' ', '#', ' ', ' ', '#', ' ', ' ', ' ', ' ', '#', '#', ' ', ' ', ' ', ' ', ' ', ' ', '#', '#', ' ', ' ', ' ', '#'],
    ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
    ['#', ' ', '#', '#', ' ', '#', '#', '#', '#', '#', ' ', ' ', ' ', ' ', 'P', ' ', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', '#', '#', ' ', ' ', ' ', '#'],
    ['#', ' ', '#', '#', ' ', '#', '#', '#', '#', '#', ' ', ' ', ' ', '#', '#', '#', ' ', '#', ' ', ' ', ' ', ' ', ' ', ' ', '#', '#', ' ', ' ', ' ', '#'],
    ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', 'B', '#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
    ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
]



# Создание словаря для отображения различных символов
tile_images = {
    '#': pygame.Surface((TILE_SIZE, TILE_SIZE)),
    'B': pygame.transform.scale(pygame.image.load('goal.png'), (40, 40)),
    'E': pygame.Surface((TILE_SIZE, TILE_SIZE)),
    'P': pygame.Surface((TILE_SIZE, TILE_SIZE)),
    'T': pygame.Surface((TILE_SIZE, TILE_SIZE)),
    ' ': pygame.Surface((TILE_SIZE, TILE_SIZE))
}
player_images = {
    'P': pygame.transform.scale(pygame.image.load('player_image(1).png'), (34, 34)),
    'P_l': pygame.transform.scale(pygame.image.load('player_image_l.png'), (34, 34)),
    'P_r': pygame.transform.scale(pygame.image.load('player_image_r.png'), (34, 34)),
    'P_d': pygame.transform.scale(pygame.image.load('player_image_d.png'), (34, 34))
}

enemy_images = {
    'E': pygame.transform.scale(pygame.image.load('enemy.png'), (34, 34)),
    'E_l': pygame.transform.scale(pygame.image.load('enemy_left(1).png'), (34, 34)),
    'E_r': pygame.transform.scale(pygame.image.load('enemy_right.png'), (34, 34)),
    'E_d': pygame.transform.scale(pygame.image.load('enemy_down.png'), (34, 34))
}


# Заполнение цветов для каждого типа клетки
tile_images['#'].fill(BROWN)
#tile_images['B'].fill(BLUE)
#tile_images['P'].fill(BLUE)
#tile_images['E'].fill(RED)
tile_images['T'].fill(YELLOW)
tile_images[' '].fill(BLACK)

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tanks")

score = 0

def draw_map(game_map):
    x = -1
    y = -1
    for row in game_map:
        y += 1
        for tile in row:
            x += 1
            screen.blit(tile_images[tile], (x * TILE_SIZE, y * TILE_SIZE))
            if tile == '#':
                blocks.add(Block(x, y))
        x = -1

class Player():
    def __init__(self, x_pos, y_pos, health=20):
        #self.image = pygame.image.load(img)
        #self.current_image = self.image
        #self.rect = self.image.get_rect()
        self.rect = pygame.Rect(x_pos * TILE_SIZE, y_pos * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        self.grid_x = x_pos
        self.grid_y = y_pos
        self.direction = 'up'
        self.health = health

    def move(self, dx, dy, game_map):
        new_x = self.grid_x + dx
        new_y = self.grid_y + dy

        if 0 <= new_x < len(game_map[0]) and 0 <= new_y < len(game_map):
            if game_map[new_y][new_x] == ' ':
                game_map[self.grid_y][self.grid_x] = ' '
                self.grid_x = new_x
                self.grid_y = new_y
                game_map[self.grid_y][self.grid_x] = 'P'
                self.rect.x = self.grid_x * TILE_SIZE
                self.rect.y = self.grid_y * TILE_SIZE

    def shoot(self):
        bullet = Bullet(self.rect.centerx - 5, self.rect.centery - 5, 10, 10, self.direction)
        p_bullets.add(bullet)

    def get_hurt(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.death()
            game_map[self.rect.y // TILE_SIZE][self.rect.x // TILE_SIZE] = ' '

    def death(self):
        game_map[self.rect.y // TILE_SIZE][self.rect.x // TILE_SIZE] = ' '

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, direction):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = 20
        self.direction = direction
        self.damage = 5

    def move(self):
        if self.direction == 'right':
            self.rect.x += self.speed
        elif self.direction == 'left':
            self.rect.x -= self.speed
        elif self.direction == 'up':
            self.rect.y -= self.speed
        elif self.direction == 'down':
            self.rect.y += self.speed

        if self.rect.x < 0 or self.rect.x > WIDTH or self.rect.y < 0 or self.rect.y > HEIGHT:
            self.kill()

    def update_collide(self, other):
        other.get_hurt(self.damage)
        self.kill()

    def reset(self):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)

class Block(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, health=10):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x_pos * TILE_SIZE, y_pos * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        self.health = health

    def get_hurt(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill()
            game_map[self.rect.y // TILE_SIZE][self.rect.x // TILE_SIZE] = ' '

class Goal(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, health=100):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(r"goal.png")
        self.rect = self.image.get_rect()
        self.grid_x = x_pos
        self.grid_y = y_pos
        self.health = health

    def reset(self):
        screen.blit(self.image, (self.grid_x, self.grid_y))

    
    def get_hurt(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill()
            game_map[self.rect.y // TILE_SIZE][self.rect.x // TILE_SIZE] = ' '


class Enemy(pygame.sprite.Sprite):
    paths = [
        [(1, 1), (2, 1), (3, 1), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8), (5, 8), (6, 8), (7, 8), (8, 8), (9, 8), (10, 8), (11, 8), (12, 8), (13, 8), (14, 8), (14, 9), (14, 10), (14, 11), (14, 12), (14, 13)]
    ]
    
    def __init__(self, x_pos, y_pos, health=15):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x_pos * TILE_SIZE, y_pos * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        self.grid_x = x_pos
        self.grid_y = y_pos
        self.direction = 'up'
        self.health = health
        self.path = pathfinding_to_eagle((self.grid_y, self.grid_x), (14, 13), game_map_123)
        self.path_index = 0
        self.move_flag = True

    def move(self):
        if self.path_index < len(self.path):
            next_pos = self.path[self.path_index]
            try:
                game_map[self.grid_y][self.grid_x] = ' '
            except:
                print(game_map[self.grid_y][self.grid_x])
            self.grid_x, self.grid_y = next_pos
            game_map[self.grid_y][self.grid_x] = 'E'
            self.rect.x = self.grid_x * TILE_SIZE
            self.rect.y = self.grid_y * TILE_SIZE
            if self.path_index < len(self.path) - 1:
                prev_step = (self.grid_x, self.grid_y)
                next_step = self.path[self.path_index + 1]
                print(prev_step, next_step)
                print(self.direction)
                if next_step[0] < prev_step[0]:

                    self.direction = 'up'
                elif next_step[0] > prev_step[0]:
                    self.direction = 'right'
                elif next_step[1] < prev_step[1]:
                    self.direction = 'left'
                    print("1")
                elif next_step[1] > prev_step[1]:
                    self.direction = 'down'
                    print("1")
            #print(next_step)
            self.path_index += 1

    def check_target(self, x, y):
        if self.grid_x == x or self.grid_y == y:
            if x < self.grid_x:
                self.direction = 'left'
            if x > self.grid_x:
                self.direction = 'right'
            if y < self.grid_y:
                self.direction = 'up'
            if y > self.grid_y:
                self.direction = 'down'
            self.shoot()
            self.move_flag = False
        else:
            self.move_flag = True

    def shoot(self):
        bullet = Bullet(self.rect.centerx - 5, self.rect.centery - 5, 10, 10, self.direction)
        e_bullets.add(bullet)

    def get_hurt(self, damage):
        global score
        self.health -= damage
        if self.health <= 0:
            self.kill()
            score += 1
            game_map[self.rect.y // TILE_SIZE][self.rect.x // TILE_SIZE] = ' '

def create_enemies(enemy_amount):
    for k in range(enemy_amount):
        positions = [(1, 1)]
        cur_pos = random.choice(positions)
        print(cur_pos)
        if game_map[cur_pos[0]][cur_pos[1]] == ' ':
            if len(enemies) <= 2:
                enemy = Enemy(cur_pos[0], cur_pos[1])
                enemies.add(enemy)
                game_map[cur_pos[0]][cur_pos[1]] = 'E'

def check_new_wave():
    global wave
    if len(enemies) == 0:
        wave += 1
        enemy_amount = random.randint(wave + 2, 5 + wave)
        if enemy_amount >= 13:
            enemy_amount = 13
        create_enemies(enemy_amount)
        
class Button():
    def __init__(self, x, y, width, height, color1, color2, text, text_color, text_x, text_y):
        self.rect = pygame.Rect(x, y, width, height)
        self.color1 = color1
        self.color2 = color2
        self.color = color1
        shrift = pygame.font.SysFont("Comix Sans MS", 80)
        self.text = shrift.render(text, True, text_color)
        self.text_x = text_x
        self.text_y = text_y

    def show(self):
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.text, (self.rect.x + self.text_x, self.rect.y + self.text_y ))

goal = Goal(7, 7)

start_button = Button(380, 206, 300, 100, (77, 41, 42), (41, 21, 22), "S T A R T", (173, 153, 154), 30, 25)
exit_button = Button(380, 406, 300, 100, (77, 41, 42), (41, 21, 22), "  E X I T", (173, 153, 154), 30, 25)
restart_button = Button(380, 206, 300, 100, (77, 41, 42), (41, 21, 22), "RESTART", (173, 153, 154), 25, 25)

game_name = pygame.font.SysFont("Verdana", 80, 1, 1).render("Tanks", True, (209, 71, 78))
lose = pygame.font.SysFont("Verdana", 80, 1, 1).render("You Lose", True, (176, 12, 67))
victory = pygame.font.SysFont("Verdana", 80, 1, 1).render("You Won", True, (75, 189, 96))
score_txt = pygame.font.SysFont("Verdana", 30, 1, 1).render("Score: " + str(score), True, (97, 132, 171))

goal_health = pygame.font.SysFont("Verdana", 40, 1, 1).render("Health: " + str(goal.health), True, (97, 132, 171))

player = Player(14, 14)



FPS = 60
clock = pygame.time.Clock()
prog = True

enemy_move_timer = 0

game = "lose"

while prog:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            prog = False
        
            #if event.type == pygame.KEYDOWN:
                #if event.key == pygame.K_w:
                    #player.move(0, -1, game_map)
                    #player.direction = 'up'
                
                #elif event.key == pygame.K_a:
                    #player.move(-1, 0, game_map)
                    #player.direction = 'left'
                
                #elif event.key == pygame.K_s:
                    #player.move(0, 1, game_map)
                    #player.direction = 'down'
                
                #elif event.key == pygame.K_d:
                    #player.move(1, 0, game_map)
                    #player.direction = 'right'
                
            #if event.key == pygame.K_SPACE:
                #player.shoot()
            #if player.direction == "up":
                #screen.blit(player_images['P'] ,(player.rect.x, player.rect.y))
            #if player.direction == "down":
                #screen.blit(player_images['P_d'] ,(player.rect.x, player.rect.y))
            #if player.direction == "left":
                #screen.blit(player_images['P_l'] ,(player.rect.x, player.rect.y))
            #if player.direction == "right":
                #screen.blit(player_images['P_r'] ,(player.rect.x, player.rect.y))
        
            
            
            '''
            for enemy in enemies:
                if enemy.direction == "up":
                    screen.blit(enemy_images['E'] ,(enemy.rect.x, enemy.rect.y))
                if enemy.direction == "down":
                    screen.blit(enemy_images['E_d'] ,(enemy.rect.x, enemy.rect.y))
                if enemy.direction == "left":
                    screen.blit(enemy_images['E_l'] ,(enemy.rect.x, enemy.rect.y))
                if enemy.direction == "right":
                    screen.blit(enemy_images['E_r'] ,(enemy.rect.x, enemy.rect.y))





            for bullet in p_bullets:
                bullet.reset()
                bullet.move()
                for block in blocks:
                    if bullet.rect.colliderect(block.rect):
                        bullet.update_collide(block)
                for enemy in enemies:
                    if bullet.rect.colliderect(enemy.rect):
                        bullet.update_collide(enemy)

            for bullet in e_bullets:
                bullet.reset()
                bullet.move()
                for block in blocks:
                    if bullet.rect.colliderect(block.rect):
                        bullet.update_collide(block)
                if bullet.rect.colliderect(player.rect):
                    bullet.update_collide(player)

                elif bullet.rect.colliderect(goal.rect):
                    bullet.update_collide(goal)

            current_time = pygame.time.get_ticks()
            if current_time - enemy_move_timer > 500:
                for enemy in enemies:
                    if enemy.move_flag:
                        enemy.move()
                    enemy.check_target(player.grid_x, player.grid_y)
                    enemy.check_target(14, 13)
                enemy_move_timer = current_time
                '''
        elif game == "menu":
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if start_button.rect.collidepoint(x, y):
                    game = "play"

                elif exit_button.rect.collidepoint(x, y):
                    prog = False

            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                if start_button.rect.collidepoint(x, y):
                    start_button.color = start_button.color2

                elif exit_button.rect.collidepoint(x, y):
                    exit_button.color = exit_button.color2

                else:
                    start_button.color = start_button.color1
                    exit_button.color = exit_button.color1


        elif game == "win":
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if restart_button.rect.collidepoint(x, y):
                    game = "play"
                    score = 0

                elif exit_button.rect.collidepoint(x, y):
                    prog = False

            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                if restart_button.rect.collidepoint(x, y):
                    restart_button.color = restart_button.color2

                elif exit_button.rect.collidepoint(x, y):
                    exit_button.color = exit_button.color2

                else:
                    restart_button.color = restart_button.color1
                    exit_button.color = exit_button.color1

        elif game == "lose":
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if restart_button.rect.collidepoint(x, y):
                    game = "play"
                    score = 0

                elif exit_button.rect.collidepoint(x, y):
                    prog = False

            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                if restart_button.rect.collidepoint(x, y):
                    restart_button.color = restart_button.color2

                elif exit_button.rect.collidepoint(x, y):
                    exit_button.color = exit_button.color2

                else:
                    restart_button.color = restart_button.color1
                    exit_button.color = exit_button.color1







    if game == "play":
        draw_map(game_map)
        check_new_wave()
        screen.blit(goal_health, (680, 570))
        screen.blit(score_txt, (40, 0))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player.move(0, -1, game_map)
                player.direction = 'up'
                
            elif event.key == pygame.K_a:
                player.move(-1, 0, game_map)
                player.direction = 'left'
                
            elif event.key == pygame.K_s:
                player.move(0, 1, game_map)
                player.direction = 'down'
                
            elif event.key == pygame.K_d:
                player.move(1, 0, game_map)
                player.direction = 'right'
                
            if event.key == pygame.K_SPACE:
                player.shoot()
            if player.direction == "up":
                screen.blit(player_images['P'] ,(player.rect.x, player.rect.y))
            if player.direction == "down":
                screen.blit(player_images['P_d'] ,(player.rect.x, player.rect.y))
            if player.direction == "left":
                screen.blit(player_images['P_l'] ,(player.rect.x, player.rect.y))
            if player.direction == "right":
                screen.blit(player_images['P_r'] ,(player.rect.x, player.rect.y))

        if player.direction == "up":
            screen.blit(player_images['P'] ,(player.rect.x, player.rect.y))
        if player.direction == "down":
            screen.blit(player_images['P_d'] ,(player.rect.x, player.rect.y))
        if player.direction == "left":
            screen.blit(player_images['P_l'] ,(player.rect.x, player.rect.y))
        if player.direction == "right":
            screen.blit(player_images['P_r'] ,(player.rect.x, player.rect.y))


        for enemy in enemies:
            if enemy.direction == "up":
                screen.blit(enemy_images['E'] ,(enemy.rect.x, enemy.rect.y))
            if enemy.direction == "down":
                screen.blit(enemy_images['E_d'] ,(enemy.rect.x, enemy.rect.y))
            if enemy.direction == "left":
                screen.blit(enemy_images['E_l'] ,(enemy.rect.x, enemy.rect.y))
            if enemy.direction == "right":
                screen.blit(enemy_images['E_r'] ,(enemy.rect.x, enemy.rect.y))





        for bullet in p_bullets:
            bullet.reset()
            bullet.move()
            for block in blocks:
                if bullet.rect.colliderect(block.rect):
                    bullet.update_collide(block)
            for enemy in enemies:
                if bullet.rect.colliderect(enemy.rect):
                    bullet.update_collide(enemy)

        for bullet in e_bullets:
            bullet.reset()
            bullet.move()
            for block in blocks:
                if bullet.rect.colliderect(block.rect):
                    bullet.update_collide(block)
            if bullet.rect.colliderect(player.rect):
                bullet.update_collide(player)

            elif bullet.rect.colliderect(goal.rect):
                bullet.update_collide(goal)

        current_time = pygame.time.get_ticks()
        if current_time - enemy_move_timer > 500:
            for enemy in enemies:
                if enemy.move_flag:
                    enemy.move()
                enemy.check_target(player.grid_x, player.grid_y)
                enemy.check_target(14, 13)
            enemy_move_timer = current_time

        if score >= 10:
            game = "win"

        elif goal.health <= 0:
            game = "lose"





    elif game == "menu":
        screen.fill(BLACK)
        start_button.show()
        exit_button.show()
        screen.blit(game_name, (380, 30))



    elif game == "win":
        screen.fill(BLACK)
        restart_button.show()
        exit_button.show()
        screen.blit(victory, (340, 30))

    elif game == "lose":
        screen.fill(BLACK)
        restart_button.show()
        exit_button.show()
        screen.blit(lose, (340, 30))

    #debug.debug()
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
