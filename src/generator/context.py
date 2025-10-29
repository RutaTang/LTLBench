import networkx as nx
from matplotlib import pyplot as plt
from networkx import DiGraph
from numpy.random import Generator
from collections import defaultdict

def generate_random_directed_graph(rng: Generator, nodes: list) -> DiGraph:
    """
    Generate a random directed graph from a list of nodes

    :param rng: a np.random.Generator
    :param nodes: list of nodes
    :return: a random directed graph
    """
    if len(nodes) != len(set(nodes)):
        raise ValueError('Nodes must be unique')
    graph = nx.DiGraph()
    graph.add_nodes_from(nodes)
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            # Add an edge from i to j with 50% probability
            if rng.random() > 0.5:
                graph.add_edge(nodes[i], nodes[j])
            # Add an edge from j to i with 50% probability
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


def generate_context_from_graph(rng: Generator, graph: nx.DiGraph) -> str:
    """
    Generate a context from the given directed graph

    :param rng: a np.random.Generator
    :param graph: a directed graph
    :return: context
    """
    context = []

    nodes = sorted(list(graph.nodes))
    node = rng.choice(nodes)
    visited = set()
    queue = [node]
    while len(queue) > 0:
        node = queue.pop(0)
        visited.add(node)

        # Get all neighbors for this node
        neighbors = sorted(list(graph.neighbors(node)))

        if len(neighbors) == 0:
            context.append(f'After {node}, no other events can happen.')
        elif len(neighbors) == 1:
            context.append(f'After {node}, {neighbors[0]} must happen.')
        else:
            neighbors_str = ', '.join(neighbors[:-1]) + f', or {neighbors[-1]}'
            context.append(f'After {node}, either {neighbors_str} must happen.')

        for neighbor in neighbors:
            if neighbor not in visited:
                queue.append(neighbor)

        if len(queue) == 0 and len(visited) != len(nodes):
            node = sorted(list(set(nodes) - visited))[0]
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

    trans_dict = defaultdict(list)
    for t in transition:
        trans_dict[t[0]].append(t[1])

    trans = []
    for source, targets in sorted(trans_dict.items()):
        if len(targets) == 1:
            t_str = f'state = {source} : {targets[0]};'
        else:
            target_set = '{' + ', '.join(sorted(targets)) + '}'
            t_str = f'state = {source} : {target_set};'
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
