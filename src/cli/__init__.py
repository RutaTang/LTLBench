import os
import re

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
@click.option('--count_of_problem', '-c', help='Count of problems to generate', type=int, default=100)
@click.option('--number_of_events', '-e', help='Number of events', type=int, default=3)
@click.option('--formula_length', '-l', help='Length of the formula', type=int, default=3)
@click.option('--random_seed', '-s', help='Random seed', type=int, default=1)
def generate(count_of_problem: int, number_of_events: int,
             formula_length: int, random_seed: int):
    """
    Generate LTL problems
    """
    rng = np.random.default_rng(random_seed)
    problems = []
    for i in range(count_of_problem):
        problem = generate_problem(rng=rng, number_of_events=number_of_events, formula_length=formula_length)
        problems.append(problem)

    path = get_data_file_path(event_n=number_of_events, formula_n=formula_length, count=count_of_problem)
    pd.DataFrame(problems).to_csv(path, index=False)
    print(f'Generated {count_of_problem} problems to {path}.')


@app.command()
@click.option('--count_of_problem', '-c', help='Count of problems to generate', type=int, default=100)
@click.option('--number_of_events', '-e', help='Number of events', type=int, default=3)
@click.option('--formula_length', '-l', help='Length of the formula', type=int, default=3)
@click.option('--models', '-m', help='List of models', multiple=True, default=['qwen:32b-chat'])
def evaluate(count_of_problem: int, number_of_events: int,
             formula_length: int, models: tuple[str]):
    """
    Evaluate models
    """
    for model in models:
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
            data.at[index, 'prediction_raw'] = message

        path = get_evaluation_file_path(event_n=number_of_events, formula_n=formula_length, count=count_of_problem,
                                        model=model)
        data.to_csv(path, index=False)
        print(f'Evaluation result of {model} saved to {path}.')
