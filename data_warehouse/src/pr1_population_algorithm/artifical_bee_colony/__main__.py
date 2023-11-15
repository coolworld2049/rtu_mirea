import random
import matplotlib.pyplot as plt
from loguru import logger


# Objective function to be optimized
def objective_function(x):
    return sum([val**2 for val in x])


# Class representing a bee
class Bee:
    def __init__(self, num_dimensions):
        self.position = [random.uniform(-5, 5) for _ in range(num_dimensions)]
        self.fitness = objective_function(self.position)

    def update(self, new_position, new_fitness):
        self.position = new_position
        self.fitness = new_fitness


# Artificial Bee Colony algorithm
def artificial_bee_colony(num_employed, num_onlookers, max_iterations):
    num_dimensions = 2
    employed_bees = [Bee(num_dimensions) for _ in range(num_employed)]
    best_solution = min(employed_bees, key=lambda bee: bee.fitness)

    # Lists for storing fitness values for visualization
    fitness_values = []
    best_fitness_values = []

    for iteration in range(max_iterations):
        # Employed bees phase
        for bee in employed_bees:
            neighbor_bee = random.choice(employed_bees)
            while neighbor_bee is bee:
                neighbor_bee = random.choice(employed_bees)

            new_position = [
                bee.position[i]
                + random.uniform(-1, 1) * (bee.position[i] - neighbor_bee.position[i])
                for i in range(num_dimensions)
            ]
            new_fitness = objective_function(new_position)

            if new_fitness < bee.fitness:
                bee.update(new_position, new_fitness)

        # Calculate the probabilities for onlooker bees
        total_fitness = sum(bee.fitness for bee in employed_bees)
        probabilities = [bee.fitness / total_fitness for bee in employed_bees]

        # Onlooker bees phase
        for i in range(num_onlookers):
            selected_bee = random.choices(employed_bees, probabilities)[0]

            neighbor_bee = random.choice(employed_bees)
            while neighbor_bee is selected_bee:
                neighbor_bee = random.choice(employed_bees)

            new_position = [
                selected_bee.position[i]
                + random.uniform(-1, 1)
                * (selected_bee.position[i] - neighbor_bee.position[i])
                for i in range(num_dimensions)
            ]
            new_fitness = objective_function(new_position)

            if new_fitness < selected_bee.fitness:
                selected_bee.update(new_position, new_fitness)

        # Scout bees phase
        for bee in employed_bees:
            if bee.fitness > best_solution.fitness:
                best_solution = bee

        fitness_values.append(best_solution.fitness)
        best_fitness_values.append(best_solution.fitness)

        logger.info(f"Iteration {iteration}: Best Fitness = {best_solution.fitness}")

    return best_solution, fitness_values, best_fitness_values


if __name__ == "__main__":
    num_employed = 20
    num_onlookers = 10
    max_iterations = 100

    best_solution, fitness_values, best_fitness_values = artificial_bee_colony(
        num_employed, num_onlookers, max_iterations
    )
    logger.info(
        f"Best solution found at position {best_solution.position} with fitness {best_solution.fitness}"
    )

    # Extracting data for visualization
    iterations = list(range(max_iterations))

    # Plot fitness values over iterations
    plt.figure(figsize=(10, 6))
    plt.plot(iterations, fitness_values, label="Fitness of Employed Bees")
    plt.plot(iterations, best_fitness_values, linestyle="--", label="Best Fitness")
    plt.xlabel("Iteration")
    plt.ylabel("Fitness")
    plt.legend()
    plt.title("ABC Algorithm - Fitness Progression")
    plt.grid(True)

    # Show the plot
    plt.show()
