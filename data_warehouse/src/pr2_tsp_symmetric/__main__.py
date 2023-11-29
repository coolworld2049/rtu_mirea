import random
import networkx as nx
from loguru import logger
from matplotlib import pyplot as plt

random.seed(42)


class DistanceCalculator:
    def __init__(self, graph):
        self.graph = graph

    def calculate_distance(self, route):
        return (
            sum(
                self.graph.edges_df[route[i], route[i + 1]]["weight"]
                for i in range(len(route) - 1)
            )
            + self.graph.edges_df[route[-1], route[0]]["weight"]
        )


class RouteInitializer:
    def __init__(self, graph):
        self.graph = graph

    def initialize_route(self):
        route = list(self.graph.nodes)
        random.shuffle(route)
        return route


class ParentSelector:
    def __init__(self, tournament_size, distance_calculator):
        self.tournament_size = tournament_size
        self.distance_calculator = distance_calculator

    def select_parents(self, population):
        tournament = random.sample(population, self.tournament_size)
        return min(tournament, key=self.distance_calculator.calculate_distance)


class CrossoverOperator:
    def crossover(self, parent1, parent2):
        size = len(parent1)
        start, end = sorted(random.sample(range(size), 2))
        temp = parent1[start:end] + [
            city for city in parent2 if city not in parent1[start:end]
        ]
        return temp[start:] + temp[:start]


class MutationOperator:
    def mutate(self, individual):
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

    def run(self, pop_size, generations, crossover_prob, mutation_prob):
        population = [
            self.population_initializer.initialize_route() for _ in range(pop_size)
        ]

        for _ in range(generations):
            new_population = []

            for _ in range(pop_size // 2):
                parent1 = self.parent_selector.select_parents(population)
                parent2 = self.parent_selector.select_parents(population)

                child1 = (
                    self.crossover_operator.crossover(parent1, parent2)
                    if random.random() < crossover_prob
                    else parent1[:]
                )
                child2 = (
                    self.crossover_operator.crossover(parent2, parent1)
                    if random.random() < crossover_prob
                    else parent2[:]
                )

                new_population.extend(
                    [
                        self.mutation_operator.mutate(child)
                        if random.random() < mutation_prob
                        else child[:]
                        for child in [child1, child2]
                    ]
                )

            population = new_population

        best_route = min(population, key=self.distance_calculator.calculate_distance)
        return best_route


# Create a random graph representing cities and distances
G = nx.complete_graph(10)
for edge in G.edges_df():
    G.edges_df[edge]["weight"] = random.randint(1, 10)

# Create instances of the classes
distance_calculator = DistanceCalculator(G)
route_initializer = RouteInitializer(G)
parent_selector = ParentSelector(
    tournament_size=3, distance_calculator=distance_calculator
)
crossover_operator = CrossoverOperator()
mutation_operator = MutationOperator()

# Create an instance of the GeneticAlgorithm
genetic_algorithm = GeneticAlgorithm(
    population_initializer=route_initializer,
    parent_selector=parent_selector,
    crossover_operator=crossover_operator,
    mutation_operator=mutation_operator,
    distance_calculator=distance_calculator,
)

# Run the genetic algorithm
best_route = genetic_algorithm.run(
    pop_size=100, generations=1000, crossover_prob=0.7, mutation_prob=0.2
)

logger.info(f"Best Route: {best_route}")
logger.info(f"Total Distance: {distance_calculator.calculate_distance(best_route)}")


def visualize_best_route(graph, best_route):
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True)

    best_route_edges = [
        (best_route[i], best_route[i + 1]) for i in range(len(best_route) - 1)
    ]
    best_route_edges.append(
        (best_route[-1], best_route[0])
    )  # Connect the last and first nodes
    nx.draw_networkx_edges(
        graph, pos, edgelist=best_route_edges, edge_color="r", width=2
    )

    plt.title("Best Route Visualization")
    plt.show()


visualize_best_route(G, best_route)
