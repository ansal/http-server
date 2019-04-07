# HTTP handlers implementation

import os
import urllib.parse
import mimetypes


class FileSystemHandler:
    """
        A simple HTTP request handler that process GET and HEAD commands.
        Serves static files from a directory provided with appropriate MIME type.
    """

    def __init__(self, method, path, directory=None, server_version="HttpServer0.1"):

        # HTTP Method
        self.method = method

        #URL Path
        self.path = path

        # Server version
        self.server_version = server_version

        # Header list
        self.headers = []

        # Response buffer
        self.response_buffer = ""

        # The directory to serve file
        if directory is None:
            directory = os.getcwd()
        self.directory = directory


    def handle(self):
        """
            Handles a HTTP method.
        """

        # Check if a supported HTTP method is requested by the client
        # If not raise an exception.
        method_function = "process_" + self.method
        if not hasattr(self, method_function):
            raise Exception("Method not supported")

        method = getattr(self, method_function)
        method()

        return (self.headers, self.response_buffer)


    def init_headers(self):
        """ Initializes headers for a request """

        # Response code and version
        self.headers.append("HTTP/1.0 200 OK\r\n")

        # Server name
        # TODO: Remove the hard coding
        self.set_header("Server", self.server_version)

        # Content type of the resource
        self.set_header("Content-type", mimetypes.guess_type(self.file_path)[0])


    def set_header(self, name, value):
        """ Set the headers of the response """
        self.headers.append("{}: {}\r\n".format(name, value))


    def end_header(self):
        """ Ends header by appending  \r\n at the end of it """
        self.headers.append("\r\n")


    def process_HEAD(self):
        """ Processes HEAD request """

        # Get the file path from the request path
        self.get_file_path()

        # Initialize the headers
        self.init_headers()

        # Unlike GET, HEAD only needs headers
        self.end_header()


    def process_GET(self):
        """ Processes GET request """

        # Get the file path from the request path
        self.get_file_path()

        # Initializes the headers
        self.init_headers()

        # Read the file
        self.response_buffer = self.read_file()

        # Set the content length
        self.set_header("Content-length", str(len(self.response_buffer)))

        # End the headers
        self.end_header()


    def get_file_path(self):
        """ Returns the absolute file system path of the requested file """

        # Discard query parameters and hash URL fragments
        file_path = self.path.split("?", 1)[0]
        file_path = file_path.split("#", 1)[0]

        # Unquote all url characters
        file_path = urllib.parse.unquote(file_path)

        self.file_path = self.directory + file_path

        # If the file is a directory, set the index.html as the file path
        if os.path.isdir(self.file_path):
            self.file_path += "index.html"


    def read_file(self):
        """ Reads a file and return its contents """
        try:
            f = open(self.file_path, "rb")
        except Exception as e:
            raise e
        else:
            return f.read()

