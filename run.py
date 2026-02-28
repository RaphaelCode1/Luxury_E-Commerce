import os
import sys
import argparse

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from backend.app import create_app
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Run the Flask app')
    parser.add_argument('--port', type=int, default=5000, help='Port to run the server on')
    args = parser.parse_args()
    
    app = create_app()
    
    if __name__ == '__main__':
        port = args.port
        print(f"🚀 Starting server on port {port}")
        app.run(debug=True, host='0.0.0.0', port=port)
except ImportError as e:
    print(f"Error importing: {e}")
    print("\nMake sure you're in the correct directory and have installed requirements:")
    print("pip install -r requirements.txt")
