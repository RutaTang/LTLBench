from unittest import TestCase

import numpy as np

from src.generator.context import generate_random_directed_graph, plot_graph, generate_context_from_graph, code_template


class TestGenerateRandomDirectedGraph(TestCase):
    def test_three_nodes(self):
        rng = np.random.default_rng(1)
        nodes = ['Node-A', 'Node-B', 'Node-C']
        random_graph = generate_random_directed_graph(rng, nodes)

        # ===assertions===
        for node in nodes:
            self.assertTrue(random_graph.has_node(node))
        self.assertTrue(len(random_graph.edges) == 3)

    def test_empty_nodes(self):
        rng = np.random.default_rng(1)
        nodes = []
        random_graph = generate_random_directed_graph(rng, nodes)

        # ===assertions===
        self.assertTrue(len(random_graph.nodes) == 0)

    def test_nodes_must_be_unique(self):
        rng = np.random.default_rng(1)
        nodes = ["Node-A", "Node-A", "Node-B"]

        # ===assertions===
        with self.assertRaises(ValueError):
            generate_random_directed_graph(rng, nodes)


class TestGenerateContextFromGraph(TestCase):
    def test_default(self):
        rng = np.random.default_rng(1)
        nodes = ['Node-A', 'Node-B', 'Node-C']
        random_graph = generate_random_directed_graph(rng, nodes)
        context = generate_context_from_graph(rng, random_graph)

        # ===assertions===
        context = context.split('.')
        context.remove('')
        self.assertTrue(len(context) == len(random_graph.edges))



