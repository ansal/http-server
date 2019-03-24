# Simple TCP server

import socket
import queue
import select


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

        # Create a list of readers and writers of sockets for reading and writing data.
        self._readers = [self._socket, ] # Our server socket will be the first.
        self._writers = []

        # We also need a dictionay of queues for data to be sent from the
        # callback.
        self.queue = {}


    def start(self):
        """ Binds the socket and start listening """

        # Set it as a non-blocking one
        self._socket.setblocking(0)

        # Bind the socket to specified ip and port
        self._socket.bind((self.ip, self.port))

        # And finally, start listening
        self._socket.listen(self._max_connections)


    def run(self):

        # Create the main server loop that reads and writes data from the
        # sockets.
        while True:

            # Call the select.select() call to get notified when the sockets
            # are ready for processing.
            # It will actually call the OS system call select() which monitors
            # sockets, open files, pipes etc for any communication/error
            # happening on them. See
            # https://docs.python.org/3/library/select.html for more
            # information.
            read, write, err = select.select(
                    self._readers,
                    self._writers,
                    self._readers
                )

            # Process the sockest that need to be read from
            for socket in read:
                pass

if __name__ == '__main__':
    server = TCPServer('127.0.0.1', 3000)
    server.start()
    server.run()

