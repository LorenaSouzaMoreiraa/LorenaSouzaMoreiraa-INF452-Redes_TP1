# 108204 - Lorena Souza Moreira
import socket

# a P2P descrita acima - comunicação formato texto, onde os dois lados devem estar online ao mesmo tempo. 
# Para se obter as informações necessárias para estabelecimento da comunicação, um segundo programa será 
# criado para funcionar como um servidor centralizado.
# Você deverá implementar o protocolo de aplicação descrito a seguir utilizando sockets

# O servidor central estará constantemente escutando a porta 10000 para que cada cliente possa estabelecer uma conexão
# TCP para enviar/receber informações para/do o servidor
# cada cliente deverá escutar alguma outra porta (não especificada pelo protocolo)
# receber conexões de outro -> uma mensagem para informar ao servidor central qual porta estará aberta 
# primeiro, perguntar ao servidor qual a porta a ser utilizada (além do endereço IP)


HOST = '200.235.131.66'          #Endereco IP do servidor
PORT = 10000        #Porta que o servidor esta

def conectado(con,cliente):
    
    print("Conectado por", cliente)
    while True:
        msg = con.recv(1024).decode
        if msg == "/fim":
            break
        print(cliente, msg)
    
    print("Finalizando conexao com cliente", cliente)
    con.close()
    return


tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.setsockopt(socket.SQL_SOCKET, socket.SO_REUSEADDR, 1)
orig = (HOST,PORT)
tcp.bind(orig)
tcp.listen(1)
 

while True:
    try:
        con, cliente = tcp.accept()      
        print('Requisitando conexão:', cliente)
        while True:
            msg = con.recv(1024).decode() 
            if msg == "/fim":
                break
            print(cliente, msg)
        print("Finalizando conexão do cliente", cliente)
        con.close()
    except Exception as ex:
        print("Alert:")
        print(ex)

tcp.close() 