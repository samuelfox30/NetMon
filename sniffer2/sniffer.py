# SERVER CONNECTION IMPORTS
from flask import Flask
from flask_socketio import SocketIO
import socketio

# SNIFFER IMPORTS
import scapy.all as scapy
from dotenv import load_dotenvxxxxxx
import os
import requests  # Biblioteca para fazer requisições HTTP em Python
import json  # Para converter os dados em JSON
import socketio

# TESTE
import threading

################################################################################################################################################

#----------JUST CUSE IT NEED TO BE HERE----------#

load_dotenv() # Carregando as variaveis de ambiente
# Obtendo a URL do endpoint e o ID do usuário a partir das variáveis de ambiente
endpoint_url = os.getenv("ENDPOINT_URL")
# Obtém o ID do usuário
user_id = os.getenv("ID_USER")
sio = socketio.Client()
sio.connect(endpoint_url)

on_or_off = True

def verification(value='none'):
    global on_or_off
    if value == 'none':
        return on_or_off    
    else:
        on_or_off = value
        return on_or_off

################################################################################################################################################

#----------CALL BACK----------#

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chave_secreta'
socketio = SocketIO(app)

@socketio.on('connect')
def on_connect():
    print('Cliente conectado.')

@socketio.on('disconnect')
def on_disconnect():
    print('Cliente desconectado.')

@socketio.on('stop')
def handle_message(msg='nothing'):
    print(f'Programa parado: {msg}')
    verification(False)

@socketio.on('start')
def handle_message(msg='nothing'):
    print(f'Programa iniciado: {msg}')
    verification(True)

################################################################################################################################################

#----------PROCESSADOR DE PACOTES----------#

def sniffed_packet(packet):
    data = {}

    # Verifica se o pacote tem a camada Ethernet
    if packet.haslayer(scapy.Ether):
        data['mac_origem'] = packet[scapy.Ether].src
        data['mac_destino'] = packet[scapy.Ether].dst

    # Verifica se o pacote tem a camada IPv4
    if packet.haslayer(scapy.IP):
        data['ip_versao'] = "IPv4"
        data['ip_origem'] = packet[scapy.IP].src
        data['ip_destino'] = packet[scapy.IP].dst
    
    # Verifica se o pacote tem a camada IPv6
    elif packet.haslayer(scapy.IPv6):
        data['ip_versao'] = "IPv6"
        data['ip_origem'] = packet[scapy.IPv6].src
        data['ip_destino'] = packet[scapy.IPv6].dst

    # Verifica se o pacote tem a camada TCP
    if packet.haslayer(scapy.TCP):
        data['protocolo'] = "TCP"
        data['porta_origem'] = packet[scapy.TCP].sport
        data['porta_destino'] = packet[scapy.TCP].dport

    # Verifica se o pacote tem a camada UDP
    elif packet.haslayer(scapy.UDP):
        data['protocolo'] = "UDP"
        data['porta_origem'] = packet[scapy.UDP].sport
        data['porta_destino'] = packet[scapy.UDP].dport

    # Verifica se contém alguma dessas portas
    if data.get('porta_destino') == 80:
        data['data_status'] = "HTTP"
    if data.get('porta_destino') == 443:
        data['data_status'] = "HTTPS"
    if data.get('porta_destino') == 21:
        data['data_status'] = "FTP"
    if data.get('porta_destino') == 25:
        data['data_status'] = "SMTP"
    if data.get('porta_destino') == 110:
        data['data_status'] = "POP3"
    if data.get('porta_destino') == 53:
        data['data_status'] = "DNS"

    # Identificação do protocolo da camada de aplicação, caso exista
    if packet.haslayer(scapy.Raw):
        data['data_status'] = "Have"
        if data.get('porta_destino') == 80 or data.get('porta_destino') == 25 or data.get('porta_destino') == 21:
            try:
                data['payload'] = packet[scapy.Raw].load.decode(errors='ignore')
            except Exception as e:
                data['payload'] = f"Error: {e}"
    else:
        data['data_status'] = "DontHave"  

    # Incluindo o ID do usuário nos dados
    data['id_usuario'] = user_id

    # Envia os dados para o endpoint PHP via POST
    if endpoint_url:  # Verifica se a variável ENDPOINT_URL foi definida
        try:
            # Enviando a mensagem do pacote
            sio.emit('pacote', data)
            # Printando
            #print(f"Dados enviados: {data}")
        except Exception as e:
            print(f"Erro ao enviar os dados: {e}")
    else:
        print("Erro: A variável ENDPOINT_URL não foi definida no arquivo .env.")

    #print("\n" + "-"*50 + "\n")

################################################################################################################################################

#----------APENAS FAZ FUNCIONAR----------#

def sniffer(interface):
    
    '''
    - O parametro 1 indica a interface de rede que deseja monitorar, 
    - O parametro 2 indica que o programa não deve armazenar nada na memória referente a captura de pacotes,
    - O parametro 3 chama a função que irá processar os pacotes capturados.
    '''
    
    scapy.sniff(iface=interface, store=False, prn=sniffed_packet, stop_filter=lambda x: not verification())

################################################################################################################################################

#----------MAIN É MAIN----------#

def main():

    # Inicia o servidor SocketIO em uma thread separada
    server_thread = threading.Thread(target=lambda: socketio.run(app, host='0.0.0.0', port=5000))
    server_thread.daemon = True  # Permite encerrar a thread quando o programa principal terminar
    server_thread.start()

    interface = os.getenv("INTERFACE")  # Definindo a interface usada baseando-se nos dados do arquivo .env
    if interface:
        # Chama o sniffer na thread principal
        sniffer(interface)
    else:
        print("Erro: A variável INTERFACE não foi definida no arquivo .env.")

################################################################################################################################################

if __name__ == '__main__':
    main()