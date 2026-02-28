# Luxury E-Commerce - Windows Setup Instructions

## Prerequisites
- Python 3.8 or higher installed
- MySQL installed (optional, SQLite works for development)

## Setup Steps

1. **Extract the project folder**

2. **Open Command Prompt or PowerShell** in the project folder

3. **Run the setup script:**

4. **Activate virtual environment** (if not already):

5. **Run the application:**

6. **Open browser** and go to:
http://localhost:5000

## Troubleshooting

### If you get "mysqlclient" errors:
- Install MySQL Connector: https://dev.mysql.com/downloads/connector/python/
- Or use SQLite (change DATABASE_URL in .env)

### If Flask-Login errors persist:
- Run the fix script manually:

### If port 5000 is in use:
- Edit run.py and change port number

## Default Admin Credentials
- Email: admin@luxurytime.com
- Password: admin123

## Project Structure
- `/frontend/templates` - HTML files
- `/frontend/static` - CSS, JS, images
- `/backend` - Python backend code
- `/database` - Database files
