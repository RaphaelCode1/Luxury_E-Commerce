import os
import re

# Find the flask_login installation
flask_login_path = None
for root, dirs, files in os.walk('venv'):
    if 'flask_login' in root and 'utils.py' in files:
        flask_login_path = os.path.join(root, 'utils.py')
        break

if flask_login_path:
    print(f"Found flask_login at: {flask_login_path}")
    
    # Read the file
    with open(flask_login_path, 'r') as f:
        content = f.read()
    
    # Replace the import
    content = content.replace(
        'from werkzeug.urls import url_decode',
        'from werkzeug.urls import url_decode\nfrom urllib.parse import urlsplit'
    )
    
    # Also add fallback
    content = content.replace(
        'url_decode(data)',
        'url_decode(data) if hasattr(url_decode, "__call__") else data'
    )
    
    # Write back
    with open(flask_login_path, 'w') as f:
        f.write(content)
    
    print("✅ Fixed flask_login import")
else:
    print("❌ Could not find flask_login utils.py")
