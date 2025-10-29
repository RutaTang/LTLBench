import os
import re
import time
from threading import Thread

import click
import numpy as np
import pandas as pd
import tqdm

from src.generator.data import generate_problem
from src.models.choose import choose_model
from src.utils.file import RESULT_FOLDER_PATH, DATA_FOLDER_PATH, get_evaluation_file_path, EVALUATION_FOLDER_PATH, \
    get_data_file_path
from src.strategies.direct import direct_prompt
from src.strategies.zero_shot_cot import cot_prompt
from src.strategies.few_shot_cot import few_shot_cot_prompt
from src.strategies.self_consistency import self_consistency_prompt
from src.strategies.least_to_most import least_to_most_prompt


@click.group()
def app():
    # init folder/file
    os.makedirs(RESULT_FOLDER_PATH, exist_ok=True)
    os.makedirs(DATA_FOLDER_PATH, exist_ok=True)
    os.makedirs(EVALUATION_FOLDER_PATH, exist_ok=True)
    print('Folders inited if not existed.')
    print(f'Result folder: {RESULT_FOLDER_PATH}')
    print(f'Data folder: {DATA_FOLDER_PATH}')
    print(f'Evaluation folder: {EVALUATION_FOLDER_PATH}')


@app.command()
@click.option('--count_of_problem', '-c', help='Count of problems to generate', type=int)
@click.option('--number_of_events', '-e', help='Number of events', type=int)
@click.option('--number_of_operators', '-l', help='Number of operators', type=int)
@click.option('--random_seed', '-s', help='Random seed', type=int, default=1)
def generate(count_of_problem: int, number_of_events: int,
             number_of_operators: int, random_seed: int):
    _generate(count_of_problem, number_of_events, number_of_operators, random_seed)


def _generate(count_of_problem: int, number_of_events: int,
              number_of_operators: int, random_seed: int):
    """
    Generate LTL problems
    """
    if count_of_problem % 2 != 0:
        raise ValueError('Count of problems must be even to ensure balanced data.')

    rng = np.random.default_rng(random_seed)
    problems = []
    problems_true = []
    problems_false = []

    # Generate problems while ensuring that there are equal number of true and false problems
    while (len(problems_false) + len(problems_true)) < count_of_problem:
        problem = generate_problem(rng=rng, number_of_events=number_of_events, formula_length=number_of_operators)
        if problem['answer'] and len(problems_true) < count_of_problem // 2:
            problems_true.append(problem)
        elif (not problem['answer']) and len(problems_false) < count_of_problem // 2:
            problems_false.append(problem)

    problems.extend(problems_true)
    problems.extend(problems_false)

    path = get_data_file_path(event_n=number_of_events, formula_n=number_of_operators, count=count_of_problem)
    pd.DataFrame(problems).to_csv(path, index=False)
    print(f'Generated {count_of_problem} problems to {path}.')


@app.command()
@click.option('--count_of_problem', '-c', help='Count of problems to generate', type=int)
@click.option('--list_of_numbers_of_events', '-e', help='List of numbers of events', type=str)
@click.option('--list_of_numbers_of_operators', '-l', help='List of numbers of operators', type=str)
@click.option('--random_seed', '-s', help='Random seed', type=int, default=1)
def batch_generate(count_of_problem: int, list_of_numbers_of_events: str,
                   list_of_numbers_of_operators: str, random_seed: int):
    # Parse
    list_of_numbers_of_events = [int(x) for x in list_of_numbers_of_events.split(',')]
    list_of_numbers_of_operators = [int(x) for x in list_of_numbers_of_operators.split(',')]
    # Generate problems in parallel
    threads = []
    for number_of_events in list_of_numbers_of_events:
        for formula_length in list_of_numbers_of_operators:
            thread = Thread(target=_generate, args=(count_of_problem, number_of_events, formula_length, random_seed))
            threads.append(thread)
            thread.start()

    print("Batch generation started (it should take time).")
    for thread in threads:
        thread.join()
    print("Batch generation completed.")


@app.command()
@click.option('--count_of_problem', '-c', help='Count of problems to generate', type=int)
@click.option('--number_of_events', '-e', help='Number of events', type=int)
@click.option('--number_of_operators', '-l', help='Number of operators', type=int)
@click.option('--model', '-m', help='Model name')
@click.option('--strategy', '-s', help='Prompt strategy to use',
              type=click.Choice(['direct', 'zero_shot_cot', 'few_shot_cot', 'self_consistency', 'least_to_most']),
              default='direct')
def evaluate(count_of_problem: int, number_of_events: int,
             number_of_operators: int, model: str, strategy: str):
    _evaluate(count_of_problem, number_of_events, number_of_operators, model, strategy)


def _evaluate(count_of_problem: int, number_of_events: int,
              number_of_operators: int, model: str, strategy: str = 'direct'):
    """
    Evaluate models
    """
    # Choose the strategy function
    strategy_map = {
        'direct': direct_prompt,
        'zero_shot_cot': cot_prompt,
        'few_shot_cot': few_shot_cot_prompt,
        'self_consistency': self_consistency_prompt,
        'least_to_most': least_to_most_prompt
    }

    strategy_func = strategy_map[strategy]

    path = get_data_file_path(event_n=number_of_events, formula_n=number_of_operators, count=count_of_problem)
    data = pd.read_csv(path)

    for index, row in tqdm.tqdm(data.iterrows(), total=len(data)):
        question = row['question']

        # Initialize fresh LLM for each problem
        llm = choose_model(model)

        # Use the selected strategy
        response, answer = strategy_func(question, llm)

        # Convert answer to numeric format
        if answer is None:
            result = -1
        else:
            answer = answer.lower()
            result = 1 if answer == 'true' else 0

        data.at[index, 'prediction'] = result
        data.at[index, 'prediction_raw'] = str(response)

    path = get_evaluation_file_path(event_n=number_of_events, formula_n=number_of_operators, count=count_of_problem,
                                    model=model)
    # Include strategy in the filename
    path = path.replace('.csv', f'_{strategy}.csv')
    data.to_csv(path, index=False)
    print(f'Evaluation result of {model} with {strategy} strategy saved to {path}.')


@app.command()
@click.option('--count_of_problem', '-c', help='Count of problems to generate', type=int)
@click.option('--list_of_numbers_of_events', '-e', help='List of numbers of events', type=str)
@click.option('--list_of_numbers_of_operators', '-l', help='List of numbers of operators', type=str)
@click.option('--model', '-m', help='Model name', default='qwen:7b-chat')
@click.option('--strategy', '-s', help='Prompt strategy to use',
              type=click.Choice(['direct', 'zero_shot_cot', 'few_shot_cot', 'self_consistency', 'least_to_most']),
              default='direct')
def batch_evaluate(count_of_problem: int, list_of_numbers_of_events: str,
                   list_of_numbers_of_operators: str, model: str, strategy: str):
    # Parse
    list_of_numbers_of_events = [int(x) for x in list_of_numbers_of_events.split(',')]
    list_of_numbers_of_operators = [int(x) for x in list_of_numbers_of_operators.split(',')]

    # Evaluate problems in parallel
    threads = []
    for number_of_events in list_of_numbers_of_events:
        for formula_length in list_of_numbers_of_operators:
            thread = Thread(target=_evaluate, args=(count_of_problem, number_of_events, formula_length, model, strategy))
            threads.append(thread)
            thread.start()

    print("Batch evaluation started (it should take time).")
    for thread in threads:
        thread.join()
    print("Batch evaluation completed.")
