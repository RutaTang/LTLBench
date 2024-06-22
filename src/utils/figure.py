import io

import networkx as nx
from matplotlib import pyplot as plt
from networkx import Graph


def save_graph_to_string(G: Graph) -> str:
    """
    Save graph to string

    """
    graphml = nx.generate_graphml(G)
    return '\n'.join(graphml)
