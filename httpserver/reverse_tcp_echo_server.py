# An example showing the use of httpserver.TCPServer
# Reverses the data received from the client and send it back

from tcpserver import TCPServer


def reverse_data(queue, data):
    queue.put(data[::-1])
    print(data)


if __name__ == '__main__':
    server = TCPServer('127.0.0.1', 8000, callback=reverse_data)
    server.start()
    server.run()

