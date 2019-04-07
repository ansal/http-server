# http-server

This is a simple web server written in Python. I built this to understand how HTTP works. Some more info behind this server can be found in my blog - [http://blog.ansals.me/2019/04/07/writing-a-simple-web-server-in-python/](http://blog.ansals.me/2019/04/07/writing-a-simple-web-server-in-python/)

The web server contains three parts - 
1. TCP Server [httpserver/tcpserver.py](httpserver/tcpserver.py)
2. HTTP Server [httpserver/httpserver.py](httpserver/httpserver.py)
3. File system handler [httpserver/handler.py](httpserver/handler.py)

A few examples using the above classes can be found in the [examples](examples/) folder. To run the web server from the examples folder, run
`python3 examples/http_file_server.py`
