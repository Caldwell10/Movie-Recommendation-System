import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sentence_transformers import SentenceTransformer
import pickle

# Load dataset
dataset_path = "/Users/caldwellwachira/Downloads/Bulk-Files/datasets/imdb_top_1000.csv"
preprocessed_dataset_path = "/Users/caldwellwachira/Downloads/Bulk-Files/preprocessed_movies.pkl"
df = pd.read_csv(dataset_path)

# Print column names to check if "No_of_votes" exists
print("Columns in dataset:", df.columns)

# Rename columns to match expected names (if needed)
df = df.rename(columns={"No_of_Votes": "No_of_votes", "IMDB_Rating": "IMDB_Rating"})  # Adjust if needed

# Drop rows with missing values in critical fields
df = df.dropna(subset=["Series_Title", "Genre", "Overview"])

# Drop unnecessary columns
df = df.drop(columns=["Poster_Link", "Certificate", "Meta_score"], errors="ignore")

# Fill missing values for numeric columns
df["Gross"] = df["Gross"].fillna("0")  # Fill missing values with "0" before conversion

# Convert 'Gross' to numeric (remove commas and convert to float)
df["Gross"] = df["Gross"].astype(str).str.replace(",", "").astype(float)

# Convert 'No_of_votes' if it exists
if "No_of_votes" in df.columns:
    df["No_of_votes"] = df["No_of_votes"].fillna(0)
else:
    print("Warning: 'No_of_votes' column not found in dataset!")

# Convert 'Released_Year' to numeric
df["Released_Year"] = pd.to_numeric(df["Released_Year"], errors="coerce")
df = df.dropna(subset=["Released_Year"])
df["Released_Year"] = df["Released_Year"].astype(int)

# Normalize numeric values
scaler = MinMaxScaler()
df["Gross_normalized"] = scaler.fit_transform(df[["Gross"]])
df["Votes_normalized"] = scaler.fit_transform(df[["No_of_votes"]]) if "No_of_votes" in df.columns else 0

# Process genres
df["Genre"] = df["Genre"].str.split(",")

# Create metadata for embeddings
df["metadata"] = df["Series_Title"] + " " + df["Genre"].apply(lambda x: " ".join(x)) + " " + df["Overview"]

# Generate embeddings
print("Generating embeddings...")
model = SentenceTransformer("all-MiniLM-L6-v2")
df["embeddings"] = df["metadata"].apply(lambda x: model.encode(x))
print("Embeddings generated!")

# Save the preprocessed dataset
with open(preprocessed_dataset_path, "wb") as f:
    pickle.dump(df, f)

print(f"Preprocessed dataset saved to {preprocessed_dataset_path}")
print("Preprocessing complete!")
