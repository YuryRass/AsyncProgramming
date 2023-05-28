import socket
import selectors

selector = selectors.DefaultSelector()


def server():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #создается файловый дескриптор
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(('localhost', 5000))
    server_sock.listen()
    #  регистрация событий для сервера
    selector.register(fileobj=server_sock, events=selectors.EVENT_READ, data=accept_connect)

def accept_connect(server_sock):
    client_sock, client_addr = server_sock.accept()
    print(f'Client {client_addr} connected...')
    selector.register(fileobj=client_sock, events=selectors.EVENT_READ, data=send_msg)
        
def send_msg(client_sock):
    data = client_sock.recv(4096)    
    if not data:
        selector.unregister(client_sock)
        client_sock.close()
    else:
        print(f"Recv data from client: {data.decode()}")
        client_sock.send("Hello!\n".encode())

def event_loop():
    while True:
        events = selector.select() # (key = {fileobj, events, data}, events)
        for key, _ in events:
            callback = key.data
            callback(key.fileobj)
        
        


if __name__ == "__main__":
    server()
    event_loop()