from sklearn.metrics import accuracy_score, precision_recall_fscore_support
import torch

def compute_metrics(eval_pred):
    """
    Computes accuracy, recall, and F1 score
    Args:
        eval_pred: A tuple ( logits, labels).
    :return:
        dict: A dictionary with accuracy, precision, recall, and F1 score
    """
    logits, labels = eval_pred
    predictions = torch.argmax(torch.tensor(logits), dim=1)
    accuracy =accuracy_score(labels, predictions)
    precision, recall, f1, _ = precision_recall_fscore_support(labels, predictions)
    return{"accuracy": accuracy, "precision": precision, "recall": recall, "f1-score": f1}


