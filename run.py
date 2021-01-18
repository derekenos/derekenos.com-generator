
import argparse
import json
import os
import shutil
from itertools import chain

from lib.htmlephant import Document
from lib.server import serve

import includes.head
import includes.body
import includes.footer

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
        # Initialize runtime attributes.
        self.current_page = None
        self.generator_item = None
        # Add any custom attributes.
        for k, v in kwargs.items():
            setattr(self, k, v)

    def static(self, filename):
        """Format filename as a static asset path, assert that the file exists,
        and return the path.
        """
        path = f'{self.STATIC_DIR}/{filename}'
        if not os.path.isfile(path):
            raise AssertionError(f'Path is not a regular file: {path}')
        return path

    def url(self, path):
        """Return path as an absolute URL.
        """
        return f'{self.base_url if self.production else ""}/{path.lstrip("/")}'

    def static_url(self, filename):
        """Return an absolute URL for a static asset filename.
        """
        return self.url(self.static(filename))

    def open(self, path):
        """Return a writable UTF-8 file handle for a self.SITE_DIR sub-path.
        """
        path = os.path.join(self.SITE_DIR, path.lstrip('/'))
        return open(path, 'w', encoding='utf-8')

###############################################################################
# Run Function
###############################################################################

def write_page(context, filename, page_mod):
    # Open the HTML output file.
    with context.open(filename) as fh:
        # Combine global includes with the module Head and Body to create
        # the final element tuples.
        head_els = chain(includes.head.Head(context), page_mod.Head(context))
        body_els = chain(
            includes.body.Body(context),
            page_mod.Body(context),
            includes.footer.Body(context),
        )
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

    # Iterate through the pages, writing each to the site dir and collecting
    # the filenames for later sitemap creation.
    filenames = []
    for page_name in context.page_names:
        # Update the context object with the name of the current page.
        context.current_page = page_name
        # Import the page module.
        page_mod = __import__(
            f'{context.PAGES_DIR}.{page_name}',
            fromlist=page_name
        )
        # Check for page generator.
        if (not hasattr(page_mod, 'CONTEXT_ITEMS_GETTER')
            or not hasattr(page_mod, 'FILENAME_GENERATOR')):
            # Write a single page.
            # Clear any previous generator item.
            context.generator_item = None
            filename = f'{page_name}.html'
            write_page(context, filename, page_mod)
            filenames.append(filename)
        else:
            # Use the page generator to write 1 or more pages.
            for item in page_mod.CONTEXT_ITEMS_GETTER(context):
                # Update the context object with the current item.
                context.generator_item = item
                filename = page_mod.FILENAME_GENERATOR(item)
                write_page(context, filename, page_mod)
                filenames.append(filename)

    # Write sitemap.txt
    with context.open('sitemap.txt') as fh:
        for filename in filenames:
            fh.write(f'{context.base_url}/{filename}\n')

    # Write robots.txt
    with context.open('robots.txt') as fh:
        fh.write(
f"""User-agent: *
Allow: /
Sitemap: {context.base_url}/sitemap.txt
""")


###############################################################################
# CLI
###############################################################################

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--development', action='store_true')
    parser.add_argument('--context-file', type=argparse.FileType('rb'))
    parser.add_argument('--serve', action='store_true')
    parser.add_argument('--host', default='0.0.0.0')
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
    print(f'Wrote new files to: {context.SITE_DIR}/')

    # Maybe start the webserver.
    if args.serve:
        print(f'Serving at: http://{args.host}:{args.port}')
        serve(context.SITE_DIR, args.host, args.port)
