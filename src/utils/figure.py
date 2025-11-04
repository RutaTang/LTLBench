import io
from typing import Optional, Iterable

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



def plot_lines(
        df: pd.DataFrame,
        x: str = "number_of_operators",
        y: str = "accuracy",
        z: str = "model",
        title: Optional[str] = None,
        x_label: Optional[str] = None,
        y_label: Optional[str] = None,
        x_ticks: Optional[Iterable] = None,
        y_ticks: Optional[Iterable] = None,
        figsize: tuple[int, int] = (7, 4),
        marker: str = "o",
        grid: bool = True,
        legend_loc: str = "best",
) -> None:
    _ALLOWED_METRICS = {"accuracy", "precision", "recall", "f1", "auc"}
    if y not in _ALLOWED_METRICS:
        raise ValueError(f"y must be one of {_ALLOWED_METRICS}, got '{y}'")

    # Drop rows with missing essentials
    data = df[[x, y, z]].dropna()

    plt.figure(figsize=figsize)

    # One line per z
    for name, group in data.groupby(z):
        # Sort by x so lines are ordered
        group = group.sort_values(by=x)
        plt.plot(group[x], group[y], marker=marker, label=str(name))

    # Labels & ticks
    plt.title(title or y.capitalize())
    plt.xlabel(x_label or x.replace("_", " ").title())
    plt.ylabel(y_label or y.upper())

    if x_ticks is not None:
        plt.xticks(x_ticks)
    if y_ticks is not None:
        plt.yticks(y_ticks)

    if grid:
        plt.grid(True, linestyle="--", linewidth=0.5, alpha=0.6)

    plt.legend(title=z, loc=legend_loc)
    plt.tight_layout()
    plt.show()
