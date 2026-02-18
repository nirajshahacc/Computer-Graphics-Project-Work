import pygame
import sys
import random
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter - CG Project")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 25)

# ---------------- Bresenham Line ----------------
def line(x1, y1, x2, y2):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    lx = 1 if x2 > x1 else -1
    ly = 1 if y2 > y1 else -1
    x, y = x1, y1

    if dx > dy:
        p = 2 * dy - dx
        for _ in range(dx + 1):
            screen.set_at((int(x), int(y)), WHITE)
            if p < 0:
                x += lx
                p += 2 * dy
            else:
                x += lx
                y += ly
                p += 2 * dy - 2 * dx
    else:
        p = 2 * dx - dy
        for _ in range(dy + 1):
            screen.set_at((int(x), int(y)), WHITE)
            if p < 0:
                y += ly
                p += 2 * dx
            else:
                x += lx
                y += ly
                p += 2 * dx - 2 * dy

# ---------------- Draw Spaceship ----------------
def draw_ship(x, y):
    points = [
        (x, y - 20),
        (x - 15, y + 20),
        (x + 15, y + 20)
    ]

    line(*points[0], *points[1])
    line(*points[1], *points[2])
    line(*points[2], *points[0])

# ---------------- Draw Circle (Enemy) ----------------
def draw_circle(xc, yc, r):
    x = 0
    y = r
    d = 1 - r

    while x <= y:
        for dx, dy in [(x,y),(x,-y),(-x,y),(-x,-y),(y,x),(y,-x),(-y,x),(-y,-x)]:
            screen.set_at((xc + dx, yc + dy), RED)
        x += 1
        if d < 0:
            d += 2 * x + 1
        else:
            y -= 1
            d += 2 * (x - y) + 1

# ---------------- Game Variables ----------------
player_x = WIDTH // 2
player_y = HEIGHT - 60
bullets = []
enemies = []
score = 0
game_over = False

# Spawn enemies
def spawn_enemy():
    x = random.randint(50, WIDTH - 50)
    y = random.randint(-100, -40)
    enemies.append([x, y])

spawn_timer = 0

# ---------------- Main Loop ----------------
while True:
    clock.tick(60)
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                bullets.append([player_x, player_y - 20])

    keys = pygame.key.get_pressed()

    if not game_over:
        if keys[pygame.K_LEFT] and player_x > 20:
            player_x -= 5
        if keys[pygame.K_RIGHT] and player_x < WIDTH - 20:
            player_x += 5

    # Draw Player
    if not game_over:
        draw_ship(player_x, player_y)

    # Move Bullets
    for bullet in bullets[:]:
        bullet[1] -= 8
        line(bullet[0], bullet[1], bullet[0], bullet[1] - 10)
        if bullet[1] < 0:
            bullets.remove(bullet)

    # Spawn Enemies
    spawn_timer += 1
    if spawn_timer > 60:
        spawn_enemy()
        spawn_timer = 0

    # Move Enemies
    for enemy in enemies[:]:
        enemy[1] += 3
        draw_circle(enemy[0], enemy[1], 15)

        # Collision with player
        if abs(enemy[0] - player_x) < 20 and abs(enemy[1] - player_y) < 20:
            game_over = True

        # Collision with bullets
        for bullet in bullets[:]:
            if abs(enemy[0] - bullet[0]) < 15 and abs(enemy[1] - bullet[1]) < 15:
                enemies.remove(enemy)
                bullets.remove(bullet)
                score += 1
                break

        if enemy[1] > HEIGHT:
            enemies.remove(enemy)

    # Score Display
    score_text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, (10, 10))

    if game_over:
        over_text = font.render("GAME OVER", True, RED)
        screen.blit(over_text, (WIDTH//2 - 80, HEIGHT//2))

    pygame.display.flip()
