#!/bin/bash
echo "Setting up Luxury E-Commerce..."

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Fix Flask-Login issue
python fix_flask_login.py

echo "Setup complete!"
echo "To run the application:"
echo "1. source venv/bin/activate"
echo "2. python run.py"
