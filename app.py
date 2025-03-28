#!/usr/bin/env python3
"""
Background Removal Server - Flask application for removing backgrounds from images.

This server provides a REST API for background removal using the BiRefNet model
and custom sky detection algorithms.

To run the server:
    python app.py [--port PORT] [--host HOST] [--debug]
"""

import os
import sys
import argparse
import logging
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import warnings

# Load environment variables from .env file if present
load_dotenv()

# Filter out FutureWarnings to suppress timm deprecation warnings
warnings.filterwarnings("ignore", category=FutureWarning)

def create_app():
    """
    Create and configure the Flask application.
    
    Returns:
        Flask application instance
    """
    # Initialize Flask app
    app = Flask(__name__)
    
    # Enable CORS
    CORS(app)
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    
    app.logger.info("Initializing Background Removal Server...")
    
    # Load model
    try:
        from models.birefnet_model import birefnet_model
        if birefnet_model is not None:
            app.logger.info("✅ BiRefNet model loaded successfully")
        else:
            app.logger.warning("⚠️ BiRefNet model could not be loaded, will use fallback method")
    except Exception as e:
        app.logger.error(f"❌ Error loading BiRefNet model: {str(e)}")
        app.logger.warning("⚠️ Will use fallback method for background removal")
    
    # Register blueprints
    from routes import register_routes
    register_routes(app)
    
    app.logger.info("✅ Server initialization complete")
    
    return app

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Background Removal Server")
    
    parser.add_argument("--port", type=int, default=int(os.environ.get("PORT", 5000)),
                        help="Port to run the server on (default: 5000 or PORT env var)")
    parser.add_argument("--host", type=str, default=os.environ.get("HOST", "0.0.0.0"),
                        help="Host to bind the server to (default: 0.0.0.0 or HOST env var)")
    parser.add_argument("--debug", action="store_true",
                        help="Run server in debug mode")
    
    return parser.parse_args()

if __name__ == "__main__":
    # Parse command line arguments
    args = parse_arguments()
    
    # Create the Flask app
    app = create_app()
    
    # Print startup message
    print(f"""
    ======================================================
    📷 Background Removal Server
    ======================================================
    🌐 Server running at: http://{args.host}:{args.port}
    🔧 Debug mode: {'✅ Enabled' if args.debug else '❌ Disabled'}
    🛠️  Press Ctrl+C to stop the server
    ======================================================
    """)
    
    # Run the server
    app.run(host=args.host, port=args.port, debug=args.debug)
