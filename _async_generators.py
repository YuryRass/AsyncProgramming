import socket
from select import select

tasks = [] # очередь с задачами
# словари с генераторами для соответствующих сокетов (read, write): 
to_read, to_write = {}, {}

def server():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(('localhost', 5000))
    server_sock.listen()
    print("Server listen...")
    while True:
        yield ('read', server_sock)
        client_sock, client_addr = server_sock.accept()
        print(f'Client {client_addr} connected...')
        tasks.append(client(client_sock))

def client(client_sock):         
    while True:
        yield ('read', client_sock)
        data = client_sock.recv(4096)        
        if not data:
            break
        else:
            #print(f"Recv data from client: {data.decode()}")
            yield ('write', client_sock)
            client_sock.send("Hello!\n".encode())
        
    client_sock.close()
    
def event_loop():
    while True:
        while not tasks:
            # в select передаем сокеты (список ключей из to_write и to_read)
            ready_to_read, ready_to_write, _ = select(to_read, to_write, [])
            
            for sock in ready_to_read:
                tasks.append(to_read.pop(sock))
            for sock in ready_to_write:
                tasks.append(to_write.pop(sock))
                
        try:
            task = tasks.pop(0)
            reason, sock = next(task) # example: ('read', client_sock)
            if reason == 'read':
                to_read[sock] = task
                print("Len of read-tasks:", len(tasks))            
            else: #if reason == 'write':
                to_write[sock] = task
                print("Len of write-tasks:", len(tasks))
        except StopIteration:
            pass
            
if __name__ == "__main__":
    tasks.append(server())
    event_loop()