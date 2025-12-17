import os
from pathlib import Path

def setup_shl_project():
    # Define the core folders
    folders = [
        "data/raw",          # For raw scraped data
        "data/processed",    # For the final 377+ items CSV
        "src/scraper",       # Crawling logic
        "src/recommender",   # RAG / Embedding logic
        "src/api",           # FastAPI implementation
        "src/frontend",      # Streamlit/UI code
        "notebooks",         # For Recall@K evaluation
    ]
    
    # Create folders
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        # Create an empty __init__.py so Python treats directories as packages
        Path(f"{folder}/__init__.py").touch()
    
    # Create the essential files
    essential_files = {
        "requirements.txt": "fastapi\nuvicorn\nbeautifulsoup4\nrequests\npandas\nlangchain\nlangchain-google-genai\nchromadb\npython-dotenv\nstreamlit",
        ".env": "GOOGLE_API_KEY=your_key_here\n",
        "README.md": "# SHL Assessment Recommendation System\nTask: Build a RAG-based recommender.",
        ".gitignore": "env/\n__pycache__/\n.env\n/data/raw/*",
        "main.py": "# Entry point for the API\nimport uvicorn\nfrom src.api.app import app\n\nif __name__ == '__main__':\n    uvicorn.run(app, host='0.0.0.0', port=8000)"
    }
    
    for filename, content in essential_files.items():
        with open(filename, "w") as f:
            f.write(content)
            
    print("✅ SHL Project structure created successfully!")

if __name__ == "__main__":
    setup_shl_project()