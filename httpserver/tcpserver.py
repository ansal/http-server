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

            # Process the socketd that need to be read from
            for socket in read:

                # If the socket is our server socket, then it means that there
                # is a client waiting at the other end to connect
                if socket is self._socket:

                    # If you want the IP, you can get it from the second value
                    # of the tuple below _
                    client_socket, _ = self._socket.accept()
                    client_socket.setblocking(0) # Make it non-blocking.

                    # Add the socket to the list of readers list
                    self._readers.append(client_socket)

                    # And give it a queue for any callback to put data
                    self.queue[client_socket] = queue.Queue()

                else:

                    # This is some other client trying to send us data. So read
                    # that data.
                    try:
                        data = socket.recv(self.bytes_count)
                    except Exception as e:
                        raise e

                    # If there is data from the socket, call the callback and
                    # put the socket in the writer list incase the callback
                    # decided to put some data in the queue and we have to send
                    # it to the client later.
                    if data:
                        if self.callback is not None:
                            self.callback(self.queue[socket], data)

                        if socket not in self._writers:
                            self._writers.append(socket)

                    else:

                        # We have received no data ie zero bytes. So close the
                        # connection and remove the socket.
                        self.remove_socket(socket)

            # Process the sockets that need to be written to
            for socket in write:

                # Get the data from the queue
                try:
                    data = self.queue[socket].get_nowait()
                except queue.Empty:
                    # The queue is empty. The callback probably didn't put any
                    # data in it. Hence remove it from the writer list
                    self._writers.remove(socket)
                else:
                    # Callback has put some data in the queue. So send it back
                    # to the client.
                    socket.send(data)

                    # Once the data is send, remove the socket from everywhere,
                    # destroy the queue and close it.
                    self.remove_socket(socket)

            # Process the sockets that have errors
            for socket in err:

                # Remove and close the socket
                self.remove_socket(socket)

    def remove_socket(self, socket):

        # Remove the socket from both lists, destroy the queue and close the
        # socket.

        if socket in self._readers:
            self._readers.remove(socket)

        if socket in self._writers:
            self._writers.remove(socket)

        del self.queue[socket]

        socket.close()

