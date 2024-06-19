import os

import click
import pandas as pd

from src.generator.data import generate_problem
from src.utils.file import RESULT_FOLDER, DATA_FOLDER, LTL_DATA_PATH


@click.group()
def app():
    # init folder/file
    print('Init folders...')
    os.makedirs(RESULT_FOLDER, exist_ok=True)
    os.makedirs(DATA_FOLDER, exist_ok=True)


@app.command()
@click.option('--path', '-p', help='Path to save the generated problems', type=str, default=LTL_DATA_PATH)
@click.option('--count_of_problem', '-c', help='Count of problems to generate', type=int, default=1000)
@click.option('--number_of_events', '-e', help='Number of events', type=int, default=3)
@click.option('--formula_length', '-l', help='Length of the formula', type=int, default=3)
def generate(path: str, count_of_problem: int, number_of_events: int,
             formula_length: int):
    '''
    Generate LTL problems
    '''
    problems = []
    for i in range(count_of_problem):
        problem = generate_problem(number_of_events=number_of_events, formula_length=formula_length)
        problems.append(problem)

    pd.DataFrame(problems).to_csv(path, index=False)
    print(f'Generated {count_of_problem} problems to {path}.')
