"""FastAPI application entry point for incident-commander-openenv.

This module wraps the main FastAPI application and serves as the deployment
entry point for multi-mode deployment to Hugging Face Spaces and other platforms.
"""

from api.main import app

# Export the application instance for uvicorn and ASGI servers
__all__ = ["app"]

if __name__ == "__main__":
    import uvicorn
    
    # Run the server with production settings
    uvicorn.run(
        "server.app:app",
        host="0.0.0.0",
        port=7860,
        reload=False,
        access_log=True,
    )
