import socket
import threading
from datetime import datetime

HOST = 'localhost'
PORT = 5000

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((HOST, PORT))
servidor.listen()

clientes = {}  
historico = []  

print("Servidor iniciado...")

def registrar_log(texto):
    with open("log.txt", "a", encoding="utf-8") as log:
        log.write(f"{datetime.now()} - {texto}\n")

def broadcast(mensagem, remetente_socket=None):
    for cliente in clientes:
        if cliente != remetente_socket:
            try:
                cliente.send(mensagem.encode())
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

def tratar_cliente(cliente):
    try:
        nome = cliente.recv(1024).decode()
        clientes[cliente] = nome
        print(f"{nome} conectou.")
        registrar_log(f"{nome} conectou.")

        cliente.send("Conectado ao servidor!\n".encode())

        if historico:
            cliente.send("\n--- Últimas mensagens ---\n".encode())
            for msg in historico:
                cliente.send((msg + "\n").encode())
            cliente.send("-------------------------\n".encode())

        broadcast(f"{nome} entrou no chat.", cliente)

        while True:
            mensagem = cliente.recv(1024).decode()

            if not mensagem:
                break

            if mensagem == "/usuarios":
                lista = "Usuários online:\n"
                for n in clientes.values():
                    lista += f"- {n}\n"
                cliente.send(lista.encode())
                continue

            if mensagem.startswith("/privado"):
                try:
                    partes = mensagem.split(" ", 2)
                    destino_nome = partes[1]
                    texto = partes[2]

                    for sock, n in clientes.items():
                        if n == destino_nome:
                            msg_privada = f"(Privado) {nome}: {texto}"
                            sock.send(msg_privada.encode())
                            cliente.send(msg_privada.encode())
                            registrar_log(msg_privada)
                            break
                except:
                    cliente.send("Uso: /privado nome mensagem\n".encode())
                continue

            msg_formatada = f"{nome}: {mensagem}"
            print(msg_formatada)
            registrar_log(msg_formatada)

            historico.append(msg_formatada)
            if len(historico) > 10:
                historico.pop(0)

            broadcast(msg_formatada, cliente)

    except:
        pass
    finally:
        remover_cliente(cliente)

def aceitar_conexoes():
    while True:
        cliente, endereco = servidor.accept()
        thread = threading.Thread(target=tratar_cliente, args=(cliente,))
        thread.start()

aceitar_conexoes()