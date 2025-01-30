import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sentence_transformers import SentenceTransformer
import pickle
import os

# Define paths
dataset_path = "/Users/caldwellwachira/Downloads/Bulk-Files/datasets/imdb_top_1000.csv"
preprocessed_dataset_path = "/Users/caldwellwachira/Downloads/Bulk-Files/preprocessed_datasets/preprocessed_movies.pkl"

# Ensure output directory exists
os.makedirs(os.path.dirname(preprocessed_dataset_path), exist_ok=True)

# Load dataset
df = pd.read_csv(dataset_path)

# Drop rows with missing critical fields
df = df.dropna(subset=["Series_Title", "Genre", "Overview"])

# Drop unnecessary columns
df = df.drop(columns=["Poster_Link", "Certificate", "Meta_score"], errors="ignore")

# Fill missing values for numeric columns
df["Gross"] = df["Gross"].fillna(0)
df["No_of_votes"] = df["No_of_votes"].fillna(0)

# Convert 'Released_Year' to numeric, remove invalid values
df["Released_Year"] = pd.to_numeric(df["Released_Year"], errors="coerce")
df = df.dropna(subset=["Released_Year"])
df["Released_Year"] = df["Released_Year"].astype(int)

# Normalize numerical values
scaler = MinMaxScaler()
df["Gross_normalized"] = scaler.fit_transform(df[["Gross"]])
df["Votes_normalized"] = scaler.fit_transform(df[["No_of_votes"]])

# Process genres
df["Genre"] = df["Genre"].str.split(",")

# Create metadata for embeddings
df["metadata"] = df["Series_Title"] + " " + df["Genre"].apply(lambda x: " ".join(x)) + " " + df["Overview"]

# Generate embeddings
print("Generating embeddings...")
model = SentenceTransformer("all-MiniLM-L6-v2")
df["embeddings"] = df["metadata"].tolist()  # Fix issue before encoding
df["embeddings"] = list(model.encode(df["metadata"].tolist(), show_progress_bar=True))
print("Embeddings generated!")

# Save the preprocessed dataset
with open(preprocessed_dataset_path, "wb") as f:
    pickle.dump(df, f)

print(f"Preprocessed dataset saved to {preprocessed_dataset_path}")
print("Preprocessing complete!")
