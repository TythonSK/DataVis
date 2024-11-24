import os
import openai
from dotenv import load_dotenv

# Načítanie hodnôt z ..env súboru
load_dotenv()

# Načítanie API kľúča z prostredia
api_key = os.getenv('OPENAI_API_KEY')

if not api_key:
    raise ValueError("API kľúč nie je nastavený v premennej prostredia 'OPENAI_API_KEY'")

class ChatWithGPT:
    def __init__(self):
        # Initialize the OpenAI client
        openai.api_key = api_key

    def get_response(self, user_query):
        try:
            # Initialize the OpenAI client and make a request
            client = openai.Client(api_key=api_key)
            stream_1 = client.chat.completions.create(
            # stream_1 = openai.ChatCompletion.create(
                model="gpt-4",  # Use the appropriate GPT model
                messages=[{"role": "user", "content": user_query}],
                stream=True
            )

            # Process the response stream and build the response text
            response_text = ""
            for chunk in stream_1:
                content = chunk.choices[0].delta.content  # Extract content
                if content:  # Check if content is not None
                    response_text += content

            # Print the response for debugging
            print(f"AI Response: {response_text}")

            return response_text
        except Exception as e:
            print(f"Error: {str(e)}")  # Log the error if one occurs
            return f"Error: {str(e)}"

