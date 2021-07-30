import socket
import threading

##HOST = '0.0.0.0'
##HOST = '3.131.207.170'
##HOST = '127.0.0.1'
##HOST = '109.234.164.138'
PORT = 13532
NAME = socket.gethostname()
print(NAME)
HOST = socket.gethostbyname(NAME)
print(HOST)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()

clients = []
nicknames = []

def broadcast(message):
    print(message)
    for client in clients:
        client.send(message.encode('ascii'))

def handle(client):
    while True:
        try:
            message = client.recv(1024).decode('ascii')
##            message = str(message)
##            message = message.replace(message[0], '').replace(message[1], '').replace(message[:1], '')
##            message = message.replace("\n", "\n").replace('\n', '\n')
##            message = message.replace("\\n", "\n").replace('\\n', '\n')
            
            index = clients.index(client)
            nickname = nicknames[index]
            broadcast(f"{nickname}: {message}")
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f"{nickname} left the chat")
            nicknames.remove(nickname)
            send_list()
            break

def send_list():
    lst="LIST\n"
    for i in nicknames:
        lst=lst+i+"\n"
    lst=lst+"END"
    broadcast(lst)

def recieve():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}!")

        client.send("NAME".encode('ascii'))
        message = client.recv(1024).decode('ascii')
##        message = str(message)
##        message = message.replace(message[0], '').replace(message[1], '').replace(message[:1], '')
##        message = message.replace("\n", "\n").replace('\n', '\n')
##        message = message.replace("\\n", "\n").replace('\\n', '\n')

        nicknames.append(message)
        clients.append(client)

        send_list()

        print(f"the name of the client{str(address)} is {message}")
        broadcast(f"{message} connected to the server!")
        client.send("You are connected to the server successfully!".encode('ascii'))

        thread = threading.Thread(target = handle, args=(client,))
        thread.start()

print("Server is running")
recieve()
