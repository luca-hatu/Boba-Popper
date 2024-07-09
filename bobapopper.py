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
BACKGROUND_COLOR = (176, 127, 76)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Boba Popper')

# Clock to control the frame rate
clock = pygame.time.Clock()

# Load sounds
pop_sound = pygame.mixer.Sound('pop.mp3')
explosion_sound = pygame.mixer.Sound('explosion.mp3')

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

# Load heart images
full_heart_image = pygame.image.load('full-heart.png')
empty_heart_image = pygame.image.load('empty-heart.png')
full_heart_image = pygame.transform.scale(full_heart_image, (30, 30))
empty_heart_image = pygame.transform.scale(empty_heart_image, (30, 30))

# Game variables
score = 0
streak = 0
lives = 3
max_lives = 3

# Font for displaying the score and game over text
font = pygame.font.SysFont(None, 36)
game_over_font = pygame.font.SysFont(None, 72)

# Function to display score and lives
def display_score_and_lives(score, streak, lives):
    score_text = font.render(f'Score: {score}  Streak: {streak}', True, BLACK)
    screen.blit(score_text, (10, 10))
    
    # Display hearts
    for i in range(max_lives):
        if i < lives:
            screen.blit(full_heart_image, (10 + i * 35, 50))
        else:
            screen.blit(empty_heart_image, (10 + i * 35, 50))
    
    current_time = pygame.time.get_ticks()

# Function to display game over screen
def display_game_over():
    game_over_text = game_over_font.render('Game Over', True, RED)
    score_text = font.render(f'Final Score: {score}', True, BLACK)
    screen.fill(WHITE)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 + game_over_text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(3000)

# Main game loop
frame_count = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill(BACKGROUND_COLOR)

    # Check if the player has no lives left
    if lives <= 0:
        display_game_over()
        running = False
        break

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
                pop_sound.play()

        for bomb in bomb_list[:]:
            if bomb.collidepoint(mouse_pos):
                bomb_list.remove(bomb)
                streak = 0
                lives -= 1
                explosion_sound.play()
                blink_start_time = pygame.time.get_ticks()

    # Display score, streak, and lives
    display_score_and_lives(score, streak, lives)

    pygame.display.flip()
    clock.tick(60)
    frame_count += 1

pygame.quit()
sys.exit()
