import socket

HOST = '127.0.0.1'  # Server's hostname or IP address
PORT = 12345        # Port used by the server

def send_data(tuple_data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        data = f"{tuple_data}\n"
        s.sendall(data.encode('utf-8'))
