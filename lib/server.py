"""A simple webserver.
"""
import asyncio
import os

from .femtoweb.filesystem_endpoints import _fs_GET
from .femtoweb.server import (
    _200,
    GET,
    POST,
    route,
    as_event_source,
    serve as _serve,
)

def serve(site_dir, host, port):
    event_senders = []

    # Define an event stream endpoint.
    @route('/_events', methods=(GET,))
    @as_event_source
    async def events(request, sender):
        event_senders.append(sender)

    # Define a _reload endpoint.
    @route('/_reload', methods=(POST,))
    async def reload(request):
        nonlocal event_senders
        # Grab the current list of event_senders.
        _event_senders = event_senders[:]
        # Clear the nonlocal event_senders list.
        event_senders[:] = []
        for sender in _event_senders:
            await sender('reload')
        return _200()

    # Define a catch-all GET handler for delivering files.
    @route('.*', methods=(GET,))
    async def get(request):
        req_path = request.path.lstrip('/')
        if req_path == '':
            # Return index.html as root.
            req_path = 'index.html'
        elif (not os.path.exists(os.path.join(site_dir, req_path))
              and not req_path.endswith('.html')):
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
