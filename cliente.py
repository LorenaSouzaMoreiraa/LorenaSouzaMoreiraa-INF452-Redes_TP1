# 108204 - Lorena Souza Moreira
import socket
import select
import time
import threading
import os
import random
import queue

# manter conexao ativa
def alive(start):
    while True:
        if time.time() - start >= 5.00:
            start = time.time()
            tcp.send('KEEP\r\n'.encode())

# cores
def RED(msg):
    return f'\033[31m{msg}\033[m'

def YELLOW(msg):
    return f'\033[33m{msg}\033[m'

def GREEN(msg):
    return f'\033[32m{msg}\033[m'

def BLUE(msg):
    return f'\033[36m{msg}\033[m'

# limpar terminal
def clear():
    if os.name == 'nt':  # Windows
        os.system('cls') or None
    else:
        os.system('clear') or None

# exibir comandos
def cheat():
    print(BLUE("___MENU___"))
    print("Inbox: /inbox")
    print("Entrar em um chat: /chat <nome_de_usuário>")
    print("Enviar mensagem: /msg <mensagem>")
    print("Encerrar chat: /bye")
    print("Desonline: /exit")
    print(BLUE("------------"))

# gerar porta para o cliente
def gerar_porta():
    return random.randint(1024, 65535)

def porta_disponivel(porta):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('0.0.0.0', porta))
            return True
        except OSError:
            return False

def porta():
    while True:
        porta = gerar_porta()
        if porta_disponivel(porta):
            return porta

# achar nome pelo socket
def find_key_by_socket(chat_dict, socket_to_find):
    for key, value in chat_dict.items():
        if value["socket"] is socket_to_find:
            return key
    return None

def menu():
    tcp.send('LIST\r\n'.encode())
    print(BLUE('___INBOX___'))
    print(f'{unread} mensagens não lidas')
    try:
        resp = tcp.recv(1024).decode()
        for friend in resp[5:].split(':'):
            if friend in chat and len(chat[friend]['new']) > 0:
                value = len(chat[friend]['new'])
                print(BLUE(f'{friend}___{value}'))
            else:
                print(friend)
        print(YELLOW("<- Visualizar MENU: /menu"))
    except Exception as ex:
        print(RED("<<Alert!>>"))
        print(ex)

# leitura
def command():
    while True:
        msg = input()
        q.put(msg)

# server central
HOSTC = '200.235.131.66'  # Endereco IP do servidor
PORTC = 10000  # Porta que o servidor esta

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (HOSTC, PORTC)
tcp.connect(dest)

# server local
HOST = ''  # Endereco IP do servidor
PORT = porta()  # Porta que o servidor esta

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
orig = (HOST, PORT)
server.bind(orig)
server.listen(1)

chat = {}
chat['server'] = {}
chat['server']['socket'] = server

# rand nome
nomes = ["flavin do pneu", "shaulin matador de porco", "capivaristo", "1000grau"]
me = random.choice(nomes)
tcp.send(f'USER {me}:{PORT}\r\n'.encode())

msg = ''
current = ''
unread = 0

# timer conexao
aux = time.time()
t = threading.Thread(target=alive, args=({aux}))
t.daemon = True
t.start()

q = queue.Queue()
tin = threading.Thread(target=command, args=({}))
tin.daemon = True
tin.start()

cheat()
while True:
    # busca atualizacoes
    if len(chat) > 0:
        try:
            inbox, _, _ = select.select([x['socket'] for x in chat.values()], [], [], 0.5)
        except Exception as ex:
            print(ex)

        before = unread
        for peer in inbox:
            if peer is server:
                con, cliente = server.accept()
                try:
                    request, _, _ = select.select([con], [], [], 0.1)
                    text = request[0].recv(1024).decode()
                    name = text[5:].strip()
                    chat[name] = {}
                    chat[name]['socket'] = con
                    chat[name]['backup'] = []
                    chat[name]['new'] = []
                    print(BLUE(f'[Conexao com {name} aceita]'))
                except Exception as ex:
                    print(ex)
            else:
                try:
                    text = peer.recv(1024).decode()
                    if text[:4] != 'DISC':
                        if current != '' and peer is chat[current]['socket']:
                            print(f'[{time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())}] {current}: {text}')
                            chat[current]['backup'].append(f'[{time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())}] {current}: {text}')
                        else:
                            name = find_key_by_socket(chat, peer)
                            if name:
                                chat[name]['new'].append(f'[{time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())}] {name}: {text}')
                                unread += 1
                    else:
                        name = find_key_by_socket(chat, peer)
                        if current == name:
                            clear()
                            cheat()
                            print(BLUE(f'[{name} encerrou a conversa]'))
                            current = ''
                        
                        del chat[name]
                except Exception as ex:
                    print(RED("<<Alert!>>"))
                    print(ex)
        if before < unread:
            print(BLUE(f'[{unread} mensagens nao lidas]'))
        
    try:
        msg = q.get_nowait()

        if msg[:6] == "/inbox":
            clear()
            tcp.send('LIST\r\n'.encode())
            print(BLUE('___INBOX___'))
            print(YELLOW(f'{unread} mensagens não lidas'))
            try:
                resp = tcp.recv(1024).decode()
                for friend in resp[5:].split(':'):
                    friend = friend.strip()
                    if friend in chat and len(chat[friend]['new']) > 0:
                        value = len(chat[friend]['new'])
                        print(BLUE(f'{friend}___{value}'))
                    else:
                        print(friend)
                print(YELLOW("<- Visualizar MENU: /menu"))
            except Exception as ex:
                print(RED("<<Alert!>>"))
                print(ex)

        elif msg[:5] == "/chat":
            name = msg[6:]
            # chat ja foi iniciado
            if (name == me):
                print(BLUE(f'Nao e possivel abrir um chat consigo.'))
            # chat ja foi iniciado
            elif name.strip() in chat.keys():
                clear()
                # muda o chat
                current = name
                print(YELLOW("<- Visualizar MENU: /menu"))
                print(YELLOW("<- Visualizar INBOX: /inbox"))
                print(GREEN(f'<Chat com {current}>'))
                # pega historico
                if len(chat[current]['backup']) > 0:
                    for text in chat[current]['backup']:
                        print(text)
                if len(chat[current]['new']) > 0:
                    print(BLUE('-----Novas mensagens------'))
                    for text in chat[current]['new']:
                        print(text)
                        chat[current]['backup'].append(text)
                    unread -= len(chat[current]['new'])
                    chat[current]['new'].clear()

            # nao existe o chat
            else:
                # pede conexao
                tcp.send(f'ADDR {name}\r\n'.encode())
                try:
                    resp = tcp.recv(1024).decode()
                    address = resp.split(':')[0][5:]
                    port = int(resp.split(':')[1])

                    name = name.strip()
                    chat[name] = {}
                    chat[name]["socket"] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    chat[name]["socket"].connect((address, port))
                    chat[name]["socket"].send(f'USER {me}\r\n'.encode())
                    chat[name]["backup"] = []
                    chat[name]["new"] = []
                    current = name
                    clear()
                    
                    print(YELLOW("<- Visualizar MENU: /menu"))
                    print(GREEN(f'<Chat com {name} >'))
                    print(YELLOW("<- Visualizar INBOX: /menu"))
                except Exception as ex:
                    print(YELLOW("<<Informações incorretas! Tente novamente.>>"))
                    print(ex)
                    print(address, port)
            

        elif msg[:4] == "/bye":
            chat[current]["socket"].send(f'DISC\r\n'.encode())
            chat.pop(current)
            current = ''
            clear()
            cheat()
            print(BLUE(f'[COnversa com {name} encerrada]'))

        elif msg[:4] == "/msg":
            chat[current]["socket"].send(f'{msg[5:]}\r\n'.encode())
            chat[current]['backup'].append(f'[{time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())}]: {msg[5:]}')

        elif msg[:5] == "/menu":
            current = ''
            clear()
            options()

        elif msg[:5] == "/exit":
            if len(chat) > 0:
                for friend in chat.values():
                    try:
                        friend["socket"].send(f'DISC\r\n'.encode())
                    except Exception as ex:
                        continue
            break

        elif len(msg) > 0:
            print(YELLOW('Nao entendi. Poderia repetir?'))
    
    except Exception as ex:
        continue

tcp.send(f'DISC\r\n'.encode())
tcp.close()
