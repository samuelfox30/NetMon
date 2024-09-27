from scapy.all import sniff

def processa_pacote(pacote):
    if pacote.haslayer('IP'):
        ip_origem = pacote['IP'].src
        ip_destino = pacote['IP'].dst
        protocolo = pacote.proto
        tamanho_pacote = len(pacote)

        print(f'Pacote: ip_origem: {ip_origem}, ip_destino: {ip_destino}, protocolo: {protocolo}, tamanho: {tamanho_pacote}')

""" sniff(prn=processa_pacote, filter="ip", store=0) """
sniff(prn=processa_pacote, filter="ip", store=0, iface="Wi-Fi")
# test