from random import choice
import pygame
import sys
from game import Snake, Fruit, Wall
from render import initialize_screen, draw_elements
from qlearning import train_qlearning, get_state, take_action, load_q_table
from bfs import *
from gbfs import *
from utils import *
from ga import *
from astar import *
from dfs import dfs  # Import DFS


def main_menu(screen, score=None):
    font = pygame.font.Font(None, 30)

    line1 = "Press 1 for User Mode"
    line2 = "Press 2 for BFS AI"
    line3 = "Press 3 for Monte Carlo AI"
    line4 = "Press 4 for Q-Learning AI"
    line5 = "Press 5 for GBFS AI"
    line6 = "Press 6 for GA AI"
    line7 = "Press 7 for A* AI"
    line8 = "Press 8 for DFS AI"
    score_text = f"Last Score: {score}" if score is not None else ""

    text1 = font.render(line1, True, (255, 255, 255))
    text2 = font.render(line2, True, (255, 255, 255))
    text3 = font.render(line3, True, (255, 255, 255))
    text4 = font.render(line4, True, (255, 255, 255))
    text5 = font.render(line5, True, (255, 255, 255))
    text6 = font.render(line6, True, (255, 255, 255))
    text7 = font.render(line7, True, (255, 255, 255))
    text8 = font.render(line8, True, (255, 255, 255))
    score_display = font.render(score_text, True, (255, 255, 255))

    screen.fill((0, 0, 0))
    screen.blit(text1, (10, 10))
    screen.blit(text2, (10, 40))
    screen.blit(text3, (10, 70))
    screen.blit(text4, (10, 100))
    screen.blit(text5, (10, 130))
    screen.blit(text6, (10, 160))
    screen.blit(text7, (10, 190))
    screen.blit(text8, (10, 220))
    screen.blit(score_display, (10, 250))

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
                    return "BFS"
                elif event.key == pygame.K_3:
                    return "MONTE_CARLO"
                elif event.key == pygame.K_4:
                    return "Q_LEARNING"
                elif event.key == pygame.K_5:
                    return "GBFS"
                elif event.key == pygame.K_6:
                    return "GA"
                elif event.key == pygame.K_7:
                    return "ASTAR"
                elif event.key == pygame.K_8:
                    return "DFS"


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
                action = choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
            else:
                action = max(Q_table[state], key=Q_table[state].get)
            take_action(action, snake)
        elif mode == "BFS":
            bfs_path = [] if 'bfs_path' not in locals() else bfs_path
            if not bfs_path:
                bfs_path = bfs(snake, fruit, walls)
                if not bfs_path:
                    return score
            action = bfs_path.pop(0)
            take_action(action, snake)
        elif mode == "GBFS":
            gbfs_path = [] if 'gbfs_path' not in locals() else gbfs_path
            if not gbfs_path:
                gbfs_path = gbfs(snake, fruit, walls)
                if not gbfs_path:
                    return score
            action = gbfs_path.pop(0)
            take_action(action, snake)
        elif mode == "GA":
            genetic_path = [] if 'genetic_path' not in locals() else genetic_path
            if not genetic_path:
                genetic_path = genetic_algorithm_improved(snake, fruit, walls)
                if not genetic_path:
                    return score
            action = genetic_path.pop(0)
            take_action(action, snake)
        elif mode == "MONTE_CARLO":
            from monte_carlo import monte_carlo_path
            action = monte_carlo_path(snake, fruit, walls)
            if action:
                snake.set_direction(action)
                snake.move()
            else:
                print("No valid Monte Carlo move found.")
                return score
        elif mode == "ASTAR":
            astar_path = [] if 'astar_path' not in locals() else astar_path
            if not astar_path:
                astar_path = astar(snake, fruit, walls)
                if not astar_path:
                    return score
            action = astar_path.pop(0)
            take_action(action, snake)
        elif mode == "DFS":
            dfs_path = [] if 'dfs_path' not in locals() else dfs_path
            if not dfs_path:
                dfs_path = dfs(snake, fruit, walls)
                if not dfs_path:
                    print("DFS could not find a path.")
                    return score
            action = dfs_path.pop(0)
            take_action(action, snake)

        # Check for collisions with walls or boundaries
        if snake.check_collision() or snake.check_wall_collision(walls):
            return score

        # Check if the snake eats the fruit
        if snake.body[0] == fruit.position:
            bfs_path = []
            gbfs_path = []
            astar_path = []
            dfs_path = []
            snake.grow()
            score += 10
            walls.add_wall(snake.body, fruit.position)
            fruit.new_position(snake.body, walls.positions)
            walls_count += 1

        # Draw all elements
        draw_elements(screen, snake, fruit, walls, score, walls_count)

        # Control the game speed
        clock.tick(FPS)


if __name__ == "__main__":
    screen = initialize_screen()
    Q_table = load_q_table("q_table.pkl")
    score = None

    while True:
        mode = main_menu(screen, score)
        score = game_loop(mode, Q_table if mode == "Q_LEARNING" else None)
