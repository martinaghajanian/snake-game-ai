import random
from settings import GRID_WIDTH, GRID_HEIGHT


class Snake:
    def __init__(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (0, -1)  # Initial direction (moving upward)

    def move(self):
        head_x, head_y = self.body[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)
        self.body = [new_head] + self.body[:-1]

    def grow(self):
        # Add a new segment to the snake at the tail position
        self.body.append(self.body[-1])

    def set_direction(self, direction):
        # Prevent the snake from reversing
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.direction = direction

    def check_collision(self):
        # Check if the snake's head collides with its body
        head = self.body[0]
        return head in self.body[1:]

    def check_wall_collision(self, walls):
        head_x, head_y = self.body[0]
        # Check collision with border walls or grid boundaries
        if head_x < 0 or head_x >= GRID_WIDTH or head_y < 0 or head_y >= GRID_HEIGHT:
            return True
        # Check collision with internal walls
        return (head_x, head_y) in walls.positions


class Fruit:
    def __init__(self):
        self.position = self.random_position()

    def random_position(self):
        return (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

    def new_position(self, snake_body, wall_positions):
        # Ensure fruit doesn't spawn on the snake or walls
        while True:
            self.position = self.random_position()
            if self.position not in snake_body and self.position not in wall_positions:
                break


class Wall:
    def __init__(self):
        self.positions = []

    def add_wall(self, snake_body, fruit_position):

        def is_adjacent_or_diagonal(pos, walls):
            # Check if the position is adjacent or diagonal to any existing wall
            x, y = pos
            neighbors = [
                (x - 1, y - 1), (x, y - 1), (x + 1, y - 1),
                (x - 1, y), (x + 1, y),
                (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)
            ]
            return any(neighbor in walls for neighbor in neighbors)

        # Collect all potential positions on the grid
        potential_positions = [
            (x, y)
            for x in range(GRID_WIDTH)
            for y in range(GRID_HEIGHT)
            if (x, y) not in snake_body
               and (x, y) != fruit_position
               and (x, y) not in self.positions
               and not is_adjacent_or_diagonal((x, y), self.positions)
        ]

        # Check if there are any valid positions left
        if potential_positions:
            new_wall = random.choice(potential_positions)  # Choose a random valid position
            self.positions.append(new_wall)
        else:
            print("No space available to add a new wall.")
