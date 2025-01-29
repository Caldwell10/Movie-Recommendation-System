import pandas as pd
from sklearn.model_selection import train_test_split
from transformers import BertTokenizer
from backend.dataset import SentimentDataset


# Step 1: Load dataset
dataset_path = "/Users/caldwellwachira/Downloads/Bulk-Files/datasets/IMDB_Dataset.csv"
data = pd.read_csv(dataset_path)

# Step 2: Encode the sentiment labels
# Convert 'positive' to 1 and 'negative' to 0
data['sentiment'] = data['sentiment'].map({'positive': 1, 'negative': 0})

# Step 3: Split the dataset into train, validation and test sets
train_texts, test_texts, train_labels, test_labels = train_test_split(
    data['review'], data['sentiment'], test_size=0.2, random_state=42
)

# Further split the test set to create a validation set
val_texts, test_texts,val_labels,test_labels=train_test_split(
    test_texts, test_labels, test_size=0.5, random_state=42
)

# Step 4: Tokenize the data using BERT tokenzier
# Initialize the tokenizer

"""
Tokenization is the process of breaking down raw text into smaller chunks (tokens) that a machine learning model can understand. For example, in BERT:

Words → Tokens: It splits the text into smaller units (e.g., words or subwords).
Tokens → IDs: Each token is converted into a numerical ID from BERT's predefined vocabulary.
"""
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# Define a function to tokenize the text data
def tokenize_data(texts):
    return tokenizer(texts.tolist(), truncation=True, padding=True, max_length=128, return_tensors="pt")

# Tokenize train, validation and test sets
train_encodings = tokenize_data(train_texts)
val_encodings = tokenize_data(val_texts)
test_encodings = tokenize_data(test_texts)

# Step 4: Create PyTorch datasets
train_dataset = SentimentDataset(train_encodings, train_labels.tolist())
val_dataset = SentimentDataset(val_encodings, val_labels.tolist())
test_Dataset = SentimentDataset(test_encodings, test_labels.tolist())



