import random
from game import Snake, Fruit, Wall
import pickle
from utils import *

# Q-learning parameters
ALPHA = 0.05  # Learning rate
GAMMA = 0.99  # Discount factor
EPSILON = 1.0  # Initial exploration rate
EPSILON_DECAY = 0.999995
MIN_EPSILON = 0.1
NUM_EPISODES = 10000000


def get_state(snake, fruit, walls):
    head = snake.body[0]
    dx, dy = fruit.position[0] - head[0], fruit.position[1] - head[1]

    # Check if the surrounding cells are safe (1 = safe, 0 = not safe)
    surroundings = [
        is_safe(head[0], head[1] - 1, walls, snake.body),  # Up
        is_safe(head[0], head[1] + 1, walls, snake.body),  # Down
        is_safe(head[0] - 1, head[1], walls, snake.body),  # Left
        is_safe(head[0] + 1, head[1], walls, snake.body),  # Right
    ]

    # Return the state as a tuple
    return (dx, dy, *surroundings)


def train_qlearning():
    Q = {}  # Initialize Q-table as a dictionary
    epsilon = EPSILON

    for episode in range(1, NUM_EPISODES + 1):
        # Initialize the environment
        snake = Snake()
        fruit = Fruit()
        walls = Wall()

        fruit.new_position(snake.body, walls.positions)
        state = get_state(snake, fruit, walls)
        total_reward = 0

        while True:
            # Choose an action (epsilon-greedy policy)
            if random.random() < epsilon:
                action = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])  # Exploration
            else:
                if state not in Q:
                    Q[state] = {a: 0 for a in ['UP', 'DOWN', 'LEFT', 'RIGHT']}
                action = max(Q[state], key=Q[state].get)  # Exploitation

            # Perform action and get new state and reward
            take_action(action, snake)
            reward = calculate_reward(snake, fruit, walls)
            new_state = get_state(snake, fruit, walls)
            total_reward += reward

            # Update Q-value
            if state not in Q:
                Q[state] = {a: 0 for a in ['UP', 'DOWN', 'LEFT', 'RIGHT']}
            if new_state not in Q:
                Q[new_state] = {a: 0 for a in ['UP', 'DOWN', 'LEFT', 'RIGHT']}
            best_future_q = max(Q[new_state].values())
            Q[state][action] += ALPHA * (reward + GAMMA * best_future_q - Q[state][action])

            # Transition to new state
            state = new_state

            # Check if the game is over
            if reward == REWARD_COLLISION:
                break
            elif snake.body[0] == fruit.position:
                snake.grow()
                fruit.new_position(snake.body, walls.positions)

        # Decay epsilon
        epsilon = max(MIN_EPSILON, epsilon * EPSILON_DECAY)

        # Save the Q-table periodically
        if episode % 100_000 == 0:
            save_q_table(Q, f"q_table_{episode}.pkl")
            print(f"Episode {episode}/{NUM_EPISODES}, Total Reward: {total_reward}. Q-table saved.")

    return Q


def save_q_table(Q, filename="q_table_4000000_notgood.pkl"):
    with open(filename, "wb") as file:
        pickle.dump(Q, file)


def load_q_table(filename="q_table_4000000_notgood.pkl"):
    try:
        with open(filename, "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        return {}


if __name__ == "__main__":
    Q_table = train_qlearning()
