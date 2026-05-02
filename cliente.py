import socket
import threading

def receive_messages(cliente_socket):
    while True:
        try:
            data = cliente_socket.recv(1024).decode('utf-8')
            if data:
                print(data)
            else:
                break
        except:
            print("Conexão encerrada.")
            cliente_socket.close()
            break

def connect_server(host: str, port: int):
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente_socket.connect((host, port))

    print("Connected to server")

    nome = input("Digite seu nome: ")
    cliente_socket.send(nome.encode('utf-8'))

    thread = threading.Thread(
        target=receive_messages,
        args=(cliente_socket,)
    )
    thread.start()

    while True:
        message = input()
        cliente_socket.send(message.encode('utf-8'))


if __name__ == '__main__':
    HOST = 'localhost'  
    PORT = 8000

    connect_server(HOST, PORT)