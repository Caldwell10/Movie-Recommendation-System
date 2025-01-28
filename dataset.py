import torch

"""
A custom PyTorch dataset class to pair the tokenized data (input_ids, attention_mask) with their labels.
Converts each batch of encodings and labels into tensors.
"""
class SentimentDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        """
        Initializes the dataset with tokenized encodings and their corresponding labels.

        Args:
            encodings (dict): Tokenized data with keys like 'input_ids' and 'attention_mask'.
            labels (list): List of labels (e.g., 0 for negative, 1 for positive).
        """
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        """
        Retrieves a single item from the dataset.

        Args:
            idx (int): Index of the item to retrieve.

        Returns:
            dict: A dictionary containing tokenized inputs and the label.
        """
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        """
        Returns the length of the dataset.

        Returns:
            int: Number of items in the dataset.
        """
        return len(self.labels)