"""A simple webserver.
"""
import asyncio
import os

from .femtoweb.femtoweb.filesystem_endpoints import _fs_GET
from .femtoweb.femtoweb.server import (
    _200,
    _303,
    GET,
    POST,
    route,
    event_source,
    serve as _serve,
)

def serve(site_dir, host, port):
    event_emitters = []

    # Define an event stream endpoint.
    @route('/_events', methods=(GET,))
    @event_source
    async def events(request, emitter):
        event_emitters.append(emitter)

    # Define a _reload endpoint.
    @route('/_reload', methods=(POST,))
    async def reload(request):
        nonlocal event_emitters
        # Grab the current list of event_emitters.
        _event_emitters = event_emitters[:]
        # Clear the nonlocal event_emitters list.
        event_emitters[:] = []
        for emitter in _event_emitters:
            await emitter(['reload'])
        return _200()

    # Define a _error endpoint.
    @route('/_error', methods=(POST,))
    async def error(request):
        # Clear the nonlocal event_emitters list.
        for emitter in event_emitters:
            await emitter(['error', request.body.decode('utf-8')])
        return _200()

    # Define a catch-all GET handler for delivering files.
    @route('.*', methods=(GET,))
    async def get(request):
        req_path = request.path.lstrip('/')
        fs_path = os.path.join(site_dir, req_path)
        if req_path == '':
            # Return index.html as root.
            req_path = 'index.html'
        elif os.path.isdir(fs_path):
            if not req_path.endswith('/'):
                # If req_path references as directory but no trailing slash
                # was specified, redirect to the same path with trailing slash.
                return _303(location=f'/{req_path}/')
            if os.path.exists(os.path.join(fs_path, 'index.html')):
                # If req_path is a directory that contains an index.html,
                # return that file.
                req_path = f'{req_path.rstrip("/")}/index.html'
        elif (not os.path.exists(fs_path) and not req_path.endswith('.html')):
            # To mimic how common webservers work, resolve a path to an .html
            # file without having to specify it in the path.
            req_path += '.html'

        return _fs_GET(site_dir, req_path)

    # Start the server.
    loop = asyncio.get_event_loop()
    loop.create_task(_serve(host, port))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
