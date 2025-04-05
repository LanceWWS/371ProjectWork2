import socket

class network:
    def __init__(self):
        self.server = server # add server address here
        self.port = 5555
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = (self.server, self.port)
        self.id = self.connect()
        print(self.id)

    def connect(self):
        try:
            
            # Connect to the server
            self.client.connect((self.server, self.port))
            return self.recv(2048).decode()
        except:
            pass
    def send(self, data):
        try:
            # Encode the data to UTF-8
            self.client.send(str.encode(data))
            return self.recv(2048).decode()
        except socket.error as e:
            print(e)

n = network()
print(n.send("Hello")) 
        
