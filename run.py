
import argparse
import json
import os
import shutil
from itertools import chain

from lib.htmlephant import Document
from lib.htmlephant_extensions import Main
from lib.server import serve
from lib import (
    copy_if_newer,
    NotDefined,
)
from lib.context import (
    Context,
    normalize_context,
)

import includes.head
import includes.footer
import includes.header
import includes.redirect

###############################################################################
# Site file writer helpers
###############################################################################

def write_page(context, filename, head=NotDefined, body=NotDefined):
    """Write a single HTML site page.
    """
    # Open the HTML output file.
    with context.open(filename) as fh:
        # Combine global includes with the module Head and Body to create
        # the final element tuples.
        head_els = chain(includes.head.Head(context), head(context))
        # Invoke the page body function and, if non-empty, assert that it
        # returns a single <main> element.
        page_body_els = body(context)
        if page_body_els and (len(page_body_els) != 1
                              or not isinstance(page_body_els[0], Main)):
            raise AssertionError(
                'Expected page_mod.Body() to return a single <main> element '
                f'but got {page_body_els} instead when attempting to write '
                f'file: {filename}'
            )
        body_els = chain(
            includes.header.Body(context),
            page_body_els,
            includes.footer.Body(context),
        )
        # Create the Document object.
        doc = Document(body_els, head_els)
        # Write the document to the file.
        for c in doc:
            fh.write(c)

def write_sitemap(context, filenames):
    with context.open(context.SITEMAP_FILENAME) as fh:
        fh.write(f'{context.base_url}/\n')
        for filename in filenames:
            fh.write(f'{context.base_url}/{filename}\n')

def write_robots(context):
    with context.open('robots.txt') as fh:
        fh.write(
f"""User-agent: *
Allow: /
Sitemap: {context.base_url}/{context.SITEMAP_FILENAME}
""")

###############################################################################
# Static file copy helper
###############################################################################

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
    for filename in os.listdir(static_dir):
        path = os.path.join(static_dir, filename)
        if os.path.isdir(path):
            # Path is a directory, so copy it as-is.
            dest = os.path.join(context.SITE_STATIC_DIR, filename)
            shutil.copytree(path, dest, dirs_exist_ok=True)
        elif not context.is_large_static_storable(filename):
            # This is not a large file, so copy to SITE_STATIC_DIR.
            dest = os.path.join(context.SITE_STATIC_DIR, filename)
            copy_if_newer(path, dest)
        else:
            # This is a large file, so create a symlink in
            # SITE_LARGE_STATIC_DIR instead of actually copying it.
            dest = os.path.join(context.SITE_LARGE_STATIC_DIR, filename)
            if not os.path.lexists(dest):
                # Use the absolute file system path as the symlink src instead
                # of trying to figure out how many parent dirs to references.
                os.symlink(
                    os.path.join(os.path.dirname(__file__), path),
                    dest
                )

###############################################################################
# Run Function
###############################################################################

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
        # Update the context object with the name of the current page module.
        context.current_page_mod = page_mod
        # Check for page generator.
        if (not hasattr(page_mod, 'CONTEXT_ITEMS_GETTER')
            or not hasattr(page_mod, 'FILENAME_GENERATOR')):
            # Write a single page.
            # Clear any previous generator item.
            context.generator_item = None
            filename = f'{page_name}.html'
            write_page(context, filename, page_mod.Head, page_mod.Body)
            filenames.append(filename)
        else:
            # Use the page generator to write 1 or more pages.
            items = page_mod.CONTEXT_ITEMS_GETTER(context)

            # Create a collection entry point page that redirects to the first
            # collection item.
            collection_name = page_mod.__name__.rsplit('.', 1)[1].split('_')[0]
            filename = f'{collection_name}s.html'
            item = next(iter(items))
            context.generator_item = item
            write_page(
                context,
                filename,
                lambda context: includes.redirect.Head(context, item['slug'])
            )
            filenames.append(filename)

            # Write the individual item pages.
            for item in items:
                # Update the context object with the current item.
                context.generator_item = item
                filename = page_mod.FILENAME_GENERATOR(item)
                write_page(context, filename, page_mod.Head, page_mod.Body)
                filenames.append(filename)

    # Write the sitemap and robots files.
    write_sitemap(context, filenames)
    write_robots(context)

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

    # Instantiate the Context object.
    if not os.path.exists(args.context_file):
        parser.error(f'Context file not found: {args.context_file}')
    context = Context(
        production=not args.development,
        **json.load(open(args.context_file, 'rb'))
    )

    # Do an in-place normalization of the context object values.
    normalize_context(context)

    # Generate the site files.
    run(context)
    print(f'Wrote new files to: {context.SITE_DIR}/')

    # Save store.exists_response_headers_cache
    if context.lss is not None:
        context.lss.save_manifest()

    # Maybe sync large static files to a remote store.
    if args.sync_large_static:
        if context.lss is None:
            raise Exception('Large static store is not configured. Please see: https://github.com/derekenos/derekenos.com-generator/blob/main/README.md#2-configure-the-store')
        context.lss.sync(context.SITE_LARGE_STATIC_DIR)

    # Maybe start the webserver.
    if args.serve:
        print(f'Serving at: http://{args.host}:{args.port}')
        serve(context.SITE_DIR, args.host, args.port)
