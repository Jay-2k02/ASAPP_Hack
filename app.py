from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

def calculate(msg):
    return str(int(msg)**2)

@socketio.on('message')
def handle_message(msg):
    print(f"Received message: {msg}")  # Log the message to the server console
    ans = calculate(msg)
    send(ans, broadcast=True)  # Broadcast the message to all connected clients

if __name__ == '__main__':
    socketio.run(app)
