import io
from typing import Optional

import networkx as nx
import numpy as np
from networkx import DiGraph
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

COLOR_PALETTE = "deep"


def save_graph_to_string(graph: DiGraph) -> str:
    """
    Save graph to string

    :param graph: graph
    :return: graphml string
    """
    graphml = nx.generate_graphml(graph)
    return '\n'.join(graphml)


def plot_lines(data: pd.DataFrame, x: str, y: str, z: str, title: str, x_label: str, y_label: str,
               x_ticks: Optional[list] = None, y_ticks: Optional[list] = None,
               fig_size: tuple[float, float] = (16, 5)):
    palette = sns.color_palette(COLOR_PALETTE, len(data[z].unique()))

    # Group the data by the z column
    grouped = data.groupby(z)

    # Create a new figure
    plt.figure(figsize=fig_size)

    # Plot each mode
    for (mode, group), color in zip(grouped, palette):
        plt.plot(group[x], group[y], label=mode, marker='s', color=color)

    # Add a legend
    plt.legend()

    # Add title and labels
    plt.title(title, fontsize=20)
    plt.xlabel(x_label, fontsize=15)
    plt.ylabel(y_label, fontsize=15)
    if isinstance(x_ticks, list):
        plt.xticks(x_ticks)
    if isinstance(y_ticks, list):
        plt.yticks(y_ticks)
    # Show the plot
    plt.show()
