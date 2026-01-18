"""
Flask application entry point
Run with: python run.py
"""

import os
import sys
from app import create_app, logger
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create Flask app
try:
    app = create_app()
    logger.info("✅✅✅ Flask app created successfully ✅✅✅")
except Exception as e:
    logger.error(f"❌ Failed to create app: {str(e)}")
    sys.exit(1)

if __name__ == '__main__':
    try:
        logger.info("🚀 Starting Flask server...")
        logger.info("🌐 Server will run on http://0.0.0.0:5000")
        logger.info("🌐 Frontend should connect to http://localhost:5000/api")
        logger.info("📝 Check logs/app.log for detailed information")
        
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True,
            use_reloader=False  # Set to False if auto-reload causes model issues
        )
    except Exception as e:
        logger.error(f"❌ Failed to start server: {str(e)}")
        sys.exit(1)
