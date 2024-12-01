from random import choice
import pygame
import sys
from settings import FPS, GRID_WIDTH, GRID_HEIGHT
from game import Snake, Fruit, Wall
from render import initialize_screen, draw_elements
from qlearning import train_qlearning, get_state, take_action, load_q_table


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


def game_loop(mode, Q_table=None):
    screen = initialize_screen()
    clock = pygame.time.Clock()

    snake = Snake()
    fruit = Fruit()
    walls = Wall()
    score = 0  # Initialize score counter
    walls_count = 0  # Initialize wall counter

    # Add border walls to the walls object
    for x in range(GRID_WIDTH):
        walls.positions.append((x, 0))  # Top border
        walls.positions.append((x, GRID_HEIGHT - 1))  # Bottom border
    for y in range(GRID_HEIGHT):
        walls.positions.append((0, y))  # Left border
        walls.positions.append((GRID_WIDTH - 1, y))  # Right border

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
        elif mode == "Q_LEARNING":
            state = get_state(snake, fruit, walls)
            if state not in Q_table:
                print(f"State {state} not found in Q-table. Taking random action.")
                action = choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
            else:
                action = max(Q_table[state], key=Q_table[state].get)
                print("action found in q table")
            take_action(action, snake)  # Execute the chosen action

        # Check for collisions with walls or boundaries
        if snake.check_collision() or snake.check_wall_collision(walls):
            return score  # Return the score to main menu on game over

        # Check if the snake eats the fruit
        if snake.body[0] == fruit.position:
            snake.grow()
            score += 10
            walls.add_wall(snake.body, fruit.position)
            walls_count += 1
            fruit.new_position(snake.body, walls.positions)

        # Draw all elements, including score and wall count
        draw_elements(screen, snake, fruit, walls, score, walls_count)

        # Control the game speed
        clock.tick(FPS)


if __name__ == "__main__":
    screen = initialize_screen()

    # Load an existing Q-table or train a new one
    Q_table = load_q_table("q_table.pkl")
    if not Q_table:
        Q_table = train_qlearning()

    score = None

    while True:
        mode = main_menu(screen, score)
        score = game_loop(mode, Q_table if mode == "Q_LEARNING" else None)
