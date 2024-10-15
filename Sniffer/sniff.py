# Importando a biblioteca Scapy
import scapy.all as scapy

# Função em que os pacotes são processados para a exibição
def sniffed_packet(packet):
    # Verifica se o pacote tem a camada Ethernet
    if packet.haslayer(scapy.Ether):
        mac_origem = packet[scapy.Ether].src
        mac_destino = packet[scapy.Ether].dst
        print(f"MAC Origem: {mac_origem}, MAC Destino: {mac_destino}")

    # Verifica se o pacote tem a camada IP
    if packet.haslayer(scapy.IP):
        ip_versao = "IPv4"
        ip_origem = packet[scapy.IP].src
        ip_destino = packet[scapy.IP].dst
        print(f"Versão IP: {ip_versao}, IP Origem: {ip_origem}, IP Destino: {ip_destino}")
    
    # Verifica se o pacote tem a camada IPv6
    elif packet.haslayer(scapy.IPv6):
        ip_versao = "IPv6"
        ip_origem = packet[scapy.IPv6].src
        ip_destino = packet[scapy.IPv6].dst
        print(f"Versão IP: {ip_versao}, IP Origem: {ip_origem}, IP Destino: {ip_destino}")

    # Verifica se o pacote tem a camada TCP
    if packet.haslayer(scapy.TCP):
        porta_origem = packet[scapy.TCP].sport
        porta_destino = packet[scapy.TCP].dport
        print(f"Protocolo: TCP, Porta Origem: {porta_origem}, Porta Destino: {porta_destino}")

    # Verifica se o pacote tem a camada UDP
    elif packet.haslayer(scapy.UDP):
        porta_origem = packet[scapy.UDP].sport
        porta_destino = packet[scapy.UDP].dport
        print(f"Protocolo: UDP, Porta Origem: {porta_origem}, Porta Destino: {porta_destino}")

    # Identificação do protocolo da camada de aplicação, caso exista
    if packet.haslayer(scapy.Raw):
        protocolo_aplicacao = "Protocolo de Aplicação: Dados brutos"
        print(protocolo_aplicacao)

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
    sniffer("Wi-Fi")

# Verificando se o arquivo está sendo executado ou importado
if __name__ == '__main__':
    main()
