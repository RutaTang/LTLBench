import base64
import io
from unittest import TestCase
from matplotlib import pyplot as plt
import matplotlib.image as mpimg

import networkx as nx

from src.utils.figure import save_graph_to_string


class Test(TestCase):
    def test_save_graph_to_string(self):
        graph = nx.DiGraph()
        graph.add_node(1)
        graph.add_node(2)
        graph.add_edge(1, 2)
        graphml_str = save_graph_to_string(graph)
        self.assertTrue(len(graphml_str) > 0)
