import socket
import threading

from nvim_py_profile.utils.formatter import formatting_output


class Sender:
    def __init__(self, host='127.0.0.1', lua_port=22122, python_port=22123):
        self.host = host
        self.lua_port = lua_port
        self.python_port = python_port

        # Start the Python TCP server in a separate thread
        self.server_thread = threading.Thread(target=self.start_python_server, daemon=True)
        self.server_thread.start()

    def send_data(self, tuple_data):
        """Send data to the Lua script's TCP server."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((self.host, self.lua_port))
                formatted_string = f"{tuple_data[2]} ns"
                sended_data = (tuple_data[0], tuple_data[1], formatting_output(tuple_data[2]))
                data = f"{sended_data}\n"
                s.sendall(data.encode('utf-8'))
            except Exception as e:
                print("Error sending data to Lua:", e)

    def handle_client(self, conn, addr):
        """Handle incoming connections from the Lua script."""
        print(f"Connected by Lua at {addr}")
        try:
            data = conn.recv(4096).decode('utf-8').strip()
            if data:
                print("Received data from Lua:", data)
                # Process the data as needed
        except Exception as e:
            print("Error receiving data from Lua:", e)
        finally:
            conn.close()

    def start_python_server(self):
        """Start the Python TCP server to receive data from the Lua script."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.python_port))
            s.listen()
            print(f"Python TCP server is listening on port {self.python_port}")

            while True:
                conn, addr = s.accept()
                client_thread = threading.Thread(target=self.handle_client, args=(conn, addr))
                client_thread.start()
