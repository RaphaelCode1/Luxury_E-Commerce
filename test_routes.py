from flask import Flask, render_template_string

app = Flask(__name__, 
           template_folder='frontend/templates',
           static_folder='frontend/static')

@app.route('/')
def index():
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head><title>Test</title></head>
        <body>
            <h1>✅ Flask is working!</h1>
            <p>Your templates are at: frontend/templates/</p>
            <p><a href="/auth/login">Go to Login</a></p>
        </body>
        </html>
    ''')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
