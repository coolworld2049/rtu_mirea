from typing import Callable

import numpy as np

np.random.seed(42)


class Bee:
    def __init__(self, fitness_function: Callable, position):
        self.position = np.array(position)  # xi
        self.fitness_function = fitness_function
        self.fitness = self.fitness_function(self.position)

    def perturb(self, lower_bound, upper_bound):
        # Внесение возмущения в позицию пчелы для создания новой позиции (vi)
        perturbation = np.random.uniform(-1, 1, len(self.position))
        self.position += perturbation
        self.position = np.clip(self.position, lower_bound, upper_bound)


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
    ):
        self.fitness_function = fitness_function
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.population_size = population_size
        self.vector_dim = vector_dim
        self.iterations = iterations
        self.onlooker_ratio = onlooker_ratio
        self.population = [
            Bee(self.fitness_function, np.random.uniform(-5.12, 5.12, vector_dim))
            for _ in range(population_size)
        ]
        self.best_solution = min(self.population, key=lambda bee: bee.fitness)

    def run(self, verbose=0):
        for i in range(self.iterations):
            self.explore()
            self.onlook()
            self.scout()
            self.best_solution = min(
                self.population + [self.best_solution],
                key=lambda bee: bee.fitness,
            )
            if verbose == 1:
                print(
                    f"Iteration: {i}\n"
                    f"best_solution.position: {self.best_solution.position}\t"
                    f"best_solution.fitness: {self.best_solution.fitness}\n"
                )
        return self.best_solution.position, self.best_solution.fitness

    def explore(self):
        for bee in self.population:
            original_position = bee.position.copy()
            bee.perturb(self.lower_bound, self.upper_bound)
            new_fitness = bee.fitness_function(bee.position)
            if new_fitness < bee.fitness:
                bee.fitness = new_fitness
            else:
                bee.position = original_position

    def onlook(self):
        def calc_select_onlooker_probs():
            total_fitness = sum(1 / bee.fitness for bee in self.population)
            probabilities = [
                (1 / bee.fitness) / total_fitness for bee in self.population
            ]
            return probabilities

        # Наблюдение за пчелами среди пчел-наблюдателей
        onlooker_count = int(self.onlooker_ratio * self.population_size)

        for _ in range(onlooker_count):
            # Расчет вероятности выбора пчелы-наблюдателя
            selected_bee_index = np.random.choice(
                range(self.population_size),
                p=calc_select_onlooker_probs(),
            )
            selected_bee = self.population[selected_bee_index]
            original_position = selected_bee.position.copy()

            selected_bee.perturb(self.lower_bound, self.upper_bound)
            new_fitness = selected_bee.fitness_function(selected_bee.position)

            if new_fitness < selected_bee.fitness:
                selected_bee.fitness = new_fitness
            else:
                selected_bee.position = original_position

    def scout(self):
        for bee in self.population:
            if bee.fitness > self.best_solution.fitness:
                bee.position = np.random.uniform(-5.12, 5.12, self.vector_dim)
                bee.fitness = bee.fitness_function(bee.position)


def rastring_function(position):
    A = 10
    fitness = A * len(position) + np.sum(
        position**2 - A * np.cos(2 * np.pi * position)
    )
    return fitness


abc = ArtificialBeeColony(
    fitness_function=rastring_function,
    lower_bound=-5.12,
    upper_bound=5.12,
    population_size=100,
    vector_dim=1,
    iterations=10,
    onlooker_ratio=0.6,
)
best_position, best_fitness = abc.run(verbose=1)
print("Best Position:", best_position)
print("Best Fitness:", best_fitness)
