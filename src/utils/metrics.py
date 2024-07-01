import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score, roc_auc_score


def metrics(data: pd.DataFrame) -> dict:
    """
    Calculate the accuracy, precision, recall, f1, auc score of the data, round to 2 decimal places
    :param data: DataFrame with columns 'answer' and 'prediction'
    :return: Dictionary with the metrics
    """
    # Accuracy
    accuracy_raw = accuracy_score(data['answer'], data['prediction'])
    # Precision
    precision_raw = precision_score(data['answer'], data['prediction'], average='macro', zero_division=0)
    # Recall
    recall_raw = recall_score(data['answer'], data['prediction'], average='macro', zero_division=0)
    # F1
    f1_raw = f1_score(data['answer'], data['prediction'], average='macro', zero_division=0)
    # AUC
    auc_raw = roc_auc_score(data['answer'], data['prediction'])
    return {
        'raw': {
            'accuracy': accuracy_raw,
            'precision': precision_raw,
            'recall': recall_raw,
            'f1': f1_raw,
            'auc': auc_raw
        },
        'formatted': {
            'accuracy': f'{accuracy_raw:.2f}',
            'precision': f'{precision_raw:.2f}',
            'recall': f'{recall_raw:.2f}',
            'f1': f'{f1_raw:.2f}',
            'auc': f'{auc_raw:.2f}'
        }
    }
