# Importando a biblioteca Scapy
import scapy.all as scapy


# Função em que ocorre a captura dos pacotes
'''
- O parametro 1 indica a interface de rede que deseja monitorar, 
- O parametro 2 indica que o programa não deve armazenar nada na memória referente a captura de pacotes,
- O parametro 3 indica chama a função que irá processar os pacotes capturados por esse função.
'''
def sniffer(interface):
    scapy.sniff(iface=interface, store=False, prn=sniffed_packet)

# Função em que os pacotes são processados para a exibição
def sniffed_packet(packet):
        print(packet)


# Definindo uma função principal
def main():
    sniffer("Ethernet")

# Verificando se o arquivo está sendo executado ou importado e, caso executado, chama a função main()
if __name__ == '__main__':
    main()