import os
import sys
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

# Add backend directory to module paths
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.routes import app

# Enable CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def start_api_server():
    """Start the FastAPI server."""
    print("Starting OmniVid Backend API on http://127.0.0.1:18000")
    uvicorn.run(app, host="127.0.0.1", port=18000, log_level="info")

if __name__ == "__main__":
    start_api_server()
