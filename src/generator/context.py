import networkx as nx
from matplotlib import pyplot as plt
from numpy.random import Generator


def generate_random_graph(rng: Generator, nodes: list):
    """
    Generate a random graph from a set of nodes

    :param nodes: list of nodes
    :return: a random graph
    """
    graph = nx.DiGraph()
    graph.add_nodes_from(nodes)
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            if rng.random() > 0.5:
                graph.add_edge(nodes[i], nodes[j])
            if rng.random() > 0.5:
                graph.add_edge(nodes[j], nodes[i])

    return graph


def plot_graph(graph: nx.Graph):
    """
    Plot a graph

    :param graph: a graph
    :return:
    """
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_color='skyblue', node_size=2000, edge_color='gray', font_size=15,
            font_color='black')
    plt.show()


def generate_context_from_graph(rng: Generator, graph: nx.Graph) -> (str, tuple):
    """
    Generate a context from the given graph

    :param graph: a graph
    :return: context and code
    """
    context = []

    nodes = list(graph.nodes)
    node = rng.choice(nodes)
    visited = set()
    queue = [node]
    while len(queue) > 0:
        node = queue.pop(0)
        visited.add(node)

        for neighbor in graph.neighbors(node):
            str = f'After {node}, {neighbor} will happen.'
            context.append(str)
            str = ""
            if neighbor not in visited:
                queue.append(neighbor)

        if len(list(graph.neighbors(node))) == 0:
            context.append(f'After {node}, no other events will happen.')

        if len(queue) == 0 and len(visited) != len(nodes):
            node = list(set(nodes) - visited)[0]
            queue.append(node)

    context = ' '.join(context)
    return context


def code_template(state: list[str], init: str, transition: list[tuple[str, str]]):
    """
    Generate a code template for NuSMV model checker

    :param state: list of states like ['s1', 's2', 's3']
    :param init: one of the state like 's1'
    :param transition: list of tuples like [('s1', 's2'), ('s2', 's3')], "s1" -> "s2" and "s2" -> "s3"
    :return:
    """
    # Add self loop for the states that are not in the transition for exclusive state purpose in NuSMV
    starts = set([t[0] for t in transition])
    not_starts = set(state) - starts
    for s in not_starts:
        transition.append((s, s))
    # Generate the code
    state: str = ', '.join(state)
    trans = []
    for t in transition:
        t_str = f'state = {t[0]} : {t[1]};'
        trans.append(t_str)
    trans = '\n\t\t'.join(trans)

    template = f'''\
MODULE main
VAR
    state : {{{state}}};
ASSIGN
    init(state) := {init};
    next(state) := case
        {trans}
    esac;'''
    return template


def generate_nodes(n: int) -> list[str]:
    """
    Generate a set of nodes

    :param n: number of nodes
    :return: list of nodes
    """
    nodes = [f'event{i}' for i in range(1, n + 1)]
    return nodes
