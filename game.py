import random

import pygame

# Initialize Constants
WINDOW_SIZE = 500
SNAKE_SIZE = 10
FPS = 15

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Initialize Pygame
pygame.init()
clock = pygame.time.Clock()
game_window = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption('Snake Game')

# Function Definitions
def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(game_window, ac, (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(game_window, ic, (x, y, w, h))

    font = pygame.font.SysFont("Arial", 20)
    text_surf = font.render(msg, True, BLACK)
    text_rect = text_surf.get_rect()
    text_rect.center = ((x + (w / 2)), (y + (h / 2)))
    game_window.blit(text_surf, text_rect)

def game_intro():
    intro = True
    # Load the background image
    background_image = pygame.image.load("background.png")
    background_image = pygame.transform.scale(background_image, (WINDOW_SIZE, WINDOW_SIZE))  # Scale the image to fit the window
    
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        # Draw the background image
        game_window.blit(background_image, [0, 0])

        button("Play", 150, 250, 100, 50, GREEN, (0, 128, 0), game_loop)
        button("About", 275, 250, 100, 50, (128, 128, 128), (64, 64, 64), about_page)
        button("Quit", 400, 250, 100, 50, RED, (128, 0, 0), quit_game)
        pygame.display.update()
        clock.tick(15)

def about_page():
    about = True
    while about:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        game_window.fill(WHITE)
        button("Back", 400, 450, 100, 50, (128, 128, 128), (64, 64, 64), game_intro)
        pygame.display.update()
        clock.tick(15)

def quit_game():
    pygame.quit()
    quit()

def check_collision():
    """Check if the snake has collided with the wall or itself."""
    global game_over
    if (snake_pos[0] < 0 or snake_pos[0] >= WINDOW_SIZE or
            snake_pos[1] < 0 or snake_pos[1] >= WINDOW_SIZE):
        game_over = True  # End the game if collision with boundary
    for block in snake_body[1:]:
        if snake_pos == block:
            game_over = True  # End the game if collision with itself

def game_over_screen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        game_window.fill(WHITE)
        font = pygame.font.SysFont("Arial", 50)
        text = font.render("Game Over", True, BLACK)
        game_window.blit(text, [WINDOW_SIZE // 4, WINDOW_SIZE // 4])
        
        button("Play Again", 150, 250, 150, 50, GREEN, (0, 128, 0), restart_game)
        button("Quit", 350, 250, 100, 50, RED, (128, 0, 0), quit_game)
        
        pygame.display.update()
        clock.tick(15)

def restart_game():
    global snake_pos, snake_body, food_pos, food_spawned, direction, score, game_over
    snake_pos = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50]]
    food_pos = [0, 0]
    food_spawned = False
    direction = 'RIGHT'
    score = 0
    game_over = False
    game_loop()



def game_loop():
    global snake_pos, snake_body, food_pos, food_spawned, direction, score, game_over

    snake_pos = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50]]
    food_pos = [0, 0]
    food_spawned = False
    direction = 'RIGHT'
    score = 0
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    direction = 'RIGHT'
                elif event.key == pygame.K_LEFT:
                    direction = 'LEFT'
                elif event.key == pygame.K_UP:
                    direction = 'UP'
                elif event.key == pygame.K_DOWN:
                    direction = 'DOWN'

        if direction == 'RIGHT':
            snake_pos[0] += SNAKE_SIZE
        elif direction == 'LEFT':
            snake_pos[0] -= SNAKE_SIZE
        elif direction == 'UP':
            snake_pos[1] -= SNAKE_SIZE
        elif direction == 'DOWN':
            snake_pos[1] += SNAKE_SIZE

        check_collision()  # Check for collision

        # If game_over is True, call game_over_screen
        if game_over:
            game_over_screen()
            break

        # If game_over is True, break from the while loop
        if game_over:
            break

        snake_body.insert(0, list(snake_pos))
        if snake_pos == food_pos:
            score += 10
            food_spawned = False
        else:
            snake_body.pop()

        if not food_spawned:
            food_pos = [random.randrange(1, (WINDOW_SIZE // SNAKE_SIZE)) * SNAKE_SIZE,
                        random.randrange(1, (WINDOW_SIZE // SNAKE_SIZE)) * SNAKE_SIZE]
            food_spawned = True

        game_window.fill(BLACK)
        for pos in snake_body:
            pygame.draw.rect(game_window, GREEN, [pos[0], pos[1], SNAKE_SIZE, SNAKE_SIZE])
        pygame.draw.rect(game_window, RED, [food_pos[0], food_pos[1], SNAKE_SIZE, SNAKE_SIZE])
        font = pygame.font.SysFont('Arial', 20)
        score_text = font.render(f"Score: {score}", True, WHITE)
        game_window.blit(score_text, [10, 10])

        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    game_intro()
    
