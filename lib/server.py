"""A simple webserver.
"""
import os
from http import server

def serve(path, host='localhost', port=5000):
    # Subclass SimpleHTTPRequestHandler to make it act more like a webserver.
    class HTTPRequestHandler(server.SimpleHTTPRequestHandler):
        def do_GET(self, *args, **kwargs):
            if self.path == f'/':
                # Resolve / request path to index.html
                self.path += '/index.html'
            elif (not os.path.exists(f'{self.directory}{self.path}')
                  and not self.path.endswith('html')):
                # No file exists at path and path doesn't end with .html, so
                # add .html
                self.path = f'{self.path}.html'
            return super().do_GET()

    print(f'Serving on: http://{host}:{port}')
    return server.HTTPServer(
        (host, port),
        lambda *args, **kwargs: HTTPRequestHandler(
            *args, **kwargs, directory=path
        )
    ).serve_forever()
