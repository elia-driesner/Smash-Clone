import socket

class Network():
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = '192.168.0.139'
        self.port = 5555
        self.addr = (self.server, self.port)
        self.connected = False
        
        self.id = self.connect()
        self.pos = (100, 100)
        print(self.id)
        
    def connect(self):
        try:
            self.client.connect(self.addr)
            recieved = self.client.recv(2048).decode()
            if recieved:
                self.connected = True
            return recieved
        except  socket.error as e:
            self.connected = False
            print(e)
            return e
        
    def send(self, data):
        try:
            self.client.send(str.encode(data))  
            return self.client.recv(2048).decode()
        except  socket.error as e:
            print(e)
            return e
        