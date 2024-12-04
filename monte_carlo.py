import numpy as np
from game import Snake, Fruit, Wall
from settings import GRID_WIDTH, GRID_HEIGHT

class MonteCarloAgent:
    def __init__(self, num_simulations=50):
        self.num_simulations = num_simulations

    def simulate_game(self, initial_snake, initial_fruit, initial_walls):
        """
        Run a Monte Carlo simulation to predict the best move
        """
        possible_moves = [
            ((0, -1), "UP"),
            ((0, 1), "DOWN"),
            ((-1, 0), "LEFT"),
            ((1, 0), "RIGHT")
        ]
        move_scores = {move[1]: 0 for move in possible_moves}

        for move, move_name in possible_moves:
            simulation_scores = []
            for _ in range(self.num_simulations):
                # Deep copy game state
                snake = Snake()
                snake.body = initial_snake.body.copy()
                snake.direction = move
                snake.set_direction(move)  # Ensure valid direction

                fruit = Fruit()
                fruit.position = initial_fruit.position

                walls = Wall()
                walls.positions = initial_walls.positions.copy()

                # Simulate game progression with this move
                simulation_score = self._run_simulation(snake, fruit, walls)
                simulation_scores.append(simulation_score)

            # Calculate average score for this move
            move_scores[move_name] = np.mean(simulation_scores)

        # Choose move with highest average score
        best_move = max(move_scores, key=move_scores.get)
        # print(f"Move scores: {move_scores}")  # Debug print
        return best_move

    def _run_simulation(self, snake, fruit, walls, max_steps=100):
        """
        Run a single game simulation
        """
        steps = 0
        while steps < max_steps:
            snake.move()
            steps += 1

            # Check collisions
            if (snake.check_collision() or
                    snake.check_wall_collision(walls) or
                    snake.body[0][0] < 0 or snake.body[0][0] >= GRID_WIDTH or
                    snake.body[0][1] < 0 or snake.body[0][1] >= GRID_HEIGHT):
                return -100  # High penalty for early termination

            # Check if snake eats fruit
            if snake.body[0] == fruit.position:
                snake.grow()
                walls.add_wall(snake.body, fruit.position)
                fruit.new_position(snake.body, walls.positions)
                return 100  # High reward for eating fruit

            # Bonus for moving towards fruit
            distance_to_fruit = self._manhattan_distance(snake.body[0], fruit.position)
            return max(10 - distance_to_fruit, -10)

        return 0  # Neutral result if max steps reached

    def _manhattan_distance(self, point1, point2):
        """
        Calculate Manhattan distance between two points
        """
        return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])


def monte_carlo_path(snake, fruit, walls):
    """
    Interface function for game loop to get Monte Carlo move
    """
    agent = MonteCarloAgent()
    best_move = agent.simulate_game(snake, fruit, walls)

    # Map move name to direction
    move_map = {
        "UP": (0, -1),
        "DOWN": (0, 1),
        "LEFT": (-1, 0),
        "RIGHT": (1, 0)
    }
    return move_map[best_move]
