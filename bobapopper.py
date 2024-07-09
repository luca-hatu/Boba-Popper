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
# Define the background color (change this to your desired color)
BACKGROUND_COLOR = (173, 216, 230)  # Light blue

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pop the Bobas')

# Clock to control the frame rate
clock = pygame.time.Clock()

# Load sounds
pop_sound = pygame.mixer.Sound('pop.mp3')
explosion_sound = pygame.mixer.Sound('explosion.mp3')
booster_sound = pygame.mixer.Sound('booster.mp3')
bubble_tea_sound = pygame.mixer.Sound('shake.mp3')
shield_sound = pygame.mixer.Sound('booster.mp3')

# Boba settings
boba_size = 40
boba_spawn_rate = 30  # Number of frames between each boba spawn
boba_list = []

# Load the boba image
boba_image = pygame.image.load('boba.png')
boba_image = pygame.transform.scale(boba_image, (boba_size, boba_size))

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

# Load bubble tea image
bubble_tea_image = pygame.image.load('bubble-tea.png')
bubble_tea_image = pygame.transform.scale(bubble_tea_image, (50, 50))
bubble_tea_count = 0
bubble_tea_display_time = 200  # Frames to display bubble tea
bubble_tea_rect = None

# Load booster image
booster_image = pygame.image.load('booster.png')
booster_image = pygame.transform.scale(booster_image, (30, 30))
shield_booster_image = pygame.image.load('shield.png')
shield_booster_image = pygame.transform.scale(shield_booster_image, (30, 30))

booster_list = []
booster_spawn_rate = 300  # Number of frames between each booster spawn
booster_effect_duration = 600  # Duration of the booster effect in frames
booster_active = False
booster_timer = 0

shield_list = []
shield_spawn_rate = 500  # Number of frames between each shield spawn
shield_effect_duration = 600  # Duration of the shield effect in frames
shield_active = False
shield_timer = 0

# Position to display bubble tea count
bubble_tea_display_pos = (650, 10)

# Game variables
score = 0
streak = 0
lives = 3
max_lives = 3

# Leaderboard variables
high_scores = []
last_eight_scores = []

# Blinking variables
blink_duration = 500  # Duration of the blink in milliseconds
blink_start_time = None

# Font for displaying the score and game over text
font = pygame.font.SysFont(None, 36)
game_over_font = pygame.font.SysFont(None, 72)

# Function to display score and lives
def display_score_and_lives(score, streak, lives, bubble_tea_count):
    score_text = font.render(f'Score: {score}  Streak: {streak}', True, BLACK)
    screen.blit(score_text, (10, 10))
    
    current_time = pygame.time.get_ticks()
    for i in range(max_lives):
        if i < lives:
            if blink_start_time and current_time - blink_start_time < blink_duration and i == lives:
                if (current_time // 100) % 2 == 0:
                    screen.blit(empty_heart_image, (10 + i * 35, 50))
                else:
                    screen.blit(full_heart_image, (10 + i * 35, 50))
            else:
                screen.blit(full_heart_image, (10 + i * 35, 50))
        else:
            screen.blit(empty_heart_image, (10 + i * 35, 50))
    
    if bubble_tea_count > 0:
        bubble_tea_text = font.render(f'x{bubble_tea_count}', True, BLACK)
        screen.blit(bubble_tea_image, bubble_tea_display_pos)
        screen.blit(bubble_tea_text, (bubble_tea_display_pos[0] + 50, bubble_tea_display_pos[1] + 10))

# Function to display game over screen and handle restart
def display_game_over():
    global score, streak, lives, bubble_tea_count, high_scores, last_eight_scores
    
    game_over_text = game_over_font.render('Game Over', True, RED)
    score_text = font.render(f'Final Score: {score}', True, BLACK)
    
    # Update leaderboard
    high_scores.append(score)
    high_scores = sorted(high_scores, reverse=True)[:3]
    last_eight_scores.append(score)
    last_eight_scores = last_eight_scores[-8:]
    
    # Display game over and final score
    screen.fill(WHITE)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 + game_over_text.get_height() // 2))

    # Create restart button
    restart_button = pygame.Rect(300, 400, 200, 50)
    pygame.draw.rect(screen, BLACK, restart_button)
    restart_text = font.render('Restart', True, WHITE)
    screen.blit(restart_text, (restart_button.centerx - restart_text.get_width() // 2, restart_button.centery - restart_text.get_height() // 2))

    # Create leaderboard button
    leaderboard_button = pygame.Rect(300, 470, 200, 50)
    pygame.draw.rect(screen, BLACK, leaderboard_button)
    leaderboard_text = font.render('Leaderboard', True, WHITE)
    screen.blit(leaderboard_text, (leaderboard_button.centerx - leaderboard_text.get_width() // 2, leaderboard_button.centery - leaderboard_text.get_height() // 2))

    pygame.display.flip()

    # Wait for player to click restart or leaderboard
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if restart_button.collidepoint(mouse_pos):
                    # Reset game variables
                    score = 0
                    streak = 0
                    lives = 3
                    bubble_tea_count = 0
                    return 'restart'
                elif leaderboard_button.collidepoint(mouse_pos):
                    return 'leaderboard'
    return 'quit'

# Function to display leaderboard
def display_leaderboard():
    screen.fill(WHITE)
    
    # Display top 3 scores
    top_scores_text = game_over_font.render('Top 3 Scores', True, BLACK)
    screen.blit(top_scores_text, (SCREEN_WIDTH // 2 - top_scores_text.get_width() // 2, 50))
    for i, score in enumerate(high_scores):
        score_text = font.render(f'{i+1}. {score}', True, BLACK)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 120 + i * 40))
    
    # Display last 8 scores
    last_scores_text = game_over_font.render('Last 8 Games', True, BLACK)
    screen.blit(last_scores_text, (SCREEN_WIDTH // 2 - last_scores_text.get_width() // 2, 300))
    for i, score in enumerate(last_eight_scores):
        score_text = font.render(f'{i+1}. {score}', True, BLACK)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 370 + i * 40))

    # Create back button
    back_button = pygame.Rect(300, 550, 200, 50)
    pygame.draw.rect(screen, BLACK, back_button)
    back_text = font.render('Back', True, WHITE)
    screen.blit(back_text, (back_button.centerx - back_text.get_width() // 2, back_button.centery - back_text.get_height() // 2))
    
    pygame.display.flip()

    # Wait for player to click back
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if back_button.collidepoint(mouse_pos):
                    return

# Main game loop
frame_count = 0
running = True
bubble_tea_timer = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Fill the screen with the background color
    screen.fill(BACKGROUND_COLOR)

    # Check if the player has no lives left
    if lives <= 0:
        action = display_game_over()
        if action == 'restart':
            frame_count = 0
            boba_list = []
            bomb_list = []
            booster_list = []
            shield_list = []
            continue
        elif action == 'leaderboard':
            display_leaderboard()
            continue
        else:
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

    # Spawn boosters
    if frame_count % booster_spawn_rate == 0:
        x = random.randint(booster_image.get_width(), SCREEN_WIDTH - booster_image.get_width())
        y = random.randint(booster_image.get_height(), SCREEN_HEIGHT - booster_image.get_height())
        booster_list.append(pygame.Rect(x, y, booster_image.get_width(), booster_image.get_height()))

    # Spawn shield boosters
    if frame_count % shield_spawn_rate == 0:
        x = random.randint(shield_booster_image.get_width(), SCREEN_WIDTH - shield_booster_image.get_width())
        y = random.randint(shield_booster_image.get_height(), SCREEN_HEIGHT - shield_booster_image.get_height())
        shield_list.append(pygame.Rect(x, y, shield_booster_image.get_width(), shield_booster_image.get_height()))


    # Draw bobas
    for boba in boba_list:
        screen.blit(boba_image, boba.topleft)

    # Draw bombs
    for bomb in bomb_list:
        screen.blit(bomb_image, bomb.topleft)
    
    # Draw boosters
    for booster in booster_list:
        screen.blit(booster_image, booster.topleft)
    
    # Draw shield boosters
    for shield in shield_list:
        screen.blit(shield_booster_image, shield.topleft)

    # Check for mouse clicks
    mouse_pressed = pygame.mouse.get_pressed()
    if mouse_pressed[0]:  # Left mouse button
        mouse_pos = pygame.mouse.get_pos()
        for boba in boba_list[:]:
            if boba.collidepoint(mouse_pos):
                boba_list.remove(boba)
                score += 1 * (2 if booster_active else 1)
                streak += 1
                pop_sound.play()

                # Check if a bubble tea should appear
                if score % 10 == 0:
                    x = random.randint(boba_size, SCREEN_WIDTH - boba_size)
                    y = random.randint(boba_size, SCREEN_HEIGHT - boba_size)
                    bubble_tea_rect = pygame.Rect(x, y, 50, 50)
                    bubble_tea_timer = bubble_tea_display_time

        for bomb in bomb_list[:]:
            if bomb.collidepoint(mouse_pos):
                if shield_active:
                    bomb_list.remove(bomb)
                    explosion_sound.play()
                    shield_active = False
                else:
                    bomb_list.remove(bomb)
                    streak = 0
                    lives -= 1
                    explosion_sound.play()
                    blink_start_time = pygame.time.get_ticks()
        
        for booster in booster_list[:]:
            if booster.collidepoint(mouse_pos):
                booster_list.remove(booster)
                booster_active = True
                booster_timer = booster_effect_duration
                booster_sound.play()

        for shield in shield_list[:]:
            if shield.collidepoint(mouse_pos):
                shield_list.remove(shield)
                shield_active = True
                shield_timer = shield_effect_duration
                shield_sound.play()

        if bubble_tea_rect and bubble_tea_rect.collidepoint(mouse_pos):
            bubble_tea_rect = None
            bubble_tea_count += 1
            bubble_tea_sound.play()

    # Draw bubble tea if it should be displayed
    if bubble_tea_rect and bubble_tea_timer > 0:
        screen.blit(bubble_tea_image, bubble_tea_rect.topleft)
        bubble_tea_timer -= 1

    # Update booster state
    if booster_active:
        booster_timer -= 1
        if booster_timer <= 0:
            booster_active = False

    # Update shield state
    if shield_active:
        shield_timer -= 1
        if shield_timer <= 0:
            shield_active = False
    
    # Display score, streak, and lives
    display_score_and_lives(score, streak, lives, bubble_tea_count)

    pygame.display.flip()
    clock.tick(60)
    frame_count += 1

pygame.quit()
sys.exit()
