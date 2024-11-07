import pygame
from settings import GRID_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, GRID_WIDTH, GRID_HEIGHT, BLACK, GREEN, RED, BLUE, SCALE_FACTOR

def initialize_screen():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake Game with AI")
    return screen

def draw_elements(screen, snake, fruit, walls):
    screen.fill(BLACK)  # Clear the screen

    # Draw top and bottom border walls
    for x in range(GRID_WIDTH):
        pygame.draw.rect(screen, BLUE, pygame.Rect(x * GRID_SIZE * SCALE_FACTOR, 0, GRID_SIZE * SCALE_FACTOR, GRID_SIZE * SCALE_FACTOR))
        pygame.draw.rect(screen, BLUE, pygame.Rect(x * GRID_SIZE * SCALE_FACTOR, (GRID_HEIGHT - 1) * GRID_SIZE * SCALE_FACTOR, GRID_SIZE * SCALE_FACTOR, GRID_SIZE * SCALE_FACTOR))

    # Draw left and right border walls
    for y in range(GRID_HEIGHT):
        pygame.draw.rect(screen, BLUE, pygame.Rect(0, y * GRID_SIZE * SCALE_FACTOR, GRID_SIZE * SCALE_FACTOR, GRID_SIZE * SCALE_FACTOR))
        pygame.draw.rect(screen, BLUE, pygame.Rect((GRID_WIDTH - 1) * GRID_SIZE * SCALE_FACTOR, y * GRID_SIZE * SCALE_FACTOR, GRID_SIZE * SCALE_FACTOR, GRID_SIZE * SCALE_FACTOR))

    # Draw the snake
    for segment in snake.body:
        pygame.draw.rect(screen, GREEN, pygame.Rect(segment[0] * GRID_SIZE * SCALE_FACTOR, segment[1] * GRID_SIZE * SCALE_FACTOR, GRID_SIZE * SCALE_FACTOR, GRID_SIZE * SCALE_FACTOR))

    # Draw the fruit
    pygame.draw.rect(screen, RED, pygame.Rect(fruit.position[0] * GRID_SIZE * SCALE_FACTOR, fruit.position[1] * GRID_SIZE * SCALE_FACTOR, GRID_SIZE * SCALE_FACTOR, GRID_SIZE * SCALE_FACTOR))

    # Draw the walls
    for wall in walls.positions:
        pygame.draw.rect(screen, BLUE, pygame.Rect(wall[0] * GRID_SIZE * SCALE_FACTOR, wall[1] * GRID_SIZE * SCALE_FACTOR, GRID_SIZE * SCALE_FACTOR, GRID_SIZE * SCALE_FACTOR))

    pygame.display.flip()  # Update the display
