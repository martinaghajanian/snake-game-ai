import random
from settings import GRID_WIDTH, GRID_HEIGHT
from game import Snake, Fruit, Wall

def genetic_algorithm1(snake, fruit, walls, population_size=50, generations=100, mutation_rate=0.1):
    directions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
    direction_map = {
        'UP': (0, -1),
        'DOWN': (0, 1),
        'LEFT': (-1, 0),
        'RIGHT': (1, 0)
    }
    max_steps = 5000

    def manhattan_distance(point1, point2):
        return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

    def generate_individual():
        return [random.choice(directions) for _ in range(GRID_WIDTH * GRID_HEIGHT)]

    def take_action(action, snake_obj):
        if action in direction_map:
            snake_obj.set_direction(direction_map[action])
        snake_obj.move()

    def fitness1(individual):
        snake_copy = Snake()
        snake_copy.body = list(snake.body)
        snake_copy.direction = snake.direction
        fruit_copy = Fruit()
        fruit_copy.position = fruit.position
        walls_copy = Wall()
        walls_copy.positions = list(walls.positions)

        steps = 0
        score = 0
        steps_without_food = 0

        for step, action in enumerate(individual[:max_steps]):
            take_action(action, snake_copy)

            if snake_copy.check_collision() or snake_copy.check_wall_collision(walls_copy):
                break  # Stop when the snake dies

            steps += 1
            steps_without_food += 1

            if snake_copy.body[0] == fruit_copy.position:
                score += 1  # Increase score for eating food
                snake_copy.grow()
                fruit_copy.new_position(snake_copy.body, walls_copy.positions)
                steps_without_food = 0

            if steps_without_food >= 200:
                break  # Stop if the snake takes too long without eating

        # Apply the new fitness formula
        return steps * steps * (2 ** score)


    def mutate(individual):
        for i in range(len(individual)):
            if random.random() < mutation_rate:
                individual[i] = random.choice(directions)

    def crossover(parent1, parent2):
        crossover_point = random.randint(0, len(parent1) - 1)
        return parent1[:crossover_point] + parent2[crossover_point:]

    population = [generate_individual() for _ in range(population_size)]

    for generation in range(generations):
        fitness_scores = [(fitness1(ind), ind) for ind in population]
        fitness_scores.sort(key=lambda x: x[0], reverse=True)

        top_individuals = [ind for _, ind in fitness_scores[:10]]

        next_generation = top_individuals[:]

        while len(next_generation) < population_size:
            parent1, parent2 = random.sample(top_individuals, 2)
            child = crossover(parent1, parent2)
            mutate(child)
            next_generation.append(child)

        population = next_generation

    best_fitness, best_individual = max((fitness1(ind), ind) for ind in population)
    return best_individual


def genetic_algorithm2(snake, fruit, walls, population_size=50, generations=100, mutation_rate=0.1):
    directions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
    direction_map = {
        'UP': (0, -1),
        'DOWN': (0, 1),
        'LEFT': (-1, 0),
        'RIGHT': (1, 0)
    }
    max_steps = 5000

    def manhattan_distance(point1, point2):
        return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

    def generate_individual():
        return [random.choice(directions) for _ in range(GRID_WIDTH * GRID_HEIGHT)]

    def take_action(action, snake_obj):
        if action in direction_map:
            snake_obj.set_direction(direction_map[action])
        snake_obj.move()


    def fitness2(individual):
        snake_copy = Snake()
        snake_copy.body = list(snake.body)
        snake_copy.direction = snake.direction
        fruit_copy = Fruit()
        fruit_copy.position = fruit.position
        walls_copy = Wall()
        walls_copy.positions = list(walls.positions)

        score = 0
        steps_without_food = 0

        for step, action in enumerate(individual[:max_steps]):
            take_action(action, snake_copy)

            if snake_copy.check_collision() or snake_copy.check_wall_collision(walls_copy):
                score -= 100  # Penalty for dying
                break

            steps_without_food += 1

            if snake_copy.body[0] == fruit_copy.position:
                score += 1000  # Reward for eating food
                snake_copy.grow()
                fruit_copy.new_position(snake_copy.body, walls_copy.positions)
                steps_without_food = 0

            if steps_without_food >= 200:
                score -= 50  # Penalty for taking too long
                break

        score -= manhattan_distance(snake_copy.body[0], fruit_copy.position) * 10  # Closer is better
        return score

    def mutate(individual):
        for i in range(len(individual)):
            if random.random() < mutation_rate:
                individual[i] = random.choice(directions)

    def crossover(parent1, parent2):
        crossover_point = random.randint(0, len(parent1) - 1)
        return parent1[:crossover_point] + parent2[crossover_point:]

    population = [generate_individual() for _ in range(population_size)]

    for generation in range(generations):
        fitness_scores = [(fitness2(ind), ind) for ind in population]
        fitness_scores.sort(key=lambda x: x[0], reverse=True)

        top_individuals = [ind for _, ind in fitness_scores[:10]]

        next_generation = top_individuals[:]

        while len(next_generation) < population_size:
            parent1, parent2 = random.sample(top_individuals, 2)
            child = crossover(parent1, parent2)
            mutate(child)
            next_generation.append(child)

        population = next_generation

    best_fitness, best_individual = max((fitness2(ind), ind) for ind in population)
    return best_individual


def genetic_algorithm_improved(snake, fruit, walls, population_size=50, generations=100, mutation_rate=0.1):
    directions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
    direction_map = {
        'UP': (0, -1),
        'DOWN': (0, 1),
        'LEFT': (-1, 0),
        'RIGHT': (1, 0)
    }
    max_steps = 1000

    def manhattan_distance(point1, point2):
        return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

    def generate_individual():
        return [random.choice(directions) for _ in range(20)]  # Smaller, dynamic decision blocks

    def take_action(action, snake_obj):
        if action in direction_map:
            snake_obj.set_direction(direction_map[action])
        snake_obj.move()

    def fitness(individual):
        snake_copy = Snake()
        snake_copy.body = list(snake.body)
        snake_copy.direction = snake.direction
        fruit_copy = Fruit()
        fruit_copy.position = fruit.position
        walls_copy = Wall()
        walls_copy.positions = list(walls.positions)

        score = 0
        steps_without_food = 0

        for action in individual:
            take_action(action, snake_copy)

            if snake_copy.check_collision() or snake_copy.check_wall_collision(walls_copy):
                score -= 100  # Heavy penalty for dying
                break

            steps_without_food += 1

            if snake_copy.body[0] == fruit_copy.position:
                score += 1000  # Reward for eating food
                snake_copy.grow()
                fruit_copy.new_position(snake_copy.body, walls_copy.positions)
                steps_without_food = 0

            if steps_without_food >= 100:
                score -= 100  # Penalty for wasting time
                break

            score += max(0, 200 - manhattan_distance(snake_copy.body[0], fruit_copy.position))  # Closer is better

        return score

    def mutate(individual):
        mutation_points = random.sample(range(len(individual)), max(1, int(len(individual) * mutation_rate)))
        for point in mutation_points:
            individual[point] = random.choice(directions)

    def crossover(parent1, parent2):
        crossover_point = random.randint(1, len(parent1) - 2)
        return parent1[:crossover_point] + parent2[crossover_point:]

    # Initialize population
    population = [generate_individual() for _ in range(population_size)]

    for generation in range(generations):
        fitness_scores = [(fitness(ind), ind) for ind in population]
        fitness_scores.sort(key=lambda x: x[0], reverse=True)

        # Elitism: Keep the top-performing individuals
        top_individuals = [ind for _, ind in fitness_scores[:5]]
        next_generation = top_individuals[:]

        while len(next_generation) < population_size:
            parent1, parent2 = random.sample(top_individuals, 2)
            child = crossover(parent1, parent2)
            mutate(child)
            next_generation.append(child)

        population = next_generation

        # Log progress
        best_fitness = fitness_scores[0][0]
        #print(f"Generation {generation + 1} - Best Fitness: {best_fitness}")

    best_fitness, best_individual = max((fitness(ind), ind) for ind in population)
    return best_individual
