
import argparse
import json
import os
from itertools import chain
from datetime import datetime
from glob import glob

from lib import copy_if_newer
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
    SITE_RELATIVE_STATIC_DIR = 'static'
    SITE_STATIC_DIR = f'{SITE_DIR}/{SITE_RELATIVE_STATIC_DIR}'
    STATIC_LARGE_FILE_THRESHOLD_MB = 1
    SITE_RELATIVE_LARGE_STATIC_DIR = f'static/large'
    SITE_LARGE_STATIC_DIR = f'{SITE_DIR}/{SITE_RELATIVE_LARGE_STATIC_DIR}'

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

    def static_last_modified_iso8601(self, filename):
        return datetime.fromtimestamp(
            os.stat(os.path.join(self.STATIC_DIR, filename)).st_mtime
        ).isoformat()

    def static(self, filename):
        """Format filename as a static asset path, assert that the file exists,
        and return the path.
        """
        path = f'{self.STATIC_DIR}/{filename}'
        if not os.path.isfile(path):
            raise AssertionError(f'Path is not a regular file: {path}')

        if not self.is_large_static(filename):
            path = f'{self.SITE_RELATIVE_STATIC_DIR}/{filename}'
        else:
            if self.production:
                return f'{self.large_static_store["endpoint"]}/{filename}'
            path = os.path.join(self.SITE_RELATIVE_LARGE_STATIC_DIR, filename)
        return path

    def is_large_static(self, filename):
        path = f'{self.STATIC_DIR}/{filename}'
        if not os.path.isfile(path):
            raise AssertionError(f'Path is not a regular file: {path}')
        return os.stat(path).st_size / 1024 / 1024 \
            >= self.STATIC_LARGE_FILE_THRESHOLD_MB

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

def copy_static(context):
    """Copy files from the local static directory to the site
    static directory, diverting large objects as appropriate, and
    copying only if the destination file doesn't exist or is out-of-date.
    """
    # Ensure that the destination directories exist.
    os.makedirs(context.SITE_STATIC_DIR, exist_ok=True)
    os.makedirs(context.SITE_LARGE_STATIC_DIR, exist_ok=True)

    # Iterate through files in the static directory.
    static_dir = context.STATIC_DIR
    static_dir_len = len(static_dir)
    for fs_path in glob(f'{static_dir}/*'):
        # Ignore directory-type paths.
        if os.path.isdir(fs_path):
            continue
        # Get the static-dir-relative path.
        filename = fs_path[static_dir_len + 1:]
        # Check whether the file exceeds the large object threshold.
        if context.is_large_static(filename):
            # This is a large file - create a symlink in the destination directory
            # instead of actually copying it.
            dest = os.path.join(context.SITE_LARGE_STATIC_DIR, filename)
            if not os.path.lexists(dest):
                # Use the absolute file system path as the symlink src instead of
                # trying to figure out how many parent dirs to references.
                os.symlink(
                    os.path.join(os.path.dirname(__file__), fs_path),
                    dest
                )
        else:
            dest = os.path.join(context.SITE_STATIC_DIR, filename)
            copy_if_newer(fs_path, dest)

def run(context):
    # Copy static files to output, creating dirs as necessary.
    copy_static(context)

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
    parser.add_argument('--context-file', default='context.json')
    parser.add_argument('--serve', action='store_true')
    parser.add_argument('--host', default='0.0.0.0')
    parser.add_argument('--port', type=int, default=5000)
    parser.add_argument('--sync-large-static', action='store_true')
    args = parser.parse_args()

    # Set the default Context kwargs.
    ctx_kwargs = { 'production': not args.development }

    # Attempt to read the context file.
    if not os.path.exists(args.context_file):
        parser.error(f'Context file not found: {args.context_file}')
    ctx_kwargs.update(json.load(open(args.context_file, 'rb')))
    context = Context(**ctx_kwargs)

    # Generate the site files.
    run(context)
    print(f'Wrote new files to: {context.SITE_DIR}/')

    # Maybe sync large static files to a remote store.
    if args.sync_large_static:
        from lib.large_static_store import sync
        sync(context.large_static_store, context.SITE_LARGE_STATIC_DIR)

    # Maybe start the webserver.
    if args.serve:
        print(f'Serving at: http://{args.host}:{args.port}')
        serve(context.SITE_DIR, args.host, args.port)
