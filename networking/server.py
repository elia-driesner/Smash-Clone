import socket
from _thread import *
import sys

class Server():
    def __init__(self):
        self.server = '192.168.0.139'
        print(self.server)
        self.port = 5555  
        
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.status = ''
        self.running = True
        self.data_size = 1
        
    def run(self):
        try:
            self.s.bind((self.server, self.port))
        except socket.error as e:
            print(str(e))
            
        self.s.listen(2)
        self.status = 'Server started, waiting for connection'
        print(self.status)
        
        while self.running:
            self.conn, self.addr = self.s.accept()
            
            start_new_thread(self.threaded_client, (self.conn,))
    
    def threaded_client(self, conn):
        reply = ''
        _run = True
        conn.send(str.encode('connected'))
        
        while _run:
            try:
                data = conn.recv(2048*self.data_size)
                reply = data.decode('utf-8')
                
                if not data:
                    self.status = 'Client disconnected'
                    _run = False
                    break
                else:
                    print('recieved: ', reply)
                    print('sending: ', reply)
                
                conn.sendall(str.encode(reply))
            except:
                break
        print('Client disconnected')
        conn.close()
          
test_server = Server()
test_server.run()