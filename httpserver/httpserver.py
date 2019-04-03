# A simple implementation of HTTP server.

from tcpserver import TCPServer


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


    def parse_request(self):
        """ Parses a HTTP request """
        pass


    def handle_request(self):
        """ Handles a single HTTP request """
        pass


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

