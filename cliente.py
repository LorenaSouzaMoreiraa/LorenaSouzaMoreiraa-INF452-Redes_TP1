# 108204 - Lorena Souza Moreira
import socket
import select
import time
import threading
import os

#cores
def RED(msg: str) -> str: 
    return f'\033[31m{msg}\033[m'

def YELLOW(msg: str) -> str: 
    return f'\033[33m{msg}\033[m'

def GREEN(msg: str) -> str: 
    return f'\033[32m{msg}\033[m'

def BLUE(msg: str) -> str: 
    return f'\033[36m{msg}\033[m'

def clear():
    if os.name == 'nt': #Win
        os.system('cls') or None
    else:
        os.system('clear') or None 

def alive(start):
    #A A A Staying alive, staying alive
    if time.time() - start >= 5.00:
        t = time.time()
        tcp.send('KEEP\r\n'.encode())

def options():
    print(BLUE("___MENU___"))
    print("Inbox:/list")
    print("Entrar em um chat:/chat <nome_de_usuário>")      
    print("Enviar mensagem:/msg <mensagem>")             
    print("Encerrar chat:/bye")        
    print("Desonline:/exit")

HOST = '200.235.131.66'          #Endereco IP do servidor
PORT = 10000                 #Porta que o servidor esta
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (HOST,PORT)
tcp.connect(dest)

tcp.send('USER lolo:18204\r\n'.encode())
options()

msg = ''
chat = {}
current = ''
unread = 0

aux = time.time()

while msg != '/exit':
    t = threading.Thread(target=alive, args=({aux}))
    t.start()

    msg  = ''
    msg = input()
    
    if len(chat)>0:
        inbox, _ , _ = select.select(list([x['socket'] for x in chat.values()]),[],[],0.1)

        for peer in inbox:
            text = peer.recv(1024)
            try:
                if peer == chat[current]['socket']:
                    print(f'[{time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())}] {current}: ',text.decode())
                    chat[current]['backup'].append(f'[{time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())}]'+current+': '+text.decode() )
                else:
                    chat[current]['new'].append(f'[{time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())}]'+current+': '+text.decode() )
                    unread +=1
            except Exception as ex:
                print(RED("<<Alert!>>"))
                print(ex)

    if msg[:5] == "/list":
        clear()
        tcp.send('LIST\r\n'.encode())
        print(BLUE('___INBOX___'))
        print(f'{unread} mensagens não lidas')
        try:
            resp = tcp.recv(1024).decode()
            for friend in resp[5:].split(':'):
                if friend in chat and chat[friend]['new']> 0:
                    value = chat[friend]['new']
                    print(BLUE(f'{friend}    {value}'))
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
            clear()
            print(YELLOW("<- Visualizar MENU: /menu"))
            print(GREEN(f'<Chat com {msg[6:]}>'))
            print(YELLOW("<- Visualizar INBOX: /list"))
            for text in chat[msg[6:]]['backup']:
                print(text)
                
            print(BLUE('-----Novas mensagens------'))
            for text in chat[msg[6:]]['new']:
                print(text)
                chat[msg[6:]]['backup'].append(text)
            unread -= len(chat[msg[6:]]['new'])
            chat[msg[6:]]['new'].clear()
            
        else:
            name = msg[6:]
            tcp.send(f'ADDR {msg[6:]}\r\n'.encode())
            resp = tcp.recv(1024).decode()
            try:
                chat[name] = {}
                chat[name]["socket"] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                chat[name]["socket"].connect((resp.split(':')[0][5:],int(resp.split(':')[1])))
                chat[name]["socket"].send('USER lolo\r\n'.encode())
                chat[name]['backup'] = []
                chat[name]['new'] = {}
                current = name
                clear()
                print(YELLOW("<- Visualizar MENU: /menu"))
                print(GREEN(f'<Chat com {name} >'))
                print(YELLOW("<- Visualizar INBOX: /menu"))
            except Exception as ex:
                print(RED("<<Alert!>>"))
                print(ex)

    elif msg[:4] == "/bye":
        chat[current]["socket"].send(f'DISC\r\n'.encode())
        chat.pop(current)
        current = ''
        clear()
        options()
    
    elif msg[:4] == "/msg":
        chat[current]["socket"].send(f'{msg[:5]}\r\n'.encode())
        chat[current]['backup'].append(f'[{time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())}]: {msg[5:]}')

    elif msg[:5] == "/menu":
        current = ''
        clear()
        options()

    elif msg[:5] == "/exit":
        if len(chat) > 0:
            for friend in chat.values():
                chat[friend]["socket"].send(f'DISC\r\n'.encode())
        break  

    elif msg[1:] != '\n':
        print(YELLOW('Nao entendi. Poderia repetir?'))
    
tcp.close() 