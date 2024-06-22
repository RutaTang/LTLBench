import base64
import io
from unittest import TestCase
from matplotlib import pyplot as plt
import matplotlib.image as mpimg

import networkx as nx

from src.utils.figure import save_graph_to_string


class Test(TestCase):
    def test_save_graph(self):
        graph = nx.DiGraph()
        graph.add_node(1)
        graph.add_node(2)
        graph.add_edge(1, 2)
        graphml_str = save_graph_to_string(graph)
        graph = nx.read_graphml(io.StringIO(graphml_str))
        nx.draw(graph, with_labels=True, font_weight='bold', node_size=2000, font_size=10, arrows=True)
        plt.show()
