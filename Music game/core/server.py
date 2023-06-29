from bluetooth import *
import threading

class Server():
    def __init__(self):
        self.client_sock = None
        self.sock = None
        self.data = ""
        self.start()
    
    def start(self):
        server_sock = BluetoothSocket( RFCOMM )
        server_sock.bind(("",PORT_ANY))
        server_sock.listen(1)
        uuid = "4e67630f-f88e-4016-8203-822a23442311"

        advertise_service( server_sock, "SampleServer",
                        service_id=uuid,
                        service_classes=[uuid, SERIAL_PORT_CLASS],
                        profiles=[SERIAL_PORT_PROFILE])
        
        self.sock = server_sock
        thread = threading.Thread(target=self.accept_client)
        thread.daemon = True
        thread.start()

    def hasClient(self):
        return bool(self.client_sock)

    def accept_client(self):
        self.client_sock, _ = self.sock.accept()
    
    def get_server_sock(self):
        return self.sock

    def get_client_sock(self):
        return self.client_sock
    
    def get_client_data(self):
        return self.data
    
    def build(self):
        thread = threading.Thread(target=self.get_message, args=(self.client_sock,))
        thread.daemon = True
        thread.start()


    def get_message(self, client):
        while True:
            self.data = client.recv(1024)
            if len(self.data) == 0:
                break
    
    def close(self):
        if (self.client_sock):
            self.client_sock.close()
            self.client_sock = None
        if (self.sock):
            self.sock.close()
            self.sock = None