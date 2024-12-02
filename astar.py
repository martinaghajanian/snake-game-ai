from heapq import heappush, heappop
from utils import *

def astar(snake, fruit, walls):
    """
    A* Search Algorithm to find the shortest path to the fruit.

    :param snake: The Snake object
    :param fruit: The Fruit object
    :param walls: The Wall object
    :return: A list of actions (UP, DOWN, LEFT, RIGHT) representing the path to the fruit
    """
    start = snake.body[0]  # Snake head position
    goal = fruit.position

    directions = [
        (0, -1, 'UP'),  # Up
        (0, 1, 'DOWN'),  # Down
        (-1, 0, 'LEFT'),  # Left
        (1, 0, 'RIGHT')  # Right
    ]

    def heuristic(pos):
        return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])  # Manhattan distance

    priority_queue = []
    heappush(priority_queue, (0 + heuristic(start), 0, start, []))
    visited = set()
    visited.add(start)

    while priority_queue:
        _, cost, position, path = heappop(priority_queue)

        if position == goal:
            return path

        for dx, dy, action in directions:
            new_position = (position[0] + dx, position[1] + dy)

            if is_safe(new_position[0], new_position[1], walls, snake.body) and new_position not in visited:
                visited.add(new_position)
                new_cost = cost + 1
                heappush(priority_queue, (new_cost + heuristic(new_position), new_cost, new_position, path + [action]))

    return []  # Return an empty path if no solution is found
