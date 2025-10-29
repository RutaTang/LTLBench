from numpy.random import Generator

from src.generator.context import generate_random_directed_graph, generate_nodes, generate_context_from_graph, code_template
from src.generator.query import generate_ltl_formulas, convert_ltl_formula_to_nl, convert_ltl_formula_to_nusmv, \
    covert_ltl_formula_to_str_formula
from copy import deepcopy

from src.utils.external import call_nusmv
from src.utils.figure import save_graph_to_string
from src.utils.types import ReferenceValue


def generate_problem(rng: Generator, number_of_events: int, formula_length: int) -> dict:
    """
    Generate a problem:
    1. Question: A question that needs to be answered consisting of a context (premises) and a query (hypothesis).
    2. Answer: The answer to the question.
    3. Many other fields such as code, formula, graph, etc.

    :param rng: a np.random.Generator
    :param number_of_events: the number of nodes in the graph.
    :param formula_length: length of the formula, len = count of operator of a formula.
    :return: a dictionary containing related fields
    """
    # Generate a context
    nodes = generate_nodes(number_of_events)
    graph = generate_random_directed_graph(rng=rng, nodes=nodes)
    context = generate_context_from_graph(rng=rng, graph=graph)

    # Generate a query
    formula = generate_ltl_formulas(rng=rng, states=nodes, formula_length=formula_length, count_of_formulas=1).pop()
    h_idx = ReferenceValue(0)
    query = ReferenceValue("")
    last_case = convert_ltl_formula_to_nl(ltl_formula=deepcopy(formula), base_states=nodes, c_idx=h_idx, result=query)
    query = query.get()
    query = f'{query}'

    # Initialize the init_state
    init_state = rng.choice(nodes)

    # Prepare the question
    context = f'Initially, {init_state} happened. {context}'
    query = f'{query}'.strip()

    # Prepare code
    context_code = code_template(state=list(nodes), init=init_state, transition=list(graph.edges))
    query_code = convert_ltl_formula_to_nusmv(ltl_formula=deepcopy(formula))
    query_code = f'LTLSPEC {query_code}'
    code = f'{context_code}\n{query_code}\n'

    # Prepare the answer
    answer = call_nusmv(code)

    problem = {
        "context": context,
        "query": query,
        "question": f'''\
=== Context ===\n
{context}\n
=== Hypothesis ===\n
{query}

{last_case} is True or False?
''',
        "code": code,
        "formula": covert_ltl_formula_to_str_formula(formula),
        "answer": answer,
        "graph": save_graph_to_string(graph),
    }
    return problem
