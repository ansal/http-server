# Simple TCP server

import socket


class TCPServer:

    def __init__(self, ip, port, max_connections=5, bytes_count=1024):

        # The IP address this server binds to
        self.ip = ip

        # The port this server binds to
        self.port = port

        # Number of bytes to be read from the socket
        self.bytes_count = bytes_count

        # Maximum number of connections
        self._max_connections = max_connections

        # Create an INET, STREAMing socket
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        self._socket.listen(self._max_connections)

