from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from pokus_stevo import ChatWithGPT  # Import the class from the other file

# Load environment variables from the ..env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for communication with the frontend

# Initialize the ChatWithGPT class
chat_gpt = ChatWithGPT()

@app.route('/')
def home():
    return "Welcome to the Flask Backend!"

@app.route('/api/ai', methods=['POST'])
def chat_with_gpt():
    """Endpoint to handle AI queries."""
    try:
        # Capture the JSON data sent from the frontend
        data = request.get_json()

        # Print the incoming request data to the terminal
        print(f"Data received from frontend: {data}")

        # Get the user query from the data (assuming it has a 'query' field)
        user_query = data.get('query', '')

        if not user_query:
            return jsonify({'error': 'Query not provided'}), 400

        # Use the ChatWithGPT class to get a response for the query
        response_text = chat_gpt.get_response(user_query)

        # Print the response text for debugging
        print(f"Response from GPT: {response_text}")

        # Return the processed response to the frontend
        return jsonify({'response': response_text})

    except Exception as e:
        # Print the error for debugging
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
