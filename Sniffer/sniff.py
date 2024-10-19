# Importando as bibliotecas necessárias
import scapy.all as scapy
from dotenv import load_dotenv
import os
import requests  # Biblioteca para fazer requisições HTTP em Python
import json  # Para converter os dados em JSON

# Carregando as variáveis do arquivo .env
load_dotenv()

# Função em que os pacotes são processados para a exibição e envio
def sniffed_packet(packet):
    data = {}

    # Verifica se o pacote tem a camada Ethernet
    if packet.haslayer(scapy.Ether):
        data['mac_origem'] = packet[scapy.Ether].src
        data['mac_destino'] = packet[scapy.Ether].dst

    # Verifica se o pacote tem a camada IP
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

    # Identificação do protocolo da camada de aplicação, caso exista
    if packet.haslayer(scapy.Raw):
        data['data_status'] = "Contém [Dados brutos]"
        if data.get('porta_destino') == 80:
            data['data_status'] = "Pacote HTTP"
            try:
                data['payload'] = packet[scapy.Raw].load.decode(errors='ignore')
            except Exception as e:
                data['payload'] = f"Error: {e}"
    else:
        data['data_status'] = "Não contém [Dados brutos]"

    # Obtendo a URL do endpoint e o ID do usuário a partir das variáveis de ambiente
    endpoint_url = os.getenv("ENDPOINT_URL")
    user_id = os.getenv("ID_USER")  # Obtém o ID do usuário

    # Incluindo o ID do usuário nos dados
    data['id_usuario'] = user_id

    # Envia os dados para o endpoint PHP via POST
    if endpoint_url:  # Verifica se a variável ENDPOINT_URL foi definida
        try:
            response = requests.post(endpoint_url, json=data)
            print(f"Dados enviados: {data}")
            print(f"Resposta do servidor: {response.json()}")
        except Exception as e:
            print(f"Erro ao enviar os dados: {e}")
    else:
        print("Erro: A variável ENDPOINT_URL não foi definida no arquivo .env.")

    print("\n" + "-"*50 + "\n")

# Função em que ocorre a captura dos pacotes
def sniffer(interface):
    '''
    - O parametro 1 indica a interface de rede que deseja monitorar, 
    - O parametro 2 indica que o programa não deve armazenar nada na memória referente a captura de pacotes,
    - O parametro 3 chama a função que irá processar os pacotes capturados.
    '''
    scapy.sniff(iface=interface, store=False, prn=sniffed_packet)

# Função principal
def main():
    # Pegando a interface de rede a partir do arquivo .env
    interface = os.getenv("INTERFACE")
    
    if interface:
        # Chama o sniffer com a interface definida no arquivo .env
        sniffer(interface)
    else:
        print("Erro: A variável INTERFACE não foi definida no arquivo .env.")

# Verificando se o arquivo está sendo executado ou importado
if __name__ == '__main__':
    main()
