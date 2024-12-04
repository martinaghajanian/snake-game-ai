import random
from settings import GRID_WIDTH, GRID_HEIGHT
from game import Snake, Fruit, Wall
from utils import *

def genetic_algorithm(snake, fruit, walls, population_size=50, generations=100, mutation_rate=0.1):
    directions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
    max_steps = 5000

    def manhattan_distance(point1, point2):
        return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

    def generate_individual():
        return [random.choice(directions) for _ in range(GRID_WIDTH * GRID_HEIGHT)]


    def fitness1(individual):
        snake_copy = Snake()
        snake_copy.body = list(snake.body)
        record = 0
        deaths = 0
        total_steps = 0
        penalties = 0
        steps_without_food = 0
        total_food = 0
        
        for step, action in enumerate(individual[:max_steps]):
            take_action(action, snake_copy)

            if snake_copy.check_collision() or snake_copy.check_wall_collision(walls):
                deaths += 1
                break

            total_steps += 1
            steps_without_food += 1

            if snake_copy.body[0] == fruit.position:
                record += 1
                total_food += 1
                steps_without_food = 0
                fruit.new_position(snake_copy.body, walls) 

            if steps_without_food >= 200:
                penalties += 1
                steps_without_food = 0

        avg_steps = total_steps / total_food if total_food > 0 else total_steps
        return record * 5000 - deaths * 150 - avg_steps * 100 - penalties * 1000


    def fitness2(individual):
        snake_copy = Snake()
        snake_copy.body = list(snake.body)
        fruit_copy = Fruit()
        fruit_copy.position = fruit.position

        steps = 0
        score = 0

        for action in individual[:max_steps]:
            take_action(action, snake_copy)

            if snake_copy.check_collision() or snake_copy.check_wall_collision(walls):
                break

            steps += 1

            if snake_copy.body[0] == fruit_copy.position:
                score += 1
                fruit_copy.new_position(snake_copy.body, walls)

        return steps * steps * (2 ** score)

    def fitness3(individual):
        snake_copy = Snake()
        snake_copy.body = list(snake.body)
        fruit_copy = Fruit()
        fruit_copy.position = fruit.position

        steps = 0
        score = 0

        for action in individual[:max_steps]:
            take_action(action, snake_copy)

            if snake_copy.check_collision() or snake_copy.check_wall_collision(walls):
                break

            steps += 1

            if snake_copy.body[0] == fruit_copy.position:
                score += 1
                fruit_copy.new_position(snake_copy.body, walls)

        distance_to_fruit = manhattan_distance(snake_copy.body[0], fruit_copy.position)

        return (steps * 10) + (score * 500) - distance_to_fruit


    def fitness4(individual):
        snake_copy = Snake()
        snake_copy.body = list(snake.body)
        fruit_copy = Fruit()
        fruit_copy.position = fruit.position

        steps = 0
        score = 0

        for action in individual[:max_steps]:
            take_action(action, snake_copy)

            if snake_copy.check_collision() or snake_copy.check_wall_collision(walls):
                break

            steps += 1

            if snake_copy.body[0] == fruit_copy.position:
                score += 1
                fruit_copy.new_position(snake_copy.body, walls)

        distance_to_fruit = manhattan_distance(snake_copy.body[0], fruit_copy.position)

        return -distance_to_fruit



    def mutate(individual):
        for i in range(len(individual)):
            if random.random() < mutation_rate:
                individual[i] = random.choice(directions)

    def crossover(parent1, parent2):
        child = []
        for p1, p2 in zip(parent1, parent2):
            child.append(p1 if random.random() < 0.5 else p2)
        return child

    population = [generate_individual() for _ in range(population_size)]

    for _ in range(generations):

        fitness_scores = [(fitness1(individual), individual) for individual in population]
        fitness_scores.sort(key=lambda x: x[0], reverse=True)


        top_individuals = [ind for _, ind in fitness_scores[:12]]


        next_generation = top_individuals[:]

        while len(next_generation) < population_size:
            parent1, parent2 = random.sample(top_individuals, 2)
            child = crossover(parent1, parent2)
            mutate(child)
            next_generation.append(child)

        population = next_generation


    best_fitness, best_individual = max((fitness1(ind), ind) for ind in population)
    return best_individual
