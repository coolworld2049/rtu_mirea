import numpy as np
import matplotlib.pyplot as plt
from benchmark_functions import benchmark_functions

np.random.seed(42)


class Bee:
    def __init__(self, fitness_function, position):
        self.position = np.array(position)
        self.fitness_function = fitness_function
        self.fitness = self.fitness_function(self.position)

    def perturb(self, lower_bound, upper_bound, use_gaussian=True):
        if use_gaussian:
            perturbation = np.random.normal(0, 1, len(self.position))
        else:
            perturbation = np.random.uniform(-1, 1, len(self.position))
        self.position += perturbation
        self.position = np.clip(self.position, lower_bound, upper_bound)

    def local_search(self, neighborhood_size, lower_bound, upper_bound):
        original_position = self.position.copy()
        for _ in range(neighborhood_size):
            self.perturb(lower_bound, upper_bound, use_gaussian=True)
            new_fitness = self.fitness_function(self.position)
            if new_fitness < self.fitness:
                self.fitness = new_fitness
            else:
                self.position = original_position


class ArtificialBeeColony:
    def __init__(
        self,
        fitness_function,
        lower_bound,
        upper_bound,
        population_size,
        vector_dim,
        iterations,
        onlooker_ratio,
        local_search_neighbors=5,
        acceptance_probability=0.1,
    ):
        self.fitness_function = fitness_function
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.population_size = population_size
        self.vector_dim = vector_dim
        self.iterations = iterations
        self.onlooker_ratio = onlooker_ratio
        self.local_search_neighbors = local_search_neighbors
        self.acceptance_probability = acceptance_probability
        self.population = [
            Bee(
                self.fitness_function,
                np.random.uniform(lower_bound, upper_bound, vector_dim),
            )
            for _ in range(population_size)
        ]
        self.best_solution = min(self.population, key=lambda bee: bee.fitness)
        self.best_fitness_history = []

    def run(self, verbose=0):
        for i in range(self.iterations):
            self.explore()
            self.onlook()
            self.scout()
            self.best_solution = min(
                self.population + [self.best_solution],
                key=lambda bee: bee.fitness,
            )
            self.best_fitness_history.append(self.best_solution.fitness)
            if verbose == 1:
                print(
                    f"Iteration: {i}\n"
                    f"best_solution.position: {self.best_solution.position}\t"
                    f"best_solution.fitness: {self.best_solution.fitness}\n"
                )
        return (
            self.best_solution.position,
            self.best_solution.fitness,
            self.best_fitness_history,
        )

    def explore(self):
        for bee in self.population:
            original_position = bee.position.copy()
            bee.perturb(self.lower_bound, self.upper_bound, use_gaussian=True)
            new_fitness = bee.fitness_function(bee.position)
            if new_fitness < bee.fitness:
                bee.fitness = new_fitness
                bee.local_search(
                    self.local_search_neighbors, self.lower_bound, self.upper_bound
                )
            else:
                bee.position = original_position

    def onlook(self):
        def calc_select_onlooker_probs():
            total_fitness = sum(1 / bee.fitness for bee in self.population)
            probabilities = [
                (1 / bee.fitness) / total_fitness for bee in self.population
            ]
            return probabilities

        onlooker_count = int(self.onlooker_ratio * self.population_size)

        for _ in range(onlooker_count):
            selected_bee_index = np.random.choice(
                range(self.population_size),
                p=calc_select_onlooker_probs(),
            )
            selected_bee = self.population[selected_bee_index]
            original_position = selected_bee.position.copy()

            selected_bee.perturb(self.lower_bound, self.upper_bound, use_gaussian=True)
            new_fitness = selected_bee.fitness_function(selected_bee.position)

            # Симуляция отжига
            if (
                new_fitness < selected_bee.fitness
                or np.random.rand() < self.acceptance_probability
            ):
                selected_bee.fitness = new_fitness
                selected_bee.local_search(
                    self.local_search_neighbors, self.lower_bound, self.upper_bound
                )
            else:
                selected_bee.position = original_position

    def scout(self):
        for bee in self.population:
            if bee.fitness > self.best_solution.fitness:
                bee.position = np.random.uniform(
                    self.lower_bound, self.upper_bound, self.vector_dim
                )
                bee.fitness = bee.fitness_function(bee.position)


n_dimensions = 1
fitness_function = benchmark_functions.Rastrigin(n_dimensions=n_dimensions)
lower_bound, upper_bound = fitness_function.suggested_bounds()

abc = ArtificialBeeColony(
    fitness_function=fitness_function,
    lower_bound=lower_bound,
    upper_bound=upper_bound,
    population_size=100,
    vector_dim=n_dimensions,
    iterations=200,
    onlooker_ratio=0.6,
    acceptance_probability=0.01,
)
best_position, best_fitness, best_fitness_history = abc.run(verbose=1)

print("Best Position:", best_position)
print("Best Fitness:", best_fitness)

plt.plot(best_fitness_history)
plt.xlabel("Iteration")
plt.ylabel("Best Fitness")
plt.title("Best Fitness History")
plt.show()
