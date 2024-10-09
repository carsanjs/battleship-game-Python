import socket
import pickle
from config import IP_NETWORK

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = IP_NETWORK  # Escribe tu direccion local aquí, si no sabes cual es, solo abre una consola de windows y escribe el comando ipconfig
        self.port = 5555
        self.address = (self.server, self.port)
        self.id = self.connect()
        print(self.id)

    def connect(self):
        try:
            self.client.connect(self.address)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        # Sending data with fixed length header
        data_bytes = pickle.dumps(data)
        header = "{0:<20}".format(len(data_bytes))
        data = bytes(header, "utf-8") + data_bytes
        self.client.send(data)
        # Receiving data with fixed length header
        data_bytes = b""
        new_data = True
        while True:
            try:
                if new_data:
                    data_len = int(self.client.recv(20))
                    new_data = False
                else:
                    packet = self.client.recv(1024)
                    data_bytes += packet
                    if len(data_bytes) == data_len:
                        break
            except Exception as e:
                print(e)
                break
        return pickle.loads(data_bytes)

    def close(self):
        self.client.close()
