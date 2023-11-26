import networkx as nx
from matplotlib import pyplot as plt


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
