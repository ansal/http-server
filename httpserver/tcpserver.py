# Simple TCP server

import socket


class TCPServer:

    def __init__(self, ip, port, callback=None, max_connections=5, bytes_count=1024):

        # The IP address this server binds to
        self.ip = ip

        # The port this server binds to
        self.port = port

        # Callback to run after a request is served
        self.callback = callback

        # Number of bytes to be read from the socket
        self.bytes_count = bytes_count

        # Maximum number of connections
        self._max_connections = max_connections

        # Create an INET, STREAMing socket
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        # Set it as a non-blocking one
        self._socket.setblocking(0)

        # Bind the socket to specified ip and port
        self._socket.bind((self.ip, self.port))

        # And finally, start listening
        self._socket.listen(self._max_connections)


if __name__ == '__main__':
    server = TCPServer('127.0.0.1', 3000)
    server.start()

