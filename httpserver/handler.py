# HTTP handlers implementation


class FileSystemHandler:
    """
        A simple HTTP request handler that process GET and HEAD commands.
        Serves static files from a directory provided with appropriate MIME type.
    """

    def __init__(self, method, path):
        self.method = method
        self.path = path


    def handle(self):
        """
            Handles a HTTP method.
        """
        print(self.method, self.path)

        # TODO: Remove the below temporary method
        header = """
HTTP/1.0 200 OK
Server: SimpleHTTP/0.6 Python/2.7.13
Date: Wed, 03 Apr 2019 13:44:50 GMT
Content-type: text/html
Content-Length: 277
Last-Modified: Wed, 03 Apr 2019 12:39:02 GMT

"""
        html = open("test.html").read()
        print(len(html))

        return bytes(header + html, "utf-8")

