# An example showing the use of HTTPServer
# If you pass a folder location, it serves that directory
# Or serves the current working directory

import sys

# Import httpserver in the python import path
sys.path.insert(0, "./httpserver")

from httpserver import HTTPServer

if __name__ == '__main__':

    # Check if a directory is passed from the command line
    try:
        directory = sys.argv[1]
    except IndexError:
        directory = None

    httpserver = HTTPServer('127.0.0.1', 8000, directory=directory)
    httpserver.start()
    httpserver.run()

