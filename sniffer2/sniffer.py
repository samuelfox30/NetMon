from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chave_secreta'
socketio = SocketIO(app)

@app.route('/')
def index():
    return "Servidor On"

@socketio.on('connect')
def on_connect():
    print('Cliente conectado.')

@socketio.on('disconnect')
def on_disconnect():
    print('Cliente desconectado.')

@socketio.on('mensagem')