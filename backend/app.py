from mmap import ALLOCATIONGRANULARITY

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI
app = FastAPI()


# Load Model and Tokenizer
model_name = "/Users/caldwellwachira/Downloads/Bulk-Files/models/checkpoint-5000"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# Define Input Schema
class RecommendationRequest(BaseModel):
    user_input: str # User input for movie preferences

@app.post("/recommend")
def recommend_movies(request: RecommendationRequest):
    try:
        # Tokenize input
        inputs = tokenizer(request.user_input, return_tensors="pt", padding=True, truncation=True)

        # Make prediction
        with torch.no_grad():
            outputs = model(**inputs)

        # Since it is a classification model with scores for movie genres
        scores = torch.softmax(outputs.logits, dim=1).tolist()[0]
        genre_scores= {f"Genre {i}": score for i, score in enumerate(scores)}

        #Return recommendations
        return {"recommendations": genre_scores}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001", "http://127.0.0.1:3001"],  # Allow both
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

