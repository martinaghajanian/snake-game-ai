from random import choice
import numpy as np
from qlearning import train_qlearning, load_q_table
from game import Snake, Fruit, Wall
from utils import *
from bfs import bfs
from gbfs import gbfs
from ga import genetic_algorithm
from astar import astar
from qlearning import get_state, take_action, load_q_table
from monte_carlo import monte_carlo_path
import random

def run_algorithm(mode, seed, Q_table=None):
    """
    Simulates a Snake game using a specific algorithm, without GUI.
    :param mode: The algorithm mode ('BFS', 'GBFS', 'GA', 'Q_LEARNING', 'ASTAR', 'MONTE_CARLO').
    :param seed: Random seed for reproducibility.
    :param Q_table: Pre-trained Q-table for Q-learning (only required for Q_LEARNING mode).
    :return: The score achieved by the algorithm.
    """
    # Set the random seed for reproducibility
    random.seed(seed)
    np.random.seed(seed)

    # Initialize game elements
    snake = Snake()
    fruit = Fruit()
    walls = Wall()
    score = 0

    # Randomize initial snake position and direction
    snake.body = [(random.randint(1, GRID_WIDTH - 2), random.randint(1, GRID_HEIGHT - 2))]
    snake.set_direction(choice([(0, -1), (0, 1), (-1, 0), (1, 0)]))

    # Add border walls
    for x in range(GRID_WIDTH):
        walls.positions.append((x, 0))  # Top border
        walls.positions.append((x, GRID_HEIGHT - 1))  # Bottom border
    for y in range(GRID_HEIGHT):
        walls.positions.append((0, y))  # Left border
        walls.positions.append((GRID_WIDTH - 1, y))  # Right border

    # Randomize initial fruit position
    fruit.new_position(snake.body, walls.positions)

    # Initialize path variables for path-planning algorithms
    path = []

    while True:
        # Logic for each algorithm
        if mode == "Q_LEARNING":
            state = get_state(snake, fruit, walls)
            if state not in Q_table:
                action = choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])  # Random action for unknown state
            else:
                action = max(Q_table[state], key=Q_table[state].get)
            take_action(action, snake)
        elif mode == "BFS":
            if not path:
                path = bfs(snake, fruit, walls)
                if not path:  # No path found
                    return score
            action = path.pop(0)
            take_action(action, snake)
        elif mode == "GBFS":
            if not path:
                path = gbfs(snake, fruit, walls)
                if not path:  # No path found
                    return score
            action = path.pop(0)
            take_action(action, snake)
        elif mode == "GA":
            if not path:
                path = genetic_algorithm(snake, fruit, walls)
                if not path:  # No path found
                    return score
            action = path.pop(0)
            take_action(action, snake)
        elif mode == "ASTAR":
            if not path:
                path = astar(snake, fruit, walls)
                if not path:  # No path found
                    return score
            action = path.pop(0)
            take_action(action, snake)
        elif mode == "MONTE_CARLO":
            try:
                action = monte_carlo_path(snake, fruit, walls)
                if action:
                    take_action(action, snake)
                else:
                    print("No valid Monte Carlo move found.")
                    return score
            except Exception as e:
                print(f"Monte Carlo error: {e}")
                return score
        else:
            raise ValueError(f"Unknown mode: {mode}")

        # Check for collisions
        if snake.check_collision() or snake.check_wall_collision(walls):
            return score

        # Check if the snake eats the fruit
        if snake.body[0] == fruit.position:
            path = []  # Reset the path as the state has changed
            snake.grow()
            score += 10
            walls.add_wall(snake.body, fruit.position)
            fruit.new_position(snake.body, walls.positions)


def analyze_algorithms(runs=50):
    """
    Analyze the performance of different algorithms over a specified number of runs.
    Includes Q-learning with a pre-trained Q-table.
    :param runs: Number of runs for each algorithm.
    :return: A dictionary containing the results for each algorithm.
    """
    algorithms = ["BFS", "GBFS", "GA", "Q_LEARNING", "ASTAR", "MONTE_CARLO"]
    results = {algo: [] for algo in algorithms}

    # Train or load the Q-learning Q-table
    print("Loading Q-learning table...")
    Q_table = load_q_table("q_table.pkl")
    if not Q_table:
        print("Training Q-learning agent...")
        Q_table = train_qlearning()

    # Perform runs
    for run in range(1, runs + 1):
        seed = random.randint(0, 1_000_000)  # Generate a random seed
        print(f"\nRun {run}/{runs} (Seed: {seed}):")

        for algorithm in algorithms:
            try:
                # Pass Q_table only for Q_LEARNING
                if algorithm == "Q_LEARNING":
                    score = run_algorithm(algorithm, seed, Q_table=Q_table)
                else:
                    score = run_algorithm(algorithm, seed)

                results[algorithm].append(score)
                print(f"{algorithm}: Score = {score}")
            except Exception as e:
                print(f"Error in {algorithm} during run {run}: {e}")
                results[algorithm].append(-1)  # Use -1 to indicate an error or failure

    # Calculate average and best scores
    summary = {}
    print("\n--- Summary of Results ---")
    for algorithm in algorithms:
        avg_score = np.mean(results[algorithm])
        best_score = max(results[algorithm])
        summary[algorithm] = {
            "average_score": avg_score,
            "best_score": best_score,
            "scores": results[algorithm],
        }
        print(f"{algorithm}: Average Score = {avg_score:.2f}, Best Score = {best_score}")

    return results, summary


if __name__ == "__main__":
    # Number of runs for analysis
    runs = 1000
    results, summary = analyze_algorithms(runs=runs)

    # Optional: Save results to a JSON file for further analysis
    import json
    with open("algorithm_performance.json", "w") as file:
        json.dump(summary, file, indent=4)

    print("\n--- Results saved to 'algorithm_performance.json' ---")
