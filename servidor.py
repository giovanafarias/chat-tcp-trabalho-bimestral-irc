import socket
import threading
from datetime import datetime

clientes = {}  
historico = []  

def registrar_log(texto: str):
    with open("log.txt", "a", encoding="utf-8") as log:
        log.write(f"{datetime.now()} - {texto}\n")

def broadcast(mensagem: str, remetente=None):
    for cliente in clientes:
        if cliente != remetente:
            try:
                cliente.send(mensagem.encode('utf-8'))
            except:
                remover_cliente(cliente)

def remover_cliente(cliente):
    if cliente in clientes:
        nome = clientes[cliente]
        print(f"{nome} desconectou.")
        registrar_log(f"{nome} desconectou.")
        del clientes[cliente]
        cliente.close()
        broadcast(f"{nome} saiu do chat.")

def handle_client(client_socket, addr):
    try:
        nome = client_socket.recv(1024).decode('utf-8')
        clientes[client_socket] = nome

        print(f"{addr} - {nome} conectou.")
        registrar_log(f"{nome} conectou.")

        if historico:
            client_socket.send("\n--- Últimas mensagens ---\n".encode('utf-8'))
            for msg in historico:
                client_socket.send((msg + "\n").encode('utf-8'))
            client_socket.send("-------------------------\n".encode('utf-8'))

        broadcast(f"{nome} entrou no chat.", client_socket)

        while True:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break

            if data == "/usuarios":
                lista = "Usuários online:\n"
                for n in clientes.values():
                    lista += f"- {n}\n"
                client_socket.send(lista.encode('utf-8'))
                continue

            if data.startswith("/privado"):
                try:
                    partes = data.split(" ", 2)
                    destino = partes[1]
                    mensagem = partes[2]

                    for sock, n in clientes.items():
                        if n == destino:
                            msg = f"(Privado) {nome}: {mensagem}"
                            sock.send(msg.encode('utf-8'))
                            client_socket.send(msg.encode('utf-8'))
                            registrar_log(msg)
                            break
                except:
                    client_socket.send("Uso: /privado nome mensagem\n".encode('utf-8'))
                continue

            mensagem_formatada = f"{nome}: {data}"
            print(mensagem_formatada)
            registrar_log(mensagem_formatada)

            historico.append(mensagem_formatada)
            if len(historico) > 10:
                historico.pop(0)

            broadcast(mensagem_formatada, client_socket)

    except:
        pass
    finally:
        remover_cliente(client_socket)

def start_server(host: str, port: int):

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()

    print(f"Server Started at {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        thread = threading.Thread(
            target=handle_client,
            args=(client_socket, addr)
        )
        thread.start()

if __name__ == '__main__':
    HOST = '0.0.0.0'
    PORT = 8000

    start_server(HOST, PORT)