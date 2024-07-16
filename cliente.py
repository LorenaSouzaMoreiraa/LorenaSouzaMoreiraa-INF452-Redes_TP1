# 108204 - Lorena Souza Moreira
import socket
import select
import time
import system

#cores
def RED(msg: str) -> str: 
    return f'\033[31m{msg}\033[m'

def YELLOW(msg: str) -> str: 
    return f'\033[33m{msg}\033[m'

def GREEN(msg: str) -> str: 
    return f'\033[32m{msg}\033[m'

def BLUE(msg: str) -> str: 
    return f'\033[36m{msg}\033[m'

def options():
    print(BLUE("___MENU___"))
    print("Inbox: /list")
    print("Entrar em um chat:/chat <nome_de_usuário>")      
    print("Enviar mensagem:/msg <mensagem>")             
    print("Encerrar chat:/bye")        
    print("Desonline:/fim")

HOST = '200.235.131.66'          #Endereco IP do servidor
PORT = 5000                 #Porta que o servidor esta
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (HOST,PORT)
tcp.conect(dest)

tcp.send('USER lolo:18204\r\n'.encode())
t = time.time()

options()

msg = ''
chat = {}
current = ''

while msg != '/fim':
    #A A A Staying alive, staying alive
    if time.time() - t > 5.00:
        t = time.time()
        tcp.send('KEEP\r\n'.encode())
        
    msg = input()
    
    inbox, _ , _ = select.select(list([x['sockets'] for x in chats.values()]),[],[],0.1)

    unread = 0
    for peer in inbox:
        text = tcp.recv(1024).decode()
        try:
            if peer == chat[current]['socket']:
                print(f'[{time:time()}]: ',text.decode())
            else:
                chat[current]['new'] +=1
               
            chat[current]['backup'].append(f'[{time:time()}]',current,': ',text.decode() )
        except Exception as ex:
            print(RED("<<Alert!>>"))
            print(ex)

    if msg[:4] == "/fim":
        if len(friends)==0:
            break
        #verifica papos
        #desonline

    elif msg[:5] == "/list":
        tcp.send('LIST\r\n'.encode())
        print(BLUE('___INBOX___'))
        try:
            resp = tcp.recv(1024).decode()
            for friend in resp[5:].split(':'):
                if chat[friend]['new'] > 0:
                    print(GREEN(friend,'    ', [friend]['new']))
                else:
                    print(friend)
            print(YELLOW("<- Visualizar MENU: /menu"))
        except Exception as ex:
            print(RED("<<Alert!>>"))
            print(ex)

    elif msg[:5] == "/chat":
        #chat ja foi iniciado
        if chat.get(msg[6:]):
            current = msg[6:]
            system('cls')
            print(YELLOW("<- Visualizar MENU: /menu"))
            print(GREEN('<Chat com ', msg[6:],'>'))
            print(YELLOW("<- Visualizar INBOX: /list"))
            for pos,text in enumerate(chat[msg[6:]]['backup']):
                if pos == len(chat[msg[6:]]['backup'])-chat[msg[6:]]['new']-1:
                    print(GREEN('-----Novas mensagens------'))
                print(text)
            chat[msg[6:]]['new'] = 0
        #nao ha chat
        else:
            tcp.send(f'ADDR {msg[6:]}\r\n'.encode())
            resp = tcp.recv(1024).decode()
            try:
                chat[msg[6:]]["socket"] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                chat[msg[6:]]["socket"].connect(resp.split(':')[0][5:],resp.split(':')[1])
                chat[msg[6:]]['backup'] = {}
                chat[msg[6:]]['new'] = 0
                current = msg[6:]
                print(YELLOW("<- Visualizar MENU: /menu"))
                print(GREEN('<Chat com ', msg[6:],' >'))
                print(YELLOW("<- Visualizar INBOX: /menu"))
            except Exception as ex:
                print(RED("<<Alert!>>"))
                print(ex)

    elif msg[:4] == "/bye":
        current = ''
        tcp.send(f'DISC\r\n'.encode())
        system('cls')
        options()
    
    elif msg[:4] == "/msg":
        tcp.send(msg[:5].encode())
        chat[msg[:5]]['backup'].append(f'[{time:time()}]: ',text.decode())

    elif msg[:5] == "/menu":
        current = ''
        system('cls')
        options()

    else:
        print(YELLOW('Nao entendi. Poderia repetir?'))
    
tcp.close() 