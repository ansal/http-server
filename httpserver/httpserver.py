# A simple implementation of HTTP server.

import sys
from http import HTTPStatus

from tcpserver import TCPServer
from handler import FileSystemHandler


# Supported HTTP methods
SUPPORTED_METHODS = ("HEAD", "GET", )


# Default error message and type

ERROR_MESSAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Error</title>
</head>
<body>
    Server error -
</body>
</html>
"""
ERROR_CONTENT_TYPE = "text/html;charset=utf-8"


# All you need to know about HTTP can be found here - 
# https://tools.ietf.org/html/rfc2616
#
# Here is an image of Telnet session where a request is made to the server
# using HTTP -
# https://en.wikipedia.org/wiki/File:Http_request_telnet_ubuntu.png
#
#
#               HTTP Request
#               ------------
#
# Briefly, an HTTP request is made of these three parts - 
# 1. Request type and path
# 2. Headers, which are optional
# 3. Data part, which is also optional
#
# The first line contains three part - 
# 1. command - HTTP methods like GET, POST etc
# 2. path - URL of the resource
# 3. version - The HTTP version like "HTTP/1.0" or "HTTP/1.1"
#
# Headers and data are separated by blank lines.
# 
# If the first line only contains two part, it is considered as a HTTP 0.9
# request that has no optional headers and data.
#
# Commands are case sensitive.
#
#
#               HTTP Response
#               -------------
#
# Similar to the request, response contains there parts - 
# 1. Response code
# 2. Headers
# 3. Data
#
# Similar to request, headers and data are separated by blank lines.

class HTTPServer(TCPServer):
    server_version = "HTTPServer/0.1"


    def __init__(self, *args, directory=None, **kwargs):
        super().__init__(*args, callback=self.tcp_callback, bytes_count=65536, **kwargs)
        self.directory = directory


    def tcp_callback(self, queue, data):
        """ Callback for the TCP Server """

        # Once we have data from the TCP server, parse it first
        status = self.parse_request(data)

        # If parse request failed, send an error code and message to the client
        if not status:
            self.send_error(queue)
            return

        # Handle the request.
        # handle_request will call the file handler which will deal with the
        # reading of file, setting headers etc
        self.handle_request()

        # Send the response by putting the data in TCP server's queue
        self.send_response(queue)

    def parse_request(self, data):
        """
        Parses a HTTP request.
        Returns True if it was able to parse the request successfully.
        Returns False otherwise.
        """

        # The error code and text that will be sent to the client if an error occurs
        self.error_code = None
        self.error_text = ""

        # Store the raw request came from the client
        self.raw_request = data
        self.request = str(self.raw_request, 'iso-8859-1')

        # Strip the last two new lines
        self.request = self.request.rstrip("\r\n")

        # Split the request into different lines
        words = self.request.split()

        # A proper server should check the request version, headers etc. I am
        # only checking if the HTTP method is supported, nothing else.

        # Get the request method and see if it is in the supported list.
        # If it is not in the supported methods, set the errors and return
        method = words[0]
        if method not in SUPPORTED_METHODS:
            self.error_code = HTTPStatus.METHOD_NOT_ALLOWED
            self.error_text = "Not a supported method"
            return False

        # Set the method and path
        self.method = method
        self.path = words[1]

        # Tell the callback that everything went fine.
        return True


    def handle_request(self):
        """ Handles a single HTTP request """
        handler = FileSystemHandler(self.method, self.path,
                directory=self.directory)
        self.headers, self.data = handler.handle()


    def send_response(self, queue):
        """ Sends response to the client """

        # Join the headers and data to form the response
        response = "".join(self.headers) + self.data + "\r\n"

        # Socket needs data in byte
        response = bytes(response, "utf-8")
        queue.put(response)


    def send_error(self, queue):
        """ Sends an error message to the client """

        # Set the http error code and message
        headers = [
            "HTTP/1.0 {} {}".format(self.error_code, self.error_text)
        ]
        headers.append("Server: {}".format(self.server_version))

        # Tell the client that the collection is closed
        headers.append("Connection: close")

        # Join the headers and put it in queue
        headers = bytes("\r\n".join(headers) + "\r\n", "utf-8")
        queue.put(headers)


    def log(self):
        """ The logger """
        pass



if __name__ == '__main__':

    # Check if a directory is passed from the command line
    try:
        directory = sys.argv[1]
    except IndexError:
        directory = None

    httpserver = HTTPServer('127.0.0.1', 8000, directory=directory)
    httpserver.start()
    httpserver.run()

