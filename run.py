
import argparse
import json
import os
import shutil
from itertools import chain

from lib.htmlephant import Document
from lib.server import serve

import includes.head
import includes.body

###############################################################################
# Context Class
###############################################################################

class Context:
    PAGES_DIR = 'pages'
    STATIC_DIR = 'static'
    SITE_DIR = 'site'
    SITE_STATIC_DIR = 'site/static'

    def __init__(self, production=False, **kwargs):
        self.production = production
        # Generate a list of page names in self.PAGES_DIR.
        self.page_names = [
            mod_name.rsplit('.', 1)[0]
            for mod_name in os.listdir(self.PAGES_DIR)
            if mod_name.endswith('.py')
        ]
        # Add any custom attributes.
        for k, v in kwargs.items():
            setattr(self, k, v)

    def static(self, filename):
        """Format filename as a static asset path, assert that he file exists,
        and return the path.
        """
        path = f'{self.STATIC_DIR}/{filename}'
        if not os.path.isfile(path):
            raise AssertionError(f'Path is not a regular file: {path}')
        return path

    def open(self, path):
        """Return a writable UTF-8 file handle for a self.SITE_DIR sub-path.
        """
        path = os.path.join(self.SITE_DIR, path.lstrip('/'))
        return open(path, 'w', encoding='utf-8')

###############################################################################
# Run Function
###############################################################################

def write_page(context, filename, mod_head, mod_body):
    # Open the HTML output file.
    with context.open(filename) as fh:
        # Combine global includes with the module Head and Body to create
        # the final element tuples.
        head_els = chain(includes.head.Head(context), mod_head(context))
        body_els = chain(includes.body.Body(context), mod_body(context))
        # Create the Document object.
        doc = Document(body_els, head_els)
        # Write the document to the file.
        for c in doc:
            fh.write(c)

def run(context):
    # Copy static files to output, creating dirs as necessary.
    shutil.copytree(
        src=context.STATIC_DIR,
        dst=context.SITE_STATIC_DIR,
        dirs_exist_ok=True
    )

    # Iterate through the pages, writing each to the site dir.
    for page_name in context.page_names:
        # Update the context object with the name of the current page.
        context.current_page = page_name
        # Import the page module.
        m = __import__(
            f'{context.PAGES_DIR}.{page_name}',
            fromlist=page_name
        )
        # Check for page generator.
        if (not hasattr(m, 'CONTEXT_ITEMS_GETTER')
            or not hasattr(m, 'FILENAME_GENERATOR')):
            # Write a single page.
            filename = f'{page_name}.html'
            write_page(context, filename, m.Head, m.Body)
        else:
            # Use the page generator to write 1 or more pages.
            for item in m.CONTEXT_ITEMS_GETTER(context):
                filename = m.FILENAME_GENERATOR(item)
                write_page(context, filename, m.Head(item), m.Body(item))

###############################################################################
# CLI
###############################################################################

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--development', action='store_true')
    parser.add_argument('--context-file', type=argparse.FileType('rb'))
    parser.add_argument('--serve', action='store_true')
    parser.add_argument('--host', default='localhost')
    parser.add_argument('--port', type=int, default=5000)
    args = parser.parse_args()

    # Set the default Context kwargs.
    ctx_kwargs = { 'production': not args.development }
    if args.context_file:
        # Update Context kwargs with custom context file.
        ctx_kwargs.update(json.load(args.context_file))
    context = Context(**ctx_kwargs)

    # Generate the site files.
    run(context)

    # Maybe start the webserver.
    if args.serve:
        serve(context.SITE_DIR, args.host, args.port)
