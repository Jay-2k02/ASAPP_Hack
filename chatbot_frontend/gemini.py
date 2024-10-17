from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

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
    print (data)
    prompt = data.get('prompt', '')

    print ("hi")
    print (prompt)
    # Make request to generate text
    response = model.generate_content(prompt)
    print (response)
    # Extract the text content safely
    if response.candidates and len(response.candidates) > 0:
        generated_content = response.text
        return jsonify({'content': str(generated_content)}), 200
    else:
        return jsonify({'error': 'No valid content was returned. Please adjust your prompt or try again.'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
