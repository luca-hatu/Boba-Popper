import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pop the Bobas')

# Clock to control the frame rate
clock = pygame.time.Clock()

# Boba settings
boba_size = 20
boba_spawn_rate = 30  # Number of frames between each boba spawn
boba_list = []

# Bomb settings
bomb_size = 50
bomb_spawn_rate = 100  # Number of frames between each bomb spawn
bomb_list = []

# Load the bomb image
bomb_image = pygame.image.load('bomb.png')
bomb_image = pygame.transform.scale(bomb_image, (bomb_size, bomb_size))

# Game variables
score = 0
streak = 0

# Font for displaying the score
font = pygame.font.SysFont(None, 36)

# Function to display score
def display_score(score, streak):
    score_text = font.render(f'Score: {score}  Streak: {streak}', True, BLACK)
    screen.blit(score_text, (10, 10))

# Main game loop
frame_count = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill(WHITE)

    # Spawn bobas
    if frame_count % boba_spawn_rate == 0:
        x = random.randint(boba_size, SCREEN_WIDTH - boba_size)
        y = random.randint(boba_size, SCREEN_HEIGHT - boba_size)
        boba_list.append(pygame.Rect(x, y, boba_size, boba_size))

    # Spawn bombs
    if frame_count % bomb_spawn_rate == 0:
        x = random.randint(bomb_size, SCREEN_WIDTH - bomb_size)
        y = random.randint(bomb_size, SCREEN_HEIGHT - bomb_size)
        bomb_list.append(pygame.Rect(x, y, bomb_size, bomb_size))

    # Draw bobas
    for boba in boba_list:
        pygame.draw.circle(screen, BLACK, boba.center, boba_size // 2)

    # Draw bombs
    for bomb in bomb_list:
        screen.blit(bomb_image, bomb.topleft)

    # Check for mouse clicks
    mouse_pressed = pygame.mouse.get_pressed()
    if mouse_pressed[0]:  # Left mouse button
        mouse_pos = pygame.mouse.get_pos()
        for boba in boba_list[:]:
            if boba.collidepoint(mouse_pos):
                boba_list.remove(boba)
                score += 1
                streak += 1

        for bomb in bomb_list[:]:
            if bomb.collidepoint(mouse_pos):
                bomb_list.remove(bomb)
                streak = 0

    # Display score and streak
    display_score(score, streak)

    pygame.display.flip()
    clock.tick(60)
    frame_count += 1

pygame.quit()
sys.exit()
