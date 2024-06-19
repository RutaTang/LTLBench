from unittest import TestCase

from src.core.context import generate_random_graph, plot_graph, generate_context_from_graph, code_template


class Test(TestCase):
    def test_generate_random_graph(self):
        nodes = ['A', 'B', 'C', 'D', 'E', 'F']
        random_graph = generate_random_graph(nodes)
        plot_graph(random_graph)

    def test_generate_context_from_graph(self):
        nodes = ['A', 'B']
        random_graph = generate_random_graph(nodes)
        plot_graph(random_graph)
        context = generate_context_from_graph(random_graph)
        print(context)

    def test_code_template(self):
        code = code_template(
            state=['a', 'b'],
            init='a',
            transition=[
                ('a', 'b'),
                ('b', 'a')
            ]
        )
        print(code)
