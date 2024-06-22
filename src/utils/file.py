import os

RESULT_FOLDER_PATH = './results'
DATA_FOLDER_PATH = os.path.join(RESULT_FOLDER_PATH, 'data')
EVALUATION_FOLDER_PATH = os.path.join(RESULT_FOLDER_PATH, 'evaluation')


def get_data_file_path(event_n: int, formula_n: int, count: int):
    return os.path.join(DATA_FOLDER_PATH, f'{count}_{event_n}_events_{formula_n}_formula_len.csv')


def get_evaluation_file_path(event_n: int, formula_n: int, count: int, model: str):
    folder = os.path.join(EVALUATION_FOLDER_PATH, f'{count}_{event_n}_events_{formula_n}_formula_len')
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, f'{model}.csv')
    return path
