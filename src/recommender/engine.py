import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

class SHLRecommender:
    def __init__(self, csv_path="data/processed/shl_catalog.csv"):
        self.csv_path = csv_path
        print("🚀 Initializing Emergency High-Stability Engine...")
        self.df = None
        self.load_data()

    def load_data(self):
        if not os.path.exists(self.csv_path):
            print(f"❌ CSV not found at {self.csv_path}")
            return
        self.df = pd.read_csv(self.csv_path)
        print(f"✅ Loaded {len(self.df)} assessments via Pandas.")

    def recommend(self, query, n=5):
        if self.df is None: return []
        
        # Simple but effective keyword matching to mimic semantic search
        query_words = query.lower().split()
        
        def calculate_score(row):
            text = f"{row['assessment_name']} {row['description']}".lower()
            return sum(1 for word in query_words if word in text)

        temp_df = self.df.copy()
        temp_df['score'] = temp_df.apply(calculate_score, axis=1)
        
        # Filter for relevant results and sort
        results = temp_df[temp_df['score'] > 0].sort_values(by='score', ascending=False)
        
        # If no keywords match, just give the top rows
        if results.empty:
            results = temp_df.head(20)

        # Balancing Logic (Knowledge vs Personality)
        k_list = results[results['test_type'] == 'K'].to_dict('records')
        p_list = results[results['test_type'] == 'P'].to_dict('records')
        
        # Create balanced list
        balanced = k_list[:n//2] + p_list[:(n - len(k_list[:n//2]))]
        
        # Fill if short
        if len(balanced) < n:
            existing_names = [b['assessment_name'] for b in balanced]
            for _, row in results.iterrows():
                if row['assessment_name'] not in existing_names and len(balanced) < n:
                    balanced.append(row.to_dict())

        return [{"name": b['assessment_name'], "url": b['url']} for b in balanced]

if __name__ == "__main__":
    rec = SHLRecommender()
    print("\n🔍 Testing Query: 'Java Developer'...")
    results = rec.recommend("Java Developer", n=5)
    for i, res in enumerate(results, 1):
        print(f"{i}. {res['name']} ({res['url']})")