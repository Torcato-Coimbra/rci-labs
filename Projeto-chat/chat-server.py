import socket
import select

# Define as configurações do servidor
HOST = 'localhost'
PORT = 1234

def start_server():
    # Cria um socket para o servidor
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"Servidor iniciado em {HOST}:{PORT}")
    
    # Lista de sockets para monitorar
    sockets_list = [server_socket]
    clients = {}

    while True:
        # Usa select para monitorar mudanças nos sockets
        read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

        for notified_socket in read_sockets:
            # Nova conexão de cliente
            if notified_socket == server_socket:
                client_socket, client_address = server_socket.accept()
                sockets_list.append(client_socket)
                clients[client_socket] = client_address
                print(f"Nova conexão de {client_address}")
            
            # Recebendo mensagem de um cliente existente
            else:
                try:
                    message = notified_socket.recv(1024)
                    if not message:
                        # Se a mensagem for vazia, o cliente desconectou
                        print(f"Conexão fechada por {clients[notified_socket]}")
                        sockets_list.remove(notified_socket)
                        del clients[notified_socket]
                        continue

                    # Exibe a mensagem recebida e retransmite para todos os clientes
                    print(f"Mensagem recebida de {clients[notified_socket]}: {message.decode('utf-8')}")
                    for client_socket in clients:
                        if client_socket != notified_socket:
                            client_socket.send(message)

                except Exception as e:
                    print(f"Erro com o cliente {clients[notified_socket]}: {e}")
                    sockets_list.remove(notified_socket)
                    del clients[notified_socket]

        for notified_socket in exception_sockets:
            sockets_list.remove(notified_socket)
            del clients[notified_socket]

if __name__ == "__main__":
    start_server()
