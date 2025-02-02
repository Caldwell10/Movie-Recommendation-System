from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from recommend import get_similar_movies

# ✅ Initialize FastAPI
app = FastAPI()

# ✅ Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001", "http://127.0.0.1:3001"],  # Allow frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Define Input Schema
class RecommendationRequest(BaseModel):
    user_input: str

# API Endpoint for Recommendations
@app.post("/recommend")
def recommend_movies(request: RecommendationRequest):
    try:
        recommended_movies = get_similar_movies(request.user_input)
        return {"recommendations": recommended_movies}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

print("✅ API is running on http://127.0.0.1:8002")
