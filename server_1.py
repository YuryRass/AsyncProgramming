import socket

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_sock.bind(('localhost', 5000))
server_sock.listen()

def accept_connect(server_sock):
    while True:
        client_sock, client_addr = server_sock.accept()
        print(f'Client {client_addr} connected...')
        send_msg(client_sock)
        
def send_msg(client_sock):
    while True:
        data = client_sock.recv(4096)
        
        if not data:
            break
        else:
            print(f"Recv data from client: {data.decode()}")
            client_sock.send("Hello!\n".encode())
    client_sock.close()

if __name__ == "__main__":
    accept_connect(server_sock)