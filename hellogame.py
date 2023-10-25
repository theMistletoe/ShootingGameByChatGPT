import pygame
import random

# Initialize Pygame
pygame.init()

# Define some constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SIZE = 100
ENEMY_SIZE = 100
BULLET_SIZE = 10
BULLET_SPEED = 10
ENEMY_SPEED = 5
PLAYER_Y = SCREEN_HEIGHT // 2

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set up the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple 2D Game")


background_image = pygame.image.load("background.png")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

player_image = pygame.image.load("player.png")
player_image = pygame.transform.scale(player_image, (PLAYER_SIZE, PLAYER_SIZE))


class Player:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = PLAYER_Y
        self.direction = 1  # 0 for facing right, 1 for facing left
    
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
        screen.blit(player_image, (self.x - PLAYER_SIZE // 2, self.y - PLAYER_SIZE // 2))

    def shoot(self):
        if self.direction == 0:  # Facing right
            return Bullet(self.x + PLAYER_SIZE, self.y)
        else:  # Facing left
            return Bullet(self.x - BULLET_SIZE, self.y, -BULLET_SPEED)

class Enemy:
    def __init__(self):
        self.y = PLAYER_Y
        self.x = 0 if random.choice([True, False]) else SCREEN_WIDTH
        self.direction = 0 if self.x == 0 else 1

    def move(self):
        if self.direction == 0:
            self.x += ENEMY_SPEED
        else:
            self.x -= ENEMY_SPEED

    def draw(self):
        pygame.draw.rect(screen, GREEN, (self.x, self.y, ENEMY_SIZE, ENEMY_SIZE))

class Bullet:
    def __init__(self, x, y, speed=BULLET_SPEED):
        self.x = x
        self.y = y
        self.speed = speed
        self.alive = True

    def move(self):
        self.x += self.speed

    def draw(self):
        pygame.draw.rect(screen, BLUE, (self.x, self.y, BULLET_SIZE, BULLET_SIZE))




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

    player.draw()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
