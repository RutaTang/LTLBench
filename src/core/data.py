import json

import numpy as np

from src.core.context import generate_random_graph, generate_nodes, generate_context_from_graph, code_template
from src.core.query import generate_ltl_formulas, conver_ltl_formula_to_NL, convert_ltl_formula_to_NuSMV
from copy import deepcopy

from src.utils.external import call_NuSMV


def generate_problem(number_of_events: int, formula_length: int) -> dict:
    """
    Generate a problem:
    1. Question: A question that needs to be answered consisting of a context (premises) and a query (hypothesis).
    2. Answer: The answer to the question.

    :param count_of_formulas:
    :param formula_length:
    :param number_of_events: the number of nodes in the graph.
    :return: a dictionary containing the question and the answer.
    """
    # Generate a context
    nodes = generate_nodes(number_of_events)
    graph = generate_random_graph(nodes=list(nodes))
    context = generate_context_from_graph(graph=graph)

    # Generate a query
    formula = generate_ltl_formulas(states=nodes, formula_length=formula_length, count_of_formulas=1).pop()
    query = conver_ltl_formula_to_NL(ltl_formula=deepcopy(formula), base_states=nodes)
    query = query[0].upper() + query[1:] + "."

    # Initialize the init_state
    init_state = np.random.choice(list(nodes))

    # Prepare the question
    context = f'Initially, {init_state} is happened. {context}'
    query = (f'Determine whether the following statement is true or false (answering in "true" or "false" '
             f'directly):\n {query}')

    # Prepare code
    context_code = code_template(state=list(nodes), init=init_state, transition=list(graph.edges))
    print(formula)
    query_code = convert_ltl_formula_to_NuSMV(ltl_formula=deepcopy(formula))
    query_code = f'LTLSPEC {query_code}'
    print(query_code)
    code = f'{context_code}\n{query_code}\n'

    # Prepare the answer
    answer = call_NuSMV(code)
    print(answer)

    problem = {
        "context": context,
        "query": query,
        "code": code,
        "answer": answer
    }
    return problem
