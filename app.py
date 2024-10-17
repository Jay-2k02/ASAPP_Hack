from flask import Flask, render_template, request, jsonify
from processInputQuery import getFinalAnswer
from chunkPapers import collection_create
from query_db import getTopChunks
from query_db import gemini
import os
app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('index.html')

uploaded_file = []
UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/api/chat',methods=['POST'])
def chatbot():
    data = request.get_json()
    query = data.get('prompt')
    response = getFinalAnswer(query)
    return jsonify({"response":response})


@app.route('/api/uploadchat',methods=['POST'])
def uploadchat():
    data = request.get_json()
    query = data.get('prompt')
    topChunks =  getTopChunks(query,uploaded_file[-1])
    finalResult = gemini(query, topChunks)
    return jsonify({"response":finalResult})

#upload pdf
@app.route('/api/upload',methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']

    # Check if the user has selected a file
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Check if the file is a PDF
    if file and file.filename.endswith('.pdf'):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        collection_name  = f"Uploaded-{file.filename}"
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        uploaded_file.append(collection_name)
        collection_create(pdf_path,collection_name)

# def calculate(msg):
#     return str(int(msg)**2)

# @socketio.on('message')
# def handle_message(msg):
#     print(f"Received message: {msg}")  # Log the message to the server console
#     ans = calculate(msg)
#     send(ans, broadcast=True)  # Broadcast the message to all connected clients

if __name__ == '__main__':
     app.run(host='127.0.0.1',port=4444)
