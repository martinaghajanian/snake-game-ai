from settings import GRID_WIDTH, GRID_HEIGHT, FPS

# Reward values
REWARD_FRUIT = 50000000
REWARD_COLLISION = -10000
REWARD_STEP = -1

def is_safe(x, y, walls, snake_body):
    # Check if the cell is within grid boundaries and not in walls or the snake's body
    if x < 0 or y < 0 or x >= GRID_WIDTH or y >= GRID_HEIGHT:
        return 0  # Not safe (out of bounds)
    if (x, y) in walls.positions or (x, y) in snake_body:
        return 0  # Not safe (wall or snake body)
    return 1  # Safe

def calculate_reward(snake, fruit, walls):
    if snake.check_wall_collision(walls) or snake.check_collision():
        return REWARD_COLLISION
    elif snake.body[0] == fruit.position:
        return REWARD_FRUIT
    else:
        return REWARD_STEP

def take_action(action, snake):
    if action == 'UP':
        snake.set_direction((0, -1))
    elif action == 'DOWN':
        snake.set_direction((0, 1))
    elif action == 'LEFT':
        snake.set_direction((-1, 0))
    elif action == 'RIGHT':
        snake.set_direction((1, 0))
    snake.move()