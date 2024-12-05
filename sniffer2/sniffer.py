from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chave_secreta'
socketio = SocketIO(app)

@socketio.on('connect')
def on_connect():
    print('Cliente conectado.')

@socketio.on('disconnect')
def on_disconnect():
    print('Cliente desconectado.')

@socketio.on('mensagem')
def handle_message(msg):
    print(f'Mensagem recebida: {msg}')
    socketio.send(f'Recebi a mensagem: {msg}')

@socketio.on('numero')
def handle_message(msg):
    print(f'Numero recebido: {msg}')
    socketio.send(f'Recebi o numero: {msg}')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)