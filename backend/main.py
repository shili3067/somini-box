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
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", 18000))
    print(f"Starting OmniBox Backend API on http://{host}:{port}")
    uvicorn.run(app, host=host, port=port, log_level="info")

if __name__ == "__main__":
    start_api_server()
