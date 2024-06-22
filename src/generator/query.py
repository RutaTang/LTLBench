import numpy as np
from numpy.random import Generator

from src.utils.types import ReferenceValue


def generate_ltl_formulas(rng: Generator, states: list, formula_length: int, count_of_formulas: int) -> list[list]:
    """
    Generate LTL formulas

    :param states: a set of base/atomic states
    :param formula_length: length of a certain formula to generate
    :param count_of_formulas: number of formulas to generate
    :return: a list of LTL formulas
    """
    # Define the logical operators
    unary_operators = ['X', 'G', 'F', '!']  # Next, Globally, Finally, Not
    binary_operators = ['&', '|', '->']  # And, Or
    operators = unary_operators + binary_operators

    # Initialize the list of lists to hold formulas of increasing lengths
    B = [[] for _ in range(formula_length + 1)]
    B[0] = states

    # Generate m formulas
    formulas = []
    for _ in range(count_of_formulas):
        for j in range(1, formula_length + 1):
            # Randomly select an operator
            x = rng.choice(list(operators))

            if x in unary_operators:
                # Choose a formula from the previous set of formulas
                y = B[j - 1][rng.integers(0, len(B[j - 1]))]
                new_formula = [x, y]
            else:
                # Choose two formulas for binary operator
                s = rng.integers(0, j)
                y1 = B[s][rng.integers(0, len(B[s]))]
                y2 = B[j - 1 - s][rng.integers(0, len(B[j - 1 - s]))]

                new_formula = [y1, x, y2]

            # Add the new formula to the list
            B[j].append(new_formula)

        # Store the final processed formula
        formula = B[formula_length][-1]
        formulas.append(formula)

    return formulas


def _convert_ltl_formula_to_NuSMV(ltl_formula: list) -> list:
    """
    Convert LTL formula from `generate_ltl_formulas` to NuSMV format

    :param ltl_formula: LTL formula
    :return: NuSMV format of the LTL formula
    """
    for i in range(len(ltl_formula)):
        if isinstance(ltl_formula[i], list):
            ltl_formula[i] = _convert_ltl_formula_to_NuSMV(ltl_formula[i])
        if isinstance(ltl_formula[i], str) and ltl_formula[i].startswith('event'):
            ltl_formula[i] = f'state={ltl_formula[i]}'

    return ltl_formula


def convert_ltl_formula_to_NuSMV(ltl_formula: list) -> str:
    """
    Convert LTL formula from `generate_ltl_formulas` to NuSMV format

    :param ltl_formula: LTL formula
    :return: NuSMV format of the LTL formula
    """

    ltl_formula = _convert_ltl_formula_to_NuSMV(ltl_formula)
    return recursive_join(ltl_formula)


def recursive_join(l: list) -> str:
    """
    Recursively join the array

    :param l: list
    :return: a string
    """
    if isinstance(l, list):
        for i in range(len(l)):
            # wrap the state with parenthesis
            if isinstance(l[i], str) and l[i].startswith('state='):
                l[i] = f'({l[i]})'
        return '({})'.format(' '.join([recursive_join(x) for x in l]))
    else:
        return str(l)


def covert_ltl_formula_to_str(ltl_formula: list) -> str:
    """
    Convert LTL formula from `generate_ltl_formulas` to string

    :param ltl_formula: LTL formula
    :return: string format of the LTL formula
    """
    return recursive_join(ltl_formula)


def conver_ltl_formula_to_NL(ltl_formula: list, base_states: list, h_idx: ReferenceValue[int],
                             result: ReferenceValue[str] = None) -> str:
    """
    Convert LTL formula from `generate_ltl_formulas` to natural language

    :param ltl_formula: LTL formula
    :param base_states:
    :param h_idx:
    :param result:
    :return: the last H index
    """
    # reversely traverse the formula
    for i in range(len(ltl_formula)):
        if isinstance(ltl_formula[i], list):
            ltl_formula[i] = conver_ltl_formula_to_NL(ltl_formula[i], base_states, h_idx, result)

    h_idx.update(h_idx.get() + 1)
    # convert the formula to natural language
    if len(ltl_formula) == 2:  # unary
        operator = ltl_formula[0]
        operand = ltl_formula[1]
        if operator == "X":
            nl = f'{operand} will happen at next time'
        elif operator == "G":
            nl = f'{operand} will always happen at any future time'
        elif operator == "F":
            nl = f'{operand} will happen eventually'
        elif operator == "!":
            if operand in base_states:
                nl = f'{operand} does not happen'
            else:
                nl = f'{operand} does not hold'
        else:
            raise ValueError(f'Unknown operator: {operator}')
        nl = nl[0].upper() + nl[1:]
        nl = f'C{h_idx.get()}: {nl}.'
        result.update(f'{result.get()}\n{nl}')
        return f'C{h_idx.get()}'
    elif len(ltl_formula) == 3:  # binary
        left_operand = ltl_formula[0]
        operator = ltl_formula[1]
        right_operand = ltl_formula[2]
        if left_operand in base_states:
            left_operand = f'{left_operand} happens'
        else:
            left_operand = f'{left_operand} holds'
        if right_operand in base_states:
            right_operand = f'{right_operand} happens'
        else:
            right_operand = f'{right_operand} holds'
        if operator == "&":
            nl = f'{left_operand} and {right_operand}'
        elif operator == "|":
            nl = f'{left_operand} or {right_operand}'
        elif operator == "->":
            nl = f'That {left_operand} implies that {right_operand}'
        else:
            raise ValueError(f'Unknown operator: {operator}')
        nl = nl[0].upper() + nl[1:]
        nl = f'C{h_idx.get()}: {nl}.'
        result.update(f'{result.get()}\n{nl}')
        return f'C{h_idx.get()}'
