import random

import matplotlib.pyplot as plt
import networkx as nx
from loguru import logger
from networkx import Graph

random.seed(42)


class DistanceCalculator:
    @staticmethod
    def calculate_distance(graph, route):
        """
        Для каждого маршрута из популяции вычисляется его приспособленность,
        которая определяется суммой расстояний между городами
        """
        return (
            sum(
                graph.edges[route[i], route[i + 1]]["weight"]
                for i in range(len(route) - 1)
            )
            + graph.edges[route[-1], route[0]][
                "weight"
            ]  # расстояние от последнего города до начального города
        )


class RouteInitializer:
    @staticmethod
    def init_route(graph: Graph):
        """
        Создание популяции маршрутов, представляющих собой случайные перестановки городов
        """
        route = list(graph.nodes)
        random.shuffle(route)
        return route


class NaturalSelector:
    def __init__(self, tournament_size, distance_calculator):
        self.tournament_size = tournament_size
        self.distance_calculator = distance_calculator

    def select_parents(self, population, graph):
        """
        Выбирает родителей для генетического алгоритма с использованием естественного отбора
        """
        tournament = random.sample(population, self.tournament_size)
        return min(
            tournament,
            key=lambda route: self.distance_calculator.calculate_distance(graph, route),
        )


class CrossoverOperator:
    @staticmethod
    def crossover(X, Y):
        """
        Cоздаются два потомка, комбинируя части родительских маршрутов для создания потомства
        """
        start, end = sorted(random.sample(range(len(X)), 2))
        temp = X[start:end] + [city for city in Y if city not in X[start:end]]
        return temp[start:] + temp[:start]


class MutationOperator:
    @staticmethod
    def mutate(individual):
        """
        Обмен местами двух городов в маршруте.
        """
        idx1, idx2 = random.sample(range(len(individual)), 2)
        individual[idx1], individual[idx2] = individual[idx2], individual[idx1]
        return individual


class GeneticAlgorithm:
    def __init__(
        self,
        population_initializer,
        parent_selector,
        crossover_operator,
        mutation_operator,
        distance_calculator,
    ):
        self.population_initializer = population_initializer
        self.parent_selector = parent_selector
        self.crossover_operator = crossover_operator
        self.mutation_operator = mutation_operator
        self.distance_calculator = distance_calculator

    def run(self, pop_size, generations, crossover_prob, mutation_prob, graph):
        population = [
            self.population_initializer.init_route(graph) for _ in range(pop_size)
        ]

        for _ in range(generations):
            new_population = []

            for _ in range(pop_size // 2):
                # Выбор двух родителей
                X = self.parent_selector.select_parents(population, graph)
                Y = self.parent_selector.select_parents(population, graph)

                # Кроссовер
                XY = (
                    self.crossover_operator.crossover(X, Y)
                    if random.random() < crossover_prob
                    else X[:]
                )
                YX = (
                    self.crossover_operator.crossover(Y, X)
                    if random.random() < crossover_prob
                    else Y[:]
                )

                # Мутация
                new_population.extend(
                    [
                        self.mutation_operator.mutate(child)
                        if random.random() < mutation_prob
                        else child[:]
                        for child in [XY, YX]
                    ]
                )

            population = new_population

        best_route = min(
            population,
            key=lambda route: self.distance_calculator.calculate_distance(graph, route),
        )
        return best_route


def visualize_shortest_path(graph, best_route):
    pos = nx.spring_layout(graph, k=10, seed=42)
    plt.figure(1, (12, 12), dpi=200)

    nx.draw(
        graph,
        pos,
        with_labels=True,
        edge_color="gray",
        width=0.5,
    )

    best_route_edges = [
        (best_route[i], best_route[i + 1]) for i in range(len(best_route) - 1)
    ]
    best_route_edges.append((best_route[-1], best_route[0]))

    edge_labels = {
        (edge[0], edge[1]): graph.edges[edge]["weight"] for edge in graph.edges
    }
    nx.draw_networkx_edges(
        graph,
        pos=pos,
        edgelist=best_route_edges,
        edge_color="r",
        width=1,
        connectionstyle="arc3,rad=0.4",
        arrowsize=15,
        arrows=True,
        arrowstyle="-|>",
    )
    nx.draw_networkx_edge_labels(graph, pos=pos, edge_labels=edge_labels)

    plt.title("Best Route Visualization")
    plt.savefig("graph.jpg")


if __name__ == "__main__":
    cities_count = 6
    G = nx.complete_graph(cities_count)
    for edge in G.edges():
        G.edges[edge]["weight"] = random.randint(1, cities_count)

    distance_calculator = DistanceCalculator()
    parent_selector = NaturalSelector(
        tournament_size=3,
        distance_calculator=distance_calculator,
    )

    genetic_algorithm = GeneticAlgorithm(
        population_initializer=RouteInitializer(),
        parent_selector=parent_selector,
        crossover_operator=CrossoverOperator(),
        mutation_operator=MutationOperator(),
        distance_calculator=distance_calculator,
    )

    best_route = genetic_algorithm.run(
        pop_size=100,
        generations=1000,
        crossover_prob=0.7,
        mutation_prob=0.2,
        graph=G,
    )

    logger.info(f"Best Route: {best_route}")
    logger.info(
        f"Total Distance: {distance_calculator.calculate_distance(G, best_route)}"
    )

    visualize_shortest_path(G, best_route)
