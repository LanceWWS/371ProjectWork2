import socket
import pickle

class network:
    def __init__(self):
        #create server
        self.server = "10.0.0.8" # add your server address here
        self.port = 5555
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = (self.server, self.port)
        self.id = self.connect()
        print(self.id)

    def getP(self):
        return self.id
    
    def connect(self):
        try:
            
            # Connect to the server
            self.client.connect((self.addr))
            return self.recv(2048).decode()
        except:
            pass
        
    def send(self, data):
        try:
            # Encode the data to UTF-8
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(2048*2))
        except socket.error as e:
            print(e)

#n = network()
#print(n.send("Hello")) 
        
