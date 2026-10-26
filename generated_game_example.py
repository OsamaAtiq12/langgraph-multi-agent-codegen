import utils.session
import pygame
import sys
import json
import random

# Constants
WIDTH, HEIGHT = 800, 400
INITIAL_SPEED = 5
GRAVITY = 0.5
JUMP_HEIGHT = 15
OBSTACLE_SPAWN_RATE = 0.3  # Lower is faster
CLUSTER_SPAWN_RATE = 0.3
DAY_NIGHT_SWITCH = 100  # Points or seconds
DAY_NIGHT_SWITCH_TIME = 20  # Seconds

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Dino:
    def __init__(self):
        self.x = 50
        self.y = HEIGHT // 2
        self.vy = 0

    def update(self):
        self.vy += GRAVITY
        self.y += self.vy

        if self.y > HEIGHT // 2:
            self.y = HEIGHT // 2
            self.vy = 0

    def jump(self):
        self.vy = -JUMP_HEIGHT

class Obstacle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def update(self, speed):
        self.x -= speed

def draw_text(text, size, x, y, screen, color):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def load_high_score():
    try:
        with open('highscore.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return 0

def save_high_score(score):
    try:
        with open('highscore.json', 'w') as f:
            json.dump(score, f)
    except Exception as e:
        print(f"Error saving high score: {e}")

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

dino = Dino()
obstacles = []
score = 0
high_score = load_high_score()
day = True
last_day_switch = 0
last_day_switch_time = 0
speed = INITIAL_SPEED

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                dino.jump()

    # Update game state
    dino.update()
    for obstacle in obstacles:
        obstacle.update(speed)
        if obstacle.x < -obstacle.width:
            obstacles.remove(obstacle)

    # Spawn new obstacles
    if random.random() < OBSTACLE_SPAWN_RATE / 60:
        if random.random() < CLUSTER_SPAWN_RATE:
            num_obstacles = random.randint(2, 3)
            for i in range(num_obstacles):
                x = WIDTH + i * 50
                y = random.randint(0, HEIGHT - 50)
                obstacles.append(Obstacle(x, y, 50, 50))
        else:
            x = WIDTH
            y = random.randint(0, HEIGHT - 50)
            obstacles.append(Obstacle(x, y, 50, 50))

    # Collision detection
    for obstacle in obstacles:
        if (obstacle.x < dino.x + 50 and
            obstacle.x + obstacle.width > dino.x and
            obstacle.y < dino.y + 50 and
            obstacle.y + obstacle.height > dino.y):
            running = False

    # Day/night cycle
    if score // DAY_NIGHT_SWITCH != last_day_switch:
        last_day_switch = score // DAY_NIGHT_SWITCH
        day = not day
    if pygame.time.get_ticks() - last_day_switch_time > DAY_NIGHT_SWITCH_TIME * 1000:
        last_day_switch_time = pygame.time.get_ticks()
        day = not day

    # Speed scaling
    speed = INITIAL_SPEED + int(score // 100)

    # Draw everything
    screen.fill(BLACK if day else WHITE)
    pygame.draw.rect(screen, WHITE if day else BLACK, (dino.x, dino.y, 50, 50))
    for obstacle in obstacles:
        pygame.draw.rect(screen, WHITE if day else BLACK, (obstacle.x, obstacle.y, obstacle.width, obstacle.height))
    draw_text(f'Score: {int(score)}', 32, 10, 10, screen, WHITE if day else BLACK)
    draw_text(f'High Score: {high_score}', 32, 10, 50, screen, WHITE if day else BLACK)

    # Update score
    score += 1 / 60

    pygame.display.flip()
    clock.tick(60)

# Save high score
if score > high_score:
    save_high_score(int(score))

pygame.quit()
sys.exit()