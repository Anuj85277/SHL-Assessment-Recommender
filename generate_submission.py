import pandas as pd
from src.recommender.engine import SHLRecommender

recommender = SHLRecommender()
test_queries = [
    "Query 1 from your test set", 
    "Query 2 from your test set",
    # ... add all 9 queries here
]

submission_data = []

for query in test_queries:
    results = recommender.recommend(query, n=10) # Get max 10
    for rec in results:
        submission_data.append({
            "Query": query,
            "Assessment_url": rec['url']
        })

df = pd.DataFrame(submission_data)
df.to_csv("test_predictions.csv", index=False)
print("File saved as test_predictions.csv")