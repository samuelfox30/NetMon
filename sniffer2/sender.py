import socketio

# Criando o cliente Socket.IO
sio = socketio.Client()


######### CALL BACK #########

# Isso é só um callback, que no caso identifica quando uma conexão ocorre. E então, quando ela ocorre, acontece o que ta dentro da função
@sio.event
def connect():
    print('Conectado ao servidor!')

# O mesmo vale para essa função
@sio.event
def disconnect():
    print('Desconectado do servidor!')

def handle_message(msg):
    print(f'Mensagem do servidor: {msg}')

######### EVENTS #########

# Conectar ao servidor
sio.connect('http://localhost:5000')  # Altere o endereço se o servidor estiver em outra máquina

# Enviando dados para o servidor
sio.emit('numero', 'Olá, servidor!')

# Aguarda alguns segundos para garantir que os eventos sejam processados
import time
time.sleep(2)

# Fechar a conexão
sio.disconnect()
