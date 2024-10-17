from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import re  # Import the regular expression module

app = Flask(__name__)
CORS(app, resources={r"/generate": {"origins": "http://localhost:3000"}})

# Store and configure the API key
api_key = "AIzaSyAi1jAyprJ-yyjKzBFgQXoGkfORQ1avvvg"
genai.configure(api_key=api_key)

# Create an instance of the GenerativeModel using a model like "gemini-1.5-flash"
model = genai.GenerativeModel("gemini-1.5-flash")

@app.route('/generate', methods=['POST'])
def generate_content():
    data = request.json
    print(data)
    prompt = data.get('prompt', '')

    print("Received prompt:", prompt)

    # Modify the prompt to guide the model to generate related queries
    enhanced_prompt = f"Provide strictly three possible user queries very short and direct related to '{prompt}'"

    try:
        # Make request to generate related suggestions
        response = model.generate_content(enhanced_prompt)
        print(response.text)

        # Extract suggestions from the response text
        if response.candidates and len(response.candidates) > 0:
            # Access the text directly
            generated_text = response.text
            
            # Split the string by newline to create an array of suggestions
            suggestions = [line.strip() for line in generated_text.split('\n') if line.strip()]
            
            # Clean suggestions: remove numbering using regex
            cleaned_suggestions = [re.sub(r'^\d+\.\s*', '', suggestion) for suggestion in suggestions]

            # Take up to the first three cleaned suggestions
            suggestions_list = cleaned_suggestions[:3]
            
            return jsonify({'suggestions': suggestions_list}), 200
        else:
            return jsonify({'error': 'No valid content was returned. Please adjust your prompt or try again.'}), 400
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': 'An error occurred while processing your request.'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4500)
