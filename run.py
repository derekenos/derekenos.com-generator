
import argparse
import os
import shutil

from lib.htmlephant import Document

import includes.head
import includes.body

PAGES_DIR = 'pages'
STATIC_DIR = 'static'
SITE_DIR = 'site'
SITE_STATIC_DIR = f'{SITE_DIR}/{STATIC_DIR}'

_open = lambda path: open(os.path.join(SITE_DIR, path), 'w', encoding='utf-8')

class Context:
    def __init__(self, pages_dir, static_dir, development=False):
        self.pages_dir = pages_dir
        self.static_dir = static_dir
        self.development = development
        self.current_page = None
        self.page_names = [
            mod_name.rsplit('.', 1)[0]
            for mod_name in os.listdir(pages_dir)
            if mod_name.endswith('.py')
        ]

    def _static(self, filename):
        path = f'{self.static_dir}/{filename}'
        if not os.path.isfile(path):
            raise AssertionError(f'Path is not a regular file: {path}')
        return path

def run(development):
    # Build the global context dict.
    context = Context(PAGES_DIR, STATIC_DIR, development)

    # Copy static files to output, creating dirs as necessary.
    shutil.copytree(STATIC_DIR, SITE_STATIC_DIR, dirs_exist_ok=True)

    for page_name in context.page_names:
        context.current_page = page_name
        with _open(f'{page_name}.html') as fh:
            mod = __import__(f'{PAGES_DIR}.{page_name}', fromlist=page_name)
            # Include the global head elements.
            head_els = includes.head.Head(context) + mod.Head(context)
            body_els = includes.body.Body(context) + mod.Body(context)
            doc = Document(body_els, head_els)
            for c in doc:
                fh.write(c)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--development', action='store_true')
    args = parser.parse_args()
    run(args.development)
