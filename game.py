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
        # Check if the snake's head collides with any wall
        head = self.body[0]
        return head in walls.positions
