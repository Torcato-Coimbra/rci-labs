import socket
import select
import sys
import threading

def receive_messages(client_socket):
    while True:
        try:
            # Recebe mensagem do servidor
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                print("Conexão com o servidor foi fechada.")
                client_socket.close()
                break
            print(f"Mensagem recebida: {message}")
        except Exception as e:
            print(f"Erro ao receber mensagem: {e}")
            client_socket.close()
            break

def send_messages(client_socket):
    while True:
        message = input()
        if message.lower() == "sair":
            print("Desconectando do servidor...")
            client_socket.close()
            break
        try:
            client_socket.send(message.encode('utf-8'))
        except Exception as e:
            print(f"Erro ao enviar mensagem: {e}")
            client_socket.close()
            break

def start_client(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
        print(f"Conectado ao servidor {host}:{port}")
    except Exception as e:
        print(f"Não foi possível conectar ao servidor: {e}")
        return

    # Cria threads para enviar e receber mensagens simultaneamente
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    send_thread = threading.Thread(target=send_messages, args=(client_socket,))

    receive_thread.start()
    send_thread.start()

    receive_thread.join()  # Aguarda o término da thread de recepção
    send_thread.join()     # Aguarda o término da thread de envio

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python chat-client.py <host> <port>")
        sys.exit()

    host = sys.argv[1]
    port = int(sys.argv[2])

    start_client(host, port)
