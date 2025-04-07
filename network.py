#network for client side

import socket
import pickle
import time

class network:
    def __init__(self):
        #create server
        self.server = "10.0.0.8" # add your server address here
        self.port = 5555
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = (self.server, self.port)
        self.p = self.connect()
        print(f"Player ID: {self.p}")  # Debug: Print the player ID to check
        if self.p is None:
            print("Error: Failed to receive player ID from the server!")

    def getP(self):
        return self.p
    
    def connect(self):
        try:
            # Connect to the server
            self.client.connect((self.addr))
            time.sleep(1) 
            data = self.client.recv(2048)
            player_id = int(data.decode())
            print(f"Player ID received in network: {player_id}")  # Debugging output
            if not data:
                print("No data received from server")
                return None
            return player_id
            #return self.client.recv(2048).decode()
        except:
            pass
        
    def send(self, data):
        try:
            # Encode the data to UTF-8
            self.client.send(str.encode(data))
            data = self.client.recv(2048*2)
            #print(f"Data received in send method: {data}")  # Debugging output
            if not data:
                print("No data received from server")
                return None
            #return pickle.loads(self.client.recv(2048*2))
            return pickle.loads(data)
        except socket.error as e:
            print(e)

#n = network()
#print(n.send("Hello")) 
        
