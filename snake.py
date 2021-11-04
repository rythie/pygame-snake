import pygame
import sys
import random

pygame.init()
clock = pygame.time.Clock()

# Setup screen
square_size = 18

screen_cells_width = 40
screen_cells_height = 40
screen = pygame.display.set_mode((screen_cells_width*square_size, screen_cells_height*square_size))

pause_font = pygame.font.SysFont('Helvetica', 100)
#pause_font = pygame.font.Font(None, 100)

# Misc static
food_color = (0, 200, 100)
snake = [(1, 1), (2, 1)]

obstacle = []
obstacle_color = (255, 255, 255)
new_obstacle = True

colors = [(255, 0, 0),
          (0, 255, 0),
          (0, 0, 255),
          (255, 128, 0),
          (128, 255, 0),
          (0, 128, 255)]
snake_color = colors[0]

# Position variables
snake_x = 0
snake_x_direction = 1
snake_y = 0
snake_y_direction = 0

food_x = random.randint(0, screen_cells_width-1)
food_y = random.randint(0, screen_cells_height-1)

def end_game():
    print("Score:", len(snake))
    sys.exit(0)

def pause_game():
    restart_game = False

    pause_box_width = 430
    pause_box_height = 120
    pause_box_x = (screen_cells_width*square_size - pause_box_width)/2
    pause_box_y = (screen_cells_height*square_size - pause_box_height)/2
    pygame.draw.rect(screen, (0,0,0), (pause_box_x, pause_box_y, pause_box_width, pause_box_height))
    pygame.draw.rect(screen, (255,255,255), (pause_box_x, pause_box_y, pause_box_width, pause_box_height), width=2)

    pause_text = pause_font.render("PAUSED", True, (255, 255, 255))
    screen.blit(pause_text, (pause_box_x+10, pause_box_y+20))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end_game()
            elif event.type == pygame.KEYDOWN:
                # Quit
                if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    end_game()
                else:
                    return

        clock.tick(10)

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

            # Pause
            if event.key == pygame.K_p or event.key == pygame.K_SPACE:
                pause_game()

            # Quit
            if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
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
    elif (snake_x, snake_y) in obstacle:
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

        if len(snake) % 10 == 0:
            new_obstacle = True

    else:
        snake.pop(0) # Don't extend, if didn't eat anything

    # draw snake
    screen.fill((0, 0, 0)) # black background
    for s in snake:
        pygame.draw.rect(screen, snake_color, pygame.Rect(s[0]*square_size, s[1]*square_size, square_size, square_size))

    # draw obstacle
    if new_obstacle:
        obstacle = []
        for x in range(0, 10):
            obstacle_x = random.randint(0, screen_cells_width-1)
            obstacle_y = random.randint(0, screen_cells_height-1)
            if (obstacle_x, obstacle_y) in snake:
                pass # obstacle was in snake
            elif (obstacle_x, obstacle_y) is (food_x, food_y):
                pass # obstacle was in food
            else:
                obstacle.append((obstacle_x, obstacle_y))

        new_obstacle = False

    for s in obstacle:
        pygame.draw.rect(screen, obstacle_color, pygame.Rect(s[0]*square_size, s[1]*square_size, square_size, square_size))

    # draw food
    pygame.draw.rect(screen, food_color, pygame.Rect(food_x*square_size, food_y*square_size, square_size, square_size))

    # Update display
    pygame.display.flip()

    level = int(len(snake) / 10)
    snake_color = colors[level % len(colors)] # change snake color with level
    fps = 6 + (2*level) # get faster in later levels
    clock.tick(fps)
