from settings import GRID_WIDTH, GRID_HEIGHT, FPS

# Reward values
REWARD_FRUIT = 100
REWARD_COLLISION = -1000
REWARD_STEP = -1

def is_safe(x, y, walls, snake_body):
    return 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT and (x, y) not in walls.positions and (x, y) not in snake_body

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