import pygame
import random

# Initialize Pygame
pygame.init()

# Define some constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SIZE = 100
ENEMY_SIZE = 100
BULLET_SIZE = 30
BULLET_SPEED = 10
ENEMY_SPEED = 1
PLAYER_Y = SCREEN_HEIGHT // 2

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

GRAVITY = 0.5
JUMP_SPEED = -10

# Set up the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple 2D Game")


background_image = pygame.image.load("images/background.png")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

player_image = pygame.image.load("images/player.png")
player_image = pygame.transform.scale(player_image, (PLAYER_SIZE, PLAYER_SIZE))

enemy_image = pygame.image.load("images/enemy.png")
enemy_image = pygame.transform.scale(enemy_image, (ENEMY_SIZE, ENEMY_SIZE))
enemy_image_flipped = pygame.transform.flip(enemy_image, True, False)

bullet_image = pygame.image.load("images/bullet.png")
bullet_image = pygame.transform.scale(bullet_image, (BULLET_SIZE, BULLET_SIZE))
bullet_image_flipped = pygame.transform.flip(bullet_image, True, False)



class Player:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = PLAYER_Y
        self.direction = 1  # 0 for facing right, 1 for facing left
        self.dy = 0  # Change in y-position (vertical speed)
        self.on_ground = True  # Is the player on the ground?

    def jump(self):
        if self.on_ground:  # Only jump if on the ground
            self.dy = JUMP_SPEED
            self.on_ground = False  # No longer on the ground

    def turn_left(self):
        self.direction = 1
        global player_image
        player_image = pygame.transform.flip(player_image, True, False)

    def turn_right(self):
        self.direction = 0
        global player_image
        player_image = pygame.transform.flip(player_image, True, False)

    def draw(self):
        # pygame.draw.rect(screen, RED, (self.x, self.y, PLAYER_SIZE, PLAYER_SIZE))
        # screen.blit(player_image, (self.x, self.y))
        # screen.blit(player_image, (self.x - PLAYER_SIZE // 2, self.y - PLAYER_SIZE // 2))
        screen.blit(player_image, (self.x - PLAYER_SIZE // 2, self.y - PLAYER_SIZE // 2))

    def shoot(self):
        bullet_x = self.x + PLAYER_SIZE // 2 if self.direction == 0 else self.x - PLAYER_SIZE // 2 - BULLET_SIZE
        bullet_y = self.y
        return Bullet(bullet_x, bullet_y, BULLET_SPEED if self.direction == 0 else -BULLET_SPEED)

    def update(self):
        self.y += self.dy
        self.dy += GRAVITY
        if self.y > PLAYER_Y:  # Check if player is on the ground level
            self.y = PLAYER_Y
            self.dy = 0
            self.on_ground = True

class Enemy:
    def __init__(self):
        self.y = PLAYER_Y
        self.x = 0 if random.choice([True, False]) else SCREEN_WIDTH
        self.direction = 0 if self.x == 0 else 1
        self.dy = 0
        self.on_ground = True

    def move(self):
        if self.direction == 0:
            self.x += ENEMY_SPEED
        else:
            self.x -= ENEMY_SPEED

        # Vertical movement (jump logic)
        if self.on_ground and random.random() < 0.1:  # 10% chance to jump
            self.dy = JUMP_SPEED
            self.on_ground = False

        self.y += self.dy
        self.dy += GRAVITY
        if self.y > PLAYER_Y:  # Check if enemy is on ground level
            self.y = PLAYER_Y
            self.dy = 0
            self.on_ground = True

    def draw(self):
        if self.direction == 0:  # Moving to the right
            screen.blit(enemy_image_flipped, (self.x - ENEMY_SIZE // 2, self.y - ENEMY_SIZE // 2))
        else:  # Moving to the left
            screen.blit(enemy_image, (self.x - ENEMY_SIZE // 2, self.y - ENEMY_SIZE // 2))


class Bullet:
    def __init__(self, x, y, speed=BULLET_SPEED):
        self.x = x
        self.y = y
        self.speed = speed
        self.alive = True

    def move(self):
        self.x += self.speed

    def draw(self):
        if self.speed > 0:  # Moving to the right
            screen.blit(bullet_image_flipped, (self.x - BULLET_SIZE // 2, self.y - BULLET_SIZE // 2))
        else:  # Moving to the left
            screen.blit(bullet_image, (self.x - BULLET_SIZE // 2, self.y - BULLET_SIZE // 2))


player = Player()
enemies = []
bullets = []

running = True
clock = pygame.time.Clock()

while running:
    screen.fill(WHITE)
    screen.blit(background_image, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.turn_left()
            elif event.key == pygame.K_RIGHT:
                player.turn_right()
            elif event.key == pygame.K_z:
                bullets.append(player.shoot())
            elif event.key == pygame.K_UP:
                player.jump()
    
    # Spawn enemies randomly
    if random.random() < 0.02:
        enemies.append(Enemy())

    # Update and draw enemies
    for enemy in enemies[:]:
        enemy.move()
        enemy.draw()
        if enemy.x > SCREEN_WIDTH or enemy.x < 0 - ENEMY_SIZE:
            enemies.remove(enemy)

    # Update and draw bullets
    for bullet in bullets[:]:
        bullet.move()
        bullet.draw()
        if bullet.x > SCREEN_WIDTH:
            bullets.remove(bullet)

    # Check for bullet-enemy collisions
    for bullet in bullets:
        for enemy in enemies:
            bullet_front = bullet.x + BULLET_SIZE if bullet.speed > 0 else bullet.x
            bullet_previous_front = bullet_front - bullet.speed
            
            # Check if the bullet's front has passed through the enemy's x position
            if bullet.speed > 0:  # Moving right
                if bullet_previous_front <= enemy.x and bullet_front >= enemy.x:
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    break
            else:  # Moving left
                if bullet_previous_front >= enemy.x + ENEMY_SIZE and bullet_front <= enemy.x + ENEMY_SIZE:
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    break

    # Check for player-enemy collisions
    for enemy in enemies:
        if player.x < enemy.x + ENEMY_SIZE and player.x + PLAYER_SIZE > enemy.x:
            running = False

    player.update()
    player.draw()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
