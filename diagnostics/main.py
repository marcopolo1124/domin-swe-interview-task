from flask import Flask, render_template
import socketio
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True
socketio = SocketIO(app)

@app.route("/")
def hello_world():
    return render_template("index.html")

@socketio.on("connect")
def handle_connect():
    print("Client connected")
    
@socketio.on("data")
def handle_data(data):
    socketio.emit("new", data)
    
if __name__ == '__main__':
    socketio.run(app, port=5000)