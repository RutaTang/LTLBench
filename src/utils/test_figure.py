import base64
import io
from unittest import TestCase

import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.image as mpimg

import networkx as nx

from src.utils.figure import save_graph_to_string, plot_lines


class Test(TestCase):
    def test_save_graph_to_string(self):
        graph = nx.DiGraph()
        graph.add_node(1)
        graph.add_node(2)
        graph.add_edge(1, 2)
        graphml_str = save_graph_to_string(graph)
        self.assertTrue(len(graphml_str) > 0)

    def test_plot_graph(self):
        graph = nx.DiGraph()
        nodes = ["event1", "event2", "event3"]
        edges = [("event1", "event2"), ("event2", "event3")]
        graph.add_nodes_from(nodes)
        graph.add_edges_from(edges)
        plt.figure()
        nx.draw(graph, with_labels=True, node_size=3000, node_color='skyblue')
        plt.show()

    def test_plot_metrics(self):
        data = {
            'x': [1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5],
            'y': [2, 3, 5, 7, 11, 1, 4, 6, 8, 9, 2, 2, 3, 3, 5],
            'mode': ['Mode 1', 'Mode 1', 'Mode 1', 'Mode 1', 'Mode 1',
                     'Mode 2', 'Mode 2', 'Mode 2', 'Mode 2', 'Mode 2',
                     'Mode 3', 'Mode 3', 'Mode 3', 'Mode 3', 'Mode 3']
        }
        df = pd.DataFrame(data)

        # just plot
        plot_lines(df, 'x', 'y', 'mode', title='Test', x_label='X', y_label='Y')
