from flask import Flask, render_template, request, jsonify
from flask_cors import CORS  # Import CORS
from processInputQuery import getFinalAnswer

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)  # This will allow all origins by default

# If you want to specify allowed origins, you can do it like this:
# CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

@app.route('/api/chat', methods=['POST'])
def chatbot():
    data = request.get_json()
    query = data.get('prompt')
    response = getFinalAnswer(query)
    return jsonify({"response": response})

# Uncomment if you have an index.html to render
# @app.route('/')
# def index():
#     return render_template('index.html')

# def calculate(msg):
#     return str(int(msg)**2)

# @socketio.on('message')
# def handle_message(msg):
#     print(f"Received message: {msg}")  # Log the message to the server console
#     ans = calculate(msg)
#     send(ans, broadcast=True)  # Broadcast the message to all connected clients

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=4444)
