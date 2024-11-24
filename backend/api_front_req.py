from flask import Flask, request, jsonify
from flask_cors import CORS
from analyza_datasetu import process_question  

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend-backend communication

@app.route('/')
def home():
    return "Welcome to the AI Data Explorer API!"

@app.route('/api/ai', methods=['POST'])
def handle_query():
    """
    Endpoint to process the question submitted via the frontend.
    """
    try:
        data = request.get_json()
        print(f"Received data: {data}")

        # Extract question
        question = data.get('query')
        if not question:
            return jsonify({'error': 'Query not provided'}), 400

        # Process the question and get the response from analyza_datasetu.py
        response = process_question(question)  # Directly call the function
        return jsonify({'response': response}) 
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
