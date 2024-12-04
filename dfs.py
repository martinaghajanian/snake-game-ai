from utils import *

def dfs(snake, fruit, walls):
    """
    Depth-First Search (DFS) to find a path to the fruit.
    :param snake: The Snake object.
    :param fruit: The Fruit object.
    :param walls: The Wall object.
    :return: A list of actions (UP, DOWN, LEFT, RIGHT) representing a path to the fruit.
    """
    start = snake.body[0]  # Snake head position
    goal = fruit.position

    directions = [
        (0, -1, 'UP'),  # Up
        (0, 1, 'DOWN'),  # Down
        (-1, 0, 'LEFT'),  # Left
        (1, 0, 'RIGHT')  # Right
    ]

    stack = [(start, [])]  # Stack holds tuples of (position, path)
    visited = set()
    visited.add(start)

    while stack:
        position, path = stack.pop()

        if position == goal:
            return path

        for dx, dy, action in directions:
            new_position = (position[0] + dx, position[1] + dy)

            if is_safe(new_position[0], new_position[1], walls, snake.body) and new_position not in visited:
                visited.add(new_position)
                stack.append((new_position, path + [action]))

    return []  # Return an empty path if no solution is found

