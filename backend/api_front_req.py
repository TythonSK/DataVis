# backend/api_front_req.py
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend (localhost:3000)

# Root route, this can be useful if you want to visit http://localhost:5000
@app.route('/')
def home():
    return "Welcome to the Flask Backend!"  # Or whatever message you'd like

@app.route('/api/data', methods=['GET'])
def get_data():
    # Example response data
    data = {'message': 'Hello from Python Flask Backend!'}
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Flask runs on http://localhost:5000
