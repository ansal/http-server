# An example TCP client.
# Retrieves a web page from a server.


import sys
import socket


class TCPClient:

    def __init__(self, ip, port, bytes_count=1024):

        # The IP address this client connects to
        self.ip = ip

        # The port this client connects to
        self.port = port

        # Number of bytes to be read from the response
        self.bytes_count = bytes_count

        # Create an INET, STREAMing socket
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self._socket.connect((self.ip, self.port))

    def send(self, data):
        # data argument takes the data to be sent to the server.
        # If the data is string type, we have to convert it into bytes.
        # send method returns the string received from the server
        if type(data) == str:
            data = bytes(data, 'utf-8')
        self._socket.send(data)

    def read(self):
        # Read all the data from the buffer
        returned_data = b''
        while True:
            chunk = self._socket.recv(self.bytes_count)
            
            # The recv method returns an empty byte object if there is no more
            # data left to read.
            if not chunk:
                return returned_data
            else:
                returned_data += chunk

    def close(self):
        self._socket.close()


if __name__ == '__main__':

    # Create the client and connect
    client = TCPClient('127.0.0.1', 8000)
    client.connect()

    # I am trying to connect to a HTTP server here.
    # So send a bare minimum GET request to fetch the index page from the
    # server.
    client.send("GET / HTTP/1.0\r\n\r\n")
    response = client.read()
    print(response)
    
    # Close the connection.
    client.close()

