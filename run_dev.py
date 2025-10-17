#!/usr/bin/env python3
"""
Development server startup script
"""
import uvicorn
import os
from pathlib import Path

def main():
    """Start the development server"""
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Set up development environment
    os.environ.setdefault("ENVIRONMENT", "development")
    
    print("Starting SecureLLM API server...")
    print("API Documentation: http://localhost:8000/docs")
    print("Alternative docs: http://localhost:8000/redoc")
    
    # Start the server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Enable auto-reload for development
        log_level="info"
    )

if __name__ == "__main__":
    main()