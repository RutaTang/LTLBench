import io

import networkx as nx
from matplotlib import pyplot as plt
from networkx import DiGraph


def save_graph_to_string(graph: DiGraph) -> str:
    """
    Save graph to string

    :param graph: graph
    :return: graphml string
    """
    graphml = nx.generate_graphml(graph)
    return '\n'.join(graphml)
