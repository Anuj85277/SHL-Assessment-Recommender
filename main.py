from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import os
import sys

sys.path.append(os.path.join(os.getcwd(), "src"))

try:
    from recommender.engine import SHLRecommender
except ImportError:
    from src.recommender.engine import SHLRecommender

app = FastAPI(
    title="SHL Assessment Recommender API",
    description="API to recommend SHL assessments based on job roles or skills.",
    version="1.0.0"
)

recommender = SHLRecommender()

class RecommendRequest(BaseModel):
    query: str
    n: int = 5

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/recommend")
def get_recommendations(request: RecommendRequest):
    results = recommender.recommend(request.query, n=request.n)

    return {
        "query": request.query,
        "total_returned": len(results),
        "recommendations": results
    }

@app.get("/")
def read_root():
    return {
        "status": "online",
        "message": "SHL Recommender API is active",
        "documentation": "/docs"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
