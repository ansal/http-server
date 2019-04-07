# A simple implementation of HTTP server.

import sys
from http import HTTPStatus
import datetime

from tcpserver import TCPServer
from handler import FileSystemHandler


# Supported HTTP methods
SUPPORTED_METHODS = ("HEAD", "GET", )


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

    # Server version
    server_version = "HTTPServer/0.1 github.com/ansal/http-server"


    def __init__(self, *args, directory=None, **kwargs):
        super().__init__(*args, callback=self.tcp_callback, bytes_count=65536, **kwargs)
        self.directory = directory

        self.log("{} started".format(self.server_version))


    def tcp_callback(self, queue, data):
        """ Callback for the TCP Server """

        # Once we have data from the TCP server, parse it first
        status = self.parse_request(data)

        # If parse request failed, send an error code and message to the client
        if not status:
            self.send_error(queue)
            return

        # Handle the request.
        # handle_request will call the FileSystemHandler which will deal with the
        # reading of file, setting headers etc
        self.handle_request(queue)


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
        self.method = words[0]
        self.path = words[1]
        if self.method not in SUPPORTED_METHODS:
            self.error_code = HTTPStatus.METHOD_NOT_ALLOWED
            self.error_text = "Not a supported method"
            return False

        # Tell the callback that everything went fine.
        return True


    def handle_request(self, queue):
        """ Handles a single HTTP request """
        handler = FileSystemHandler(self.method, self.path,
                directory=self.directory, server_version=self.server_version)

        # Let the FileSystemHandler try to read and return the file.
        try:
            self.headers, self.data = handler.handle()

        # If file is not found, send a 404 status
        except FileNotFoundError:
            self.error_code = HTTPStatus.NOT_FOUND
            self.error_text = "File not found"
            self.send_error(queue)

        # Any other exception, we will treat it as an internal server error
        except Exception as e:
            print(e)
            self.error_code = HTTPStatus.INTERNAL_SERVER_ERROR
            self.error_text = "Server error occurred"
            self.send_error(queue)

        # If all is well, send the data back to the tcp queue
        else:
            # Send the response by putting the data in TCP server's queue
            self.send_response(queue)


    def send_response(self, queue):
        """ Sends response to the client """

        # Socket excepts the data in bytes format

        # Build the headers part first
        response = bytes("".join(self.headers), "utf=8")

        # If there is data needs to be sent, put it in the response as well
        if self.data:
            response += bytes(self.data)

        # Put the data in the TCP callback queue
        queue.put(response)

        self.log("{} {} -- {}".format(self.method, self.path, 200))


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

        self.log("{} {} -- {}".format(self.method, self.path, self.error_code))


    def log(self, message):
        """ The logger """
        date = datetime.datetime.now()
        print("[{}] -- {}".format(date, message))

