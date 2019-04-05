# A simple implementation of HTTP server.

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, callback=self.tcp_callback, bytes_count=65536, **kwargs)

    def tcp_callback(self, queue, data):
        """ Callback for the TCP Server """

        # Once we have data from the TCP server, parse it first
        status = self.parse_request(data)

        if not status:
            print(self.error_code, self.error_text)
            queue.put(bytes(self.error_text, "utf-8"))
        else:
            headers, data = self.handle_request()
            response = "".join(headers) + data + "\r\n"

            print(headers)

            print(response)

            # Socket needs data in byte
            response = bytes(response, "utf-8")

            queue.put(response)

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
            self.error_text = "Not a supported method!"
            return False

        # Set the method and path
        self.method = method
        self.path = words[1]

        # Tell the callback that everything went fine.
        return True


    def handle_request(self):
        """ Handles a single HTTP request """
        handler = FileSystemHandler(self.method, self.path)
        return handler.handle()


    def send_header(self):
        """ Sends header """
        pass


    def end_headers(self):
        """ Sends a blank line ending the headers """
        pass


    def send_response(self):
        """ Sends response """
        pass


    def send_error(self):
        """ Sends an error message to the client """
        pass


    def log(self):
        """ The logger """
        pass



if __name__ == '__main__':
    httpserver = HTTPServer('127.0.0.1', 8000)
    httpserver.start()
    httpserver.run()

