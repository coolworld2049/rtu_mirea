import random
import copy
from abc import ABC, abstractmethod
import numpy as np


class City:
    def __init__(self, index, x, y):
        self.index = index
        self.x = x
        self.y = y


class MutationStrategy(ABC):
    @abstractmethod
    def mutate(self, route):
        pass


class CrossoverStrategy(ABC):
    @abstractmethod
    def crossover(self, parent1, parent2):
        pass


class ExchangeMutation(MutationStrategy):
    def mutate(self, route):
        new_route = route.copy()
        index1, index2 = random.sample(range(len(route)), 2)
        new_route[index1], new_route[index2] = new_route[index2], new_route[index1]
        return new_route


class PartiallyMappedCrossover(CrossoverStrategy):
    def crossover(self, parent1, parent2):
        point1, point2 = sorted(random.sample(range(len(parent1)), 2))

        offspring = [None] * len(parent1)
        offspring[point1:point2] = parent1[point1:point2]

        for i in range(len(parent2)):
            if point1 <= i < point2:
                continue

            gene = parent2[i]

            while gene in offspring[point1:point2]:
                index = parent2.index(gene)
                gene = parent2[index]

            offspring[i] = gene

        return offspring


class GeneticAlgorithm:
    def __init__(
        self,
        population_size,
        generations,
        mutation_rate,
        mutation_strategy,
        crossover_strategy,
    ):
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.mutation_strategy = mutation_strategy
        self.crossover_strategy = crossover_strategy

    def run_genetic_algorithm(self):
        population = [
            City(i, np.random.randint(1, 10), np.random.uniform(-1, 1))
            for i in range(population_size)
        ]
        for _ in range(self.generations):
            population = sorted(population, key=lambda x: x[1])

            new_population = []
            for _ in range(self.population_size // 2):
                parent1 = self.tournament_selection(population)
                parent2 = self.tournament_selection(population)
                child1 = self.crossover_strategy.crossover(parent1[0], parent2[0])
                child2 = self.crossover_strategy.crossover(parent2[0], parent1[0])
                new_population.extend([(child1, 0), (child2, 0)])

            for i in range(self.population_size):
                if random.random() < self.mutation_rate:
                    new_population[i] = (
                        self.mutation_strategy.mutate(new_population[i][0]),
                        0,
                    )

            population = [
                (route, self.calculate_total_distance(route))
                for route, _ in new_population
            ]

        return min(population, key=lambda x: x[1])[0]

    def generate_random_route(self):
        route = copy.deepcopy(self.city_list)
        random.shuffle(route)
        return route

    def calculate_total_distance(self, route):
        total_distance = 0
        for i in range(len(route) - 1):
            total_distance += self.calculate_distance(route[i], route[i + 1])
        total_distance += self.calculate_distance(route[-1], route[0])
        return total_distance

    @staticmethod
    def calculate_distance(city1, city2):
        return ((city1.x - city2.x) ** 2 + (city1.y - city2.y) ** 2) ** 0.5

    @staticmethod
    def tournament_selection(population, k=3):
        tournament = random.sample(population, k)
        return min(tournament, key=lambda x: x[1])


if __name__ == "__main__":
    population_size = 10
    generations = 100
    mutation_rate = 0.2

    mutation_strategy = ExchangeMutation()
    crossover_strategy = PartiallyMappedCrossover()

    genetic_algorithm = GeneticAlgorithm(
        population_size,
        generations,
        mutation_rate,
        mutation_strategy,
        crossover_strategy,
    )

    best_route = genetic_algorithm.run_genetic_algorithm()

    print("Best Route:", [city.index for city in best_route])
    print("Total Distance:", genetic_algorithm.calculate_total_distance(best_route))
