import socket
import threading
import json

class SimpleClient: 
    def __init__(self, server="localhost", port=5555):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server
        self.port = port
        self.addr = (self.server, self.port)
        self.connected = False
        self.callback = None
        self.listener_thread = None
        
    def connect(self):
        try:
            self.client.connect(self.addr)
            self.connected = True
            print(f"Connected to server at {self.addr}")
            
            # Start the listener thread
            self.listener_thread = threading.Thread(target=self._listen_for_messages, daemon=True)
            self.listener_thread.start()
            
            return True
        except Exception as e:
            print(f"Connection Error: {e}")
            return False
    
    def disconnect(self):
        if self.connected:
            self.send("disconnect")
            self.connected = False
            self.client.close()
            print("Disconnected from server")
    
    def send(self, message):
        try:
            # Encode the message as UTF-8
            encoded_message = message.encode("utf-8")
            self.client.send(encoded_message)
            return True
        except socket.error as e:
            print(f"Send Error: {e}")
            return False
    
    def register_callback(self, callback_function):
        self.callback = callback_function
    
    def _listen_for_messages(self):
        while self.connected:
            try:
                # Receive data from server
                data = self.client.recv(2048).decode("utf-8")
                
                # If no data, connection might be closed
                if not data:
                    print("Server connection closed")
                    self.connected = False
                    break
                
                print(f"Received from server: {data}")
                
                # Call the callback function if registered
                if self.callback:
                    self.callback(data)
                    
            except socket.error as e:
                print(f"Socket Error in listener: {e}")
                self.connected = False
                break
            except Exception as e:
                print(f"Unexpected error in listener: {e}")


# Testing
if __name__ == "__main__":
    def handle_message(message):
        print(f"Callback received message: {message}")
    
    # Create and connect client
    client = SimpleClient()
    if client.connect():
        # Register callback
        client.register_callback(handle_message)
        
        try:
            # Keep the main thread running and allow sending messages
            while client.connected:
                message = input("Enter message to send (or 'q' to quit): ")
                if message.lower() == 'q':
                    break
                
                client.send(message)
                
        except KeyboardInterrupt:
            print("Interrupted by user")
        finally:
            client.disconnect()