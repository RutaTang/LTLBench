import os
import re
from threading import Thread

import click
import numpy as np
import pandas as pd
import tqdm

from src.generator.data import generate_problem
from src.models.choose import choose_model
from src.utils.file import RESULT_FOLDER_PATH, DATA_FOLDER_PATH, get_evaluation_file_path, EVALUATION_FOLDER_PATH, \
    get_data_file_path


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
@click.option('--count_of_problem', '-c', help='Count of problems to generate', type=int, default=300)
@click.option('--number_of_events', '-e', help='Number of events', type=int, default=3)
@click.option('--formula_length', '-l', help='Length of the formula', type=int, default=3)
@click.option('--random_seed', '-s', help='Random seed', type=int, default=1)
def generate(count_of_problem: int, number_of_events: int,
             formula_length: int, random_seed: int):
    _generate(count_of_problem, number_of_events, formula_length, random_seed)


def _generate(count_of_problem: int, number_of_events: int,
              formula_length: int, random_seed: int):
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
        problem = generate_problem(rng=rng, number_of_events=number_of_events, formula_length=formula_length)
        if problem['answer'] and len(problems_true) < count_of_problem // 2:
            problems_true.append(problem)
        elif (not problem['answer']) and len(problems_false) < count_of_problem // 2:
            problems_false.append(problem)

    problems.extend(problems_true)
    problems.extend(problems_false)

    path = get_data_file_path(event_n=number_of_events, formula_n=formula_length, count=count_of_problem)
    pd.DataFrame(problems).to_csv(path, index=False)
    print(f'Generated {count_of_problem} problems to {path}.')


@app.command()
@click.option('--count_of_problem', '-c', help='Count of problems to generate', type=int, default=300)
@click.option('--list_of_number_of_events', '-e', help='List of number of events', type=int, multiple=True,
              default=(2, 3, 4, 5, 6))
@click.option('--list_of_formula_length', '-l', help='List of length of the formula', type=int, multiple=True,
              default=(2, 3, 4, 5, 6))
@click.option('--random_seed', '-s', help='Random seed', type=int, default=1)
def batch_generate(count_of_problem: int, list_of_number_of_events: list[int],
                   list_of_formula_length: list[int], random_seed: int):
    threads = []
    for number_of_events in list_of_number_of_events:
        for formula_length in list_of_formula_length:
            thread = Thread(target=_generate, args=(count_of_problem, number_of_events, formula_length, random_seed))
            threads.append(thread)
            thread.start()

    print("Batch generation started (it should take time).")
    for thread in threads:
        thread.join()
    print("Batch generation completed.")


@app.command()
@click.option('--count_of_problem', '-c', help='Count of problems to generate', type=int, default=300)
@click.option('--number_of_events', '-e', help='Number of events', type=int, default=3)
@click.option('--formula_length', '-l', help='Length of the formula', type=int, default=3)
@click.option('--model', '-m', help='Model name', default='qwen:7b-chat')
def evaluate(count_of_problem: int, number_of_events: int,
             formula_length: int, model: str):
    _evaluate(count_of_problem, number_of_events, formula_length, model)


def _evaluate(count_of_problem: int, number_of_events: int,
              formula_length: int, model: str):
    """
    Evaluate models
    """
    path = get_data_file_path(event_n=number_of_events, formula_n=formula_length, count=count_of_problem)
    data = pd.read_csv(path)
    llm = choose_model(model)
    llm.reconfig({
        'max_tokens': 5,
    })
    for index, row in tqdm.tqdm(data.iterrows(), total=len(data)):
        question = row['question']
        message = llm.chat(message=question)
        pattern = r'(true|false)'
        result = re.search(pattern, message, flags=re.IGNORECASE)
        if result is None:
            result = -1
        else:
            result = result.group(0)
            result = result.lower()
            result = 1 if result == 'true' else 0
        data.at[index, 'prediction'] = result
        data.at[index, 'prediction_raw'] = str(message)

    path = get_evaluation_file_path(event_n=number_of_events, formula_n=formula_length, count=count_of_problem,
                                    model=model)
    data.to_csv(path, index=False)
    print(f'Evaluation result of {model} saved to {path}.')


@app.command()
@click.option('--count_of_problem', '-c', help='Count of problems to generate', type=int, default=300)
@click.option('--list_of_number_of_events', '-e', help='List of number of events', type=int, multiple=True,
              default=(2,))
@click.option('--list_of_formula_length', '-l', help='List of length of the formula', type=int, multiple=True,
              default=(2, 3, 4, 5, 6))
@click.option('--model', '-m', help='Model name', default='qwen:7b-chat')
def batch_evaluate(count_of_problem: int, list_of_number_of_events: list[int],
                   list_of_formula_length: list[int], model: str):
    threads = []
    for number_of_events in list_of_number_of_events:
        for formula_length in list_of_formula_length:
            thread = Thread(target=_evaluate, args=(count_of_problem, number_of_events, formula_length, model))
            threads.append(thread)
            thread.start()

    print("Batch evaluation started (it should take time).")
    for thread in threads:
        thread.join()
    print("Batch evaluation completed.")
