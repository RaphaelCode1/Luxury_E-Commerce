from flask import Flask, jsonify
from backend.models import db
from backend.utils.helpers import generate_order_number

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SECRET_KEY'] = 'test-key'
db.init_app(app)

@app.route('/')
def index():
    return jsonify({
        'message': 'API is working',
        'test_order_number': generate_order_number()
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    print("Test order number:", generate_order_number())
    app.run(debug=True, port=5000)
