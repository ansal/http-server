# HTTP handlers implementation

import os
import urllib.parse


class FileSystemHandler:
    """
        A simple HTTP request handler that process GET and HEAD commands.
        Serves static files from a directory provided with appropriate MIME type.
    """

    def __init__(self, method, path, directory=None):

        # HTTP Method
        self.method = method

        #URL Path
        self.path = path

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
        # 
        # TODO: We are not likely to come here as the http callback will itself
        # handle the http method not implemented part.
        #
        method_function = "process_" + self.method
        if not hasattr(self, method_function):
            raise Exception("Method not supported")

        method = getattr(self, method_function)
        method()

        return (self.headers, self.response_buffer)


    def send_header(self, file_name):
        """ Sends the header for a request """
        self.headers.append("HTTP/1.0 200 OK")
        self.set_header("Server", "ToyServer/0.1")
        self.set_header("Content-type", "text/html")


    def set_header(self, name, value):
        """ Set the headers of the response """
        self.headers.append("{}: {}\r\n".format(name, value))


    def end_header(self):
        """ Ends header by appending  \r\n at the end of it """
        self.headers.append("\r\n")


    def process_HEAD(self):
        """ Processes HEAD request """
        pass


    def process_GET(self):
        """ Processes GET request """
        file_name = self.get_file_path()
        self.send_header(file_name)
        self.response_buffer = self.read_file(file_name)
        self.set_header("Content-length", len(self.response_buffer))
        self.end_header()


    def get_file_path(self):
        """ Returns the absolute file system path of the requested file """

        # Discard query parameters and hash URL fragments
        file_path = self.path.split("?", 1)[0]
        file_path = file_path.split("#", 1)[0]

        # Unquote all url characters
        file_path = urllib.parse.unquote(file_path)

        return self.directory + file_path


    def read_file(self, file_name):
        """ Reads a file and return its contents """
        try:
            f = open(file_name)
        except IsADirectoryError:
            # If a directory is specified as the path, try reading index.html
            # from the path.
            print(file_name + "index.html")
            try:
                f = open(file_name + "index.html")
            except Exception as e:
                raise e

        return f.read()

