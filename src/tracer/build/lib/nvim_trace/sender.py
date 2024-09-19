import socket


class Sender:
    _HOST = '127.0.0.1'

    def __init__(self, port: int = 24130):
        self.port = port

    def send_data(self, tuple_data):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self._HOST, self.port))
            data = f"{tuple_data}\n"
            s.sendall(data.encode('utf-8'))
