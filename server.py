from json import load
import socket, threading
from service.api import ApiService

HOST = "127.0.0.1"
PORT = 9091

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()

clients = []

# broadcast
def broadcast(message):
    for client in clients:
        client.send(message)

# handle
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            data = load_service(message.decode("utf-8"))
            # broadcast(f"{data}.\n".encode("utf-8"))
            broadcast(f"{data}.\n\n".encode("utf-8"))
        except:
            clients.remove(client)
            client.close()
        

# receive
def receive():
    while True:
        client, address = server.accept()
        print(f"Conectado em {str(address)}!\n")

        # Encaminhar mensagem para client
        client.send(f"Seja bem-vindo {str(address)}".encode("utf-8"))
        msg_client = client.recv(1024)

        clients.append(client)

        # Carregando dados da API
        data = load_service(msg_client.decode("utf-8"))

        print("[*] Broadcast:")
        broadcast(f"{address} ==> {data}.\n\n".encode("utf-8"))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


def load_service(string):
    print('string', string)
    state = string.strip()[0:2]
    city = string.strip()[3:]
    data = ApiService.search(state, city)
    return data

print(f"Servidor em execução...{HOST}:{PORT}")
receive()