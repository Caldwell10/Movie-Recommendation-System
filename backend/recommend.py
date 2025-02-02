import pickle
import os
import torch
from sentence_transformers import SentenceTransformer, util

# ✅ Load the Preprocessed Dataset
pkl_path = os.path.join(os.path.dirname(__file__), "preprocessed_movies.pkl")

with open(pkl_path, "rb") as f:
    df = pickle.load(f)

print("✅ Preprocessed movie dataset loaded!")

# ✅ Load the Sentence Transformer Model
model = SentenceTransformer("all-MiniLM-L6-v2")
print("✅ Model loaded successfully!")

# ✅ Recommendation Logic
def get_similar_movies(user_query, top_n=5):
    try:
        # Convert user query into an embedding
        query_embedding = model.encode(user_query, convert_to_tensor=True).cpu()

        # Convert movie embeddings from DataFrame
        movie_embeddings = torch.stack([torch.tensor(e) for e in df["embeddings"].values])

        # Compute cosine similarity scores
        similarity_scores = util.pytorch_cos_sim(query_embedding, movie_embeddings)[0]

        # Get the top N most similar movies
        top_indices = torch.argsort(similarity_scores, descending=True)[:top_n]

        # Extract recommended movies
        recommendations = []
        for idx in top_indices:
            movie = df.iloc[idx.item()]
            recommendations.append({
                "title": movie["Series_Title"],
                "genres": ", ".join(movie["Genre"]),
                "year": int(movie["Released_Year"]),
                "rating": float(movie["IMDB_Rating"]),
                "summary": movie["Overview"],
            })
        return recommendations

    except Exception as e:
        print(f"Error in recommendation logic: {e}")
        return []
