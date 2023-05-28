import socket
from select import select
list_fd = [] # спсиок файловых дескрипторов

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #создается файловый дескриптор
server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_sock.bind(('localhost', 5000))
server_sock.listen()

def accept_connect(server_sock):
    client_sock, client_addr = server_sock.accept()
    print(f'Client {client_addr} connected...')
    list_fd.append(client_sock)
        
def send_msg(client_sock):
    data = client_sock.recv(4096)    
    if not data:
        client_sock.close()
    else:
        print(f"Recv data from client: {data.decode()}")
        client_sock.send("Hello!\n".encode())

def event_loop():
    while True:
        # ready_to_read - список сокетов, готовых для чтения 
        ready_to_read, _, _ = select(list_fd, [], []) # [read], [write], [error]
        for sock in ready_to_read:
            if sock is server_sock:
                accept_connect(server_sock)
            #Client socket:
            else:
                send_msg(sock)
        


if __name__ == "__main__":
    list_fd.append(server_sock)
    event_loop()