""" TCP-server on sockets """
import socket

def server():
    """ Creating TCP-server
    """
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(('localhost', 5000))

    server_sock.listen()
    while True:
        client_sock, client_addr = server_sock.accept()
        print(f'Client {client_addr} connected...')
        while True:
            data = client_sock.recv(4096)
            if not data:
                break
            print(f"Recv data from client: {data.decode()}")
            client_sock.send("Hello!\n".encode())
        client_sock.close()
    #Start the server with blocking functions:
    server()
    