import os
import argparse
from waitress import serve
from dotenv import load_dotenv
from app import app

# Create an argument parser
parser = argparse.ArgumentParser()
parser.add_argument('--env', help='Environment mode (local, production, etc.)', required=True, choices=['local', 'production'])

# Parse the command-line arguments
args = parser.parse_args()

# Load the .env file based on FLASK_ENV
load_dotenv(f"env-variables/.env.{args.env}")

if __name__ == "__main__":
    if os.getenv("CB_ENV") == 'production':
        serve(app, host='0.0.0.0', port=os.getenv("CB_PORT"), threads=1)
    else:
        app.run(port=os.getenv("CB_PORT"), debug=os.getenv('CB_DEBUG', '').lower() == 'true')
