import pygame
import sys
import random

clock = pygame.time.Clock()

# Setup screen
square_size = 12

screen_cells_width = 40
screen_cells_height = 40
screen = pygame.display.set_mode((screen_cells_width*square_size, screen_cells_height*square_size))

# Misc static
snake_color = (255, 0, 0) # red
food_color = (128, 128, 128) # gray
snake = [(1, 1), (2, 1)]

# Position variables
snake_x = 0
snake_x_direction = 1
snake_y = 0
snake_y_direction = 0

food_x = 5
food_y = 5

def end_game():
    sys.exit(0)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end_game()
        elif event.type == pygame.KEYDOWN:
            key = pygame.key.get_pressed()

            # change dir (WASD or arrow keys)
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                snake_x_direction = -1
                snake_y_direction = 0
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                snake_x_direction = 1
                snake_y_direction = 0
            elif event.key == pygame.K_w or event.key == pygame.K_UP:
                snake_y_direction = -1
                snake_x_direction = 0
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                snake_y_direction = 1
                snake_x_direction = 0

            # Quit
            if event.key == pygame.K_q:
                end_game()

    # Move the snake
    snake_x += snake_x_direction
    snake_y += snake_y_direction

    # detect collision
    if snake_x >= screen_cells_width:
        end_game()
    elif snake_x < 0:
        end_game()
    elif snake_y >= screen_cells_height:
        end_game()
    elif snake_y < 0:
        end_game()
    elif (snake_x, snake_y) in snake:
        end_game()

    # Move snake by adding new location to the end
    snake.append((snake_x, snake_y))

    # Did we eat food this time?
    if food_x == snake_x and food_y == snake_y:

        # find a place for the food that's not in the snake
        while True:
            food_x = random.randint(0, screen_cells_width-1)
            food_y = random.randint(0, screen_cells_height-1)

            if (food_x, food_y) not in snake:
                break

    else:
        snake.pop(0) # Don't extend, if didn't eat anything

    # draw snake
    screen.fill((0, 0, 0)) # black background
    for s in snake:
        pygame.draw.rect(screen, snake_color, pygame.Rect(s[0]*square_size, s[1]*square_size, square_size, square_size))

    # draw food
    pygame.draw.rect(screen, food_color, pygame.Rect(food_x*square_size, food_y*square_size, square_size, square_size))

    # Update display
    pygame.display.flip()

    # Set speed
    clock.tick(6)
