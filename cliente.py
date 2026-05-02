import socket
import threading

HOST = 'localhost'
PORT = 5000

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((HOST, PORT))

nome = input("Digite seu nome: ")
cliente.send(nome.encode())

def receber():
    while True:
        try:
            mensagem = cliente.recv(1024).decode()
            if mensagem:
                print(mensagem)
            else:
                break
        except:
            print("Erro na conexão.")
            cliente.close()
            break

def enviar():
    while True:
        mensagem = input()
        cliente.send(mensagem.encode())

thread_receber = threading.Thread(target=receber)
thread_receber.start()

thread_enviar = threading.Thread(target=enviar)
thread_enviar.start()