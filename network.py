# network for client side
import socket
import pickle
import time
import subprocess
import os

class network:
    def __init__(self, start_server=False):
        self.server = "169.254.205.157"
        self.port = 55555
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = (self.server, self.port)
        self.server_process = None

        if not self.try_connect():
            if start_server:
                self.start_server()
                time.sleep(2)
                self.try_connect()
            else:
                raise ConnectionError("No server found.")
    
    def try_connect(self):
        """Try to connect to server, return True if successful"""
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect(self.addr)
            time.sleep(0.5)
            data = self.client.recv(2048)
            self.p = int(data.decode())
            print(f"Connected to server. Received player ID: {self.p}")
            return True
        except Exception as e:
            print(f"No server running: {e}")
            return False
            
    def start_server(self):
        """Start the server as a subprocess"""
        print("No server detected. Starting server...")
        try:
            # Get the path of the server script
            # Note: Update the path to your server script
            server_script = "server.py"  # Or absolute path if needed
            
            # Start the server as a subprocess
            if os.name == 'nt':  # Windows
                self.server_process = subprocess.Popen(
                    ["python", server_script], 
                    creationflags=subprocess.CREATE_NEW_CONSOLE
                )
            else:  # Unix/Linux/Mac
                self.server_process = subprocess.Popen(
                    ["python3", server_script],
                    stdout=subprocess.PIPE
                )
                
            print(f"Server started with PID: {self.server_process.pid}")
        except Exception as e:
            print(f"Error starting server: {e}")

    def getP(self):
        return self.p
    
    def connect(self):
        """Legacy connect method for backward compatibility"""
        try:
            # Connect to the server
            self.client.connect((self.addr))
            time.sleep(1)
            data = self.client.recv(2048)
            player_id = int(data.decode())
            if not data:
                print("No data received from server")
                return None
            return player_id
        except Exception as e:
            print(f"Connection error: {e}")
            return None
        
    def send(self, data):
        try:
            # Encode the data to UTF-8
            self.client.send(str.encode(data))
            received_data = self.client.recv(2048*2)
            if not received_data:
                print("No data received from server")
                return None
            return pickle.loads(received_data)
        except socket.error as e:
            print(f"Send error: {e}")
            return None