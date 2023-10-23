import random

import pygame

# initialize pygame
pygame.init()

# set up the game window
window_width = 500
window_height = 500
game_window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Snake Game')

# set up the clock
clock = pygame.time.Clock()

# define colors
white = pygame.Color(255, 255, 255)
black = pygame.Color(0, 0, 0)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)

# create the snake and food objects
snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]
food_pos = [random.randrange(1, (window_width//10)) * 10, 
            random.randrange(1, (window_height//10)) * 10]
food_spawned = True

# define the movement of the snake
direction = 'RIGHT'
change_to = direction

# define the game over condition and score
game_over = False
score = 0

# main game loop
while not game_over:
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'
            elif event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            elif event.key == pygame.K_UP:
                change_to = 'UP'
            elif event.key == pygame.K_DOWN:
                change_to = 'DOWN'

    # check for direction change
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'
    elif change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    elif change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    elif change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'

    # update snake position
    if direction == 'RIGHT':
        snake_pos[0] += 10
    elif direction == 'LEFT':
        snake_pos[0] -= 10
    elif direction == 'UP':
        snake_pos[1] -= 10
    elif direction == 'DOWN':
        snake_pos[1] += 10

    # add snake body segment
    snake_body.insert(0, list(snake_pos))
    if snake_pos == food_pos:
        food_spawned = False
        score += 10
    else:
        snake_body.pop()

    # spawn new food
    if not food_spawned:
        food_pos = [random.randrange(1, (window_width//10)) * 10, 
                    random.randrange(1, (window_height//10)) * 10]
        food_spawned = True

    # draw game objects
    game_window.fill(black)
    for pos in snake_body:
        pygame.draw.rect(game_window, green, pygame.Rect(
            pos[0], pos[1], 10, 10))
    pygame.draw.rect(game_window, red, pygame.Rect(
        food_pos[0], food_pos[1], 10, 10))

    # check for collisions
    if snake_pos[0] < 0 or snake_pos[0] > window_width-10:
        game_over = True
    elif snake_pos[1] < 0 or snake_pos[1] > window_height-10:
        game_over = True
    for block in snake_body[1:]:
        if snake_pos == block:
            game_over = True

    # update the game window
    pygame.display.update()

    # set the game over condition and display the score
    if game_over:
        font = pygame.font.SysFont('Arial', 30)
        text = font.render('Game Over!', True, white)
        game_window.blit(text, (window_width/2 - text.get_width()/2,
                                window_height/2 - text.get_height()/2))
        pygame.display.update()
        pygame.time.wait(3000)
        pygame.quit()
        quit()

    # set the game speed
    clock.tick(15)    
    pygame.time.wait(50)
