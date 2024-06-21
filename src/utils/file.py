import os

RESULT_FOLDER = './results'
DATA_FOLDER = os.path.join(RESULT_FOLDER, 'data')
EVALUATION_FOLDER = os.path.join(RESULT_FOLDER, 'evaluation')


def get_data_file_path(event_n: int, formula_n: int, count: int):
    return os.path.join(DATA_FOLDER, f'{count}_{event_n}_events_{formula_n}_formula_len.csv')


def get_evaluation_file_path(event_n: int, formula_n: int, count: int, model: str):
    folder = os.path.join(EVALUATION_FOLDER, f'{count}_{event_n}_events_{formula_n}_formula_len')
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, f'{model}.csv')
    return path
