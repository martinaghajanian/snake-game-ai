import pygame
import sys
from settings import FPS, GRID_WIDTH, GRID_HEIGHT
from game import Snake, Fruit, Wall
from render import initialize_screen, draw_elements


def main_menu(screen, score=None):
    # Use a readable font size
    font = pygame.font.Font(None, 30)

    # Define each line of text separately
    line1 = "Press 1 for User Mode"
    line2 = "Press 2 for And-Or AI"
    line3 = "Press 3 for Monte Carlo AI"
    line4 = "Press 4 for Q-Learning AI"
    score_text = f"Last Score: {score}" if score is not None else ""  # Display score if available

    # Render each line of text
    text1 = font.render(line1, True, (255, 255, 255))
    text2 = font.render(line2, True, (255, 255, 255))
    text3 = font.render(line3, True, (255, 255, 255))
    text4 = font.render(line4, True, (255, 255, 255))
    score_display = font.render(score_text, True, (255, 255, 255))

    # Clear the screen
    screen.fill((0, 0, 0))

    # Display each line at a specified position, with spacing between lines
    screen.blit(text1, (10, 10))
    screen.blit(text2, (10, 40))
    screen.blit(text3, (10, 70))
    screen.blit(text4, (10, 100))
    screen.blit(score_display, (10, 130))  # Display score below menu options

    # Update the display to show the text
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "USER"
                elif event.key == pygame.K_2:
                    return "AND_OR"
                elif event.key == pygame.K_3:
                    return "MONTE_CARLO"
                elif event.key == pygame.K_4:
                    return "Q_LEARNING"


def game_loop(mode):
    screen = initialize_screen()
    clock = pygame.time.Clock()

    snake = Snake()
    fruit = Fruit()
    walls = Wall()  # Reinitialize walls each time game starts
    score = 0

    # Add border walls to the walls object
    for x in range(GRID_WIDTH):
        walls.positions.append((x, 0))  # Top border
        walls.positions.append((x, GRID_HEIGHT - 1))  # Bottom border
    for y in range(GRID_HEIGHT):
        walls.positions.append((0, y))  # Left border
        walls.positions.append((GRID_WIDTH - 1, y))  # Right border

    # Reinitialize the fruit to avoid conflict with walls
    fruit.new_position(snake.body, walls.positions)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif mode == "USER" and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.set_direction((0, -1))
                elif event.key == pygame.K_DOWN:
                    snake.set_direction((0, 1))
                elif event.key == pygame.K_LEFT:
                    snake.set_direction((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    snake.set_direction((1, 0))

        # Snake movement and logic based on the mode
        if mode == "USER":
            snake.move()
        else:
            # AI logic to set snake direction goes here
            pass

        # Check for collisions with walls or boundaries
        if snake.check_collision() or snake.check_wall_collision(walls):
            return score  # Return the score to main menu on game over

        # Check if the snake eats the fruit
        if snake.body[0] == fruit.position:
            snake.grow()
            score += 1
            walls.add_wall(snake.body, fruit.position)
            fruit.new_position(snake.body, walls.positions)

        # Draw all elements
        draw_elements(screen, snake, fruit, walls)

        # Control the game speed
        clock.tick(FPS)


if __name__ == "__main__":
    screen = initialize_screen()

    score = None  # Initialize score to None for the first game

    while True:
        # Show the main menu and get the selected mode
        mode = main_menu(screen, score)

        # Start the game loop with the selected mode and capture the score
        score = game_loop(mode)  # game_loop will return the score after game over