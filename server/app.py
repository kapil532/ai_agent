"""FastAPI application entry point for incident-commander-openenv.

This module wraps the main FastAPI application and serves as the deployment
entry point for multi-mode deployment to Hugging Face Spaces and other platforms.
"""

import uvicorn
from api.main import app


def main() -> None:
    """Run the FastAPI server for incident-commander-openenv.
    
    This is the main entry point for the application when deployed via
    multi-mode deployment or directly invoked from the command line.
    """
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=7860,
        log_level="info",
    )


if __name__ == "__main__":
    main()
