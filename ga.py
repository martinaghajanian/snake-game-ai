import random
from settings import GRID_WIDTH, GRID_HEIGHT
from game import Snake, Fruit, Wall
from utils import *

def genetic_algorithm(snake, fruit, walls, population_size=50, generations=100, mutation_rate=0.1):
    directions = ['UP', 'DOWN', 'LEFT', 'RIGHT']

    def generate_individual():
        return [random.choice(directions) for _ in range(GRID_WIDTH * GRID_HEIGHT)]

    def fitness(individual):
        snake_copy = Snake()
        snake_copy.body = list(snake.body)

        for action in individual:
            take_action(action, snake_copy)
            if snake_copy.body[0] == fruit.position:
                return 0  # Optimal solution found
            if snake_copy.check_collision() or snake_copy.check_wall_collision(walls):
                return float('inf')  # Collision penalty

        head = snake_copy.body[0]
        return abs(head[0] - fruit.position[0]) + abs(head[1] - fruit.position[1])  # Manhattan distance to fruit

    def mutate(individual):
        for i in range(len(individual)):
            if random.random() < mutation_rate:
                individual[i] = random.choice(directions)

    def crossover(parent1, parent2):
        point = random.randint(0, len(parent1) - 1)
        return parent1[:point] + parent2[point:]

    population = [generate_individual() for _ in range(population_size)]

    for _ in range(generations):
        population = sorted(population, key=fitness)
        if fitness(population[0]) == 0:
            return population[0]

        next_generation = population[:population_size // 2]

        while len(next_generation) < population_size:
            parent1, parent2 = random.sample(population[:population_size // 2], 2)
            child = crossover(parent1, parent2)
            mutate(child)
            next_generation.append(child)

        population = next_generation

    return min(population, key=fitness)  # Return the best individual after all generations
