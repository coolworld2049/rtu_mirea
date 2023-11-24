import random
import numpy as np
from loguru import logger

random.seed(42)


def calculate_distance(adj_matrix, route):
    distance = 0
    for i in range(len(route) - 1):
        distance += adj_matrix[route[i], route[i + 1]]
    distance += adj_matrix[route[-1], route[0]]
    return distance


class NaturalSelector:
    def __init__(self, tournament_size):
        self.tournament_size = tournament_size

    def select_parents(self, population):
        tournament = random.sample(population, self.tournament_size)
        return min(
            tournament,
            key=lambda item: item[1],  # Compare routes based on their weights
        )


class CrossoverOperator:
    @staticmethod
    def crossover(X, Y):
        start, end = sorted(random.sample(range(len(X[0])), 2))
        child_route = np.zeros_like(X[0])
        child_route[start:end] = X[0, start:end]
        missing_cities = [city for city in Y[0] if city not in child_route]
        child_route[end:] = missing_cities + X[0, :start] + X[0, end:]
        child_weight = (X[1] + Y[1]) / 2  # Take the average of the weights
        return np.array([child_route, child_weight])


class MutationOperator:
    @staticmethod
    def mutate(individual):
        route, weight = individual
        idx1, idx2 = random.sample(range(len(route)), 2)
        route[idx1], route[idx2] = route[idx2], route[idx1]
        return np.array([route, weight])


class GeneticAlgorithm:
    def __init__(
        self,
        selector,
        crossover_operator,
        mutation_operator,
    ):
        self.selector = selector
        self.crossover_operator = crossover_operator
        self.mutation_operator = mutation_operator

    def run(self, pop_size, generations, crossover_rate, mutation_rate, adj_matrix):
        population = []

        for _ in range(pop_size):
            route = np.random.permutation(len(adj_matrix))
            weight = (
                np.sum(adj_matrix[route[:-1], route[1:]])
                + adj_matrix[route[-1], route[0]]
            )
            population.append([route, weight])  # Don't convert to NumPy array here

        for g in range(generations):
            new_population = []

            for p in range(pop_size // 2):
                X = self.selector.select_parents(population)
                Y = self.selector.select_parents(population)

                child = (
                    self.crossover_operator.crossover(X, Y)
                    if random.random() < crossover_rate
                    else X
                )

                if random.random() < mutation_rate:
                    new_population.extend([self.mutation_operator.mutate(child)])
                else:
                    new_population.extend([child])

            population = new_population
            best_route = min(
                population,
                key=lambda item: item[1],  # Find the route with the minimum weight
            )
            logger.info(
                f"Generation: {g}. Best route: {best_route[0]}. Weight: {best_route[1]}"
            )

        return population


if __name__ == "__main__":
    cities_count = 10
    adjacency_matrix = np.random.randint(1, 10, size=(cities_count, cities_count))

    natural_selector = NaturalSelector(
        tournament_size=3,
    )

    genetic_algorithm = GeneticAlgorithm(
        selector=natural_selector,
        crossover_operator=CrossoverOperator(),
        mutation_operator=MutationOperator(),
    )

    population = genetic_algorithm.run(
        pop_size=100,
        generations=1000,
        crossover_rate=0.9,
        mutation_rate=0.1,
        adj_matrix=adjacency_matrix,
    )

    best_route = min(
        population,
        key=lambda item: item[1],  # Find the route with the minimum weight
    )
    best_route_nodes = best_route[0]
    best_route_total_distance = best_route[1]

    logger.info(f"Adjacency Matrix:\n{adjacency_matrix}")
    logger.info(f"Best Route: {best_route_nodes}")
    logger.info(f"Total Distance: {best_route_total_distance}")
